
import os
import sys
import time
import csv
import logging
import numpy as np
from PyQt5.QtCore import pyqtSignal, QSettings, QObject, pyqtSlot
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from pyqt_instruments import ui_data_saver
from pyqtgraph import PlotWidget

import pyqtgraph as pg

class Spectrometer(QWidget):
    name = 'Spectrometer'
    signal_dump_spec = pyqtSignal(object, object, object)
    signal_dump_spec_stop = pyqtSignal()
    signal_dataReady = pyqtSignal(object, object)
    def __init__(self):
        super().__init__()
        self.m_sp_plotter = PlSpectrometer()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.m_sp_plotter)
        self.setLayout(self.layout)

    def slot_on_spec_update(self, devicesMap, useSum):
        dataSum = 0
        plotIndex = 0
        if not useSum:
            self.m_sp_plotter.clear()
        for device in devicesMap.values():
            for chan in device.channels:
                if chan.isActive:
                    print("Channel name: {0}".format(chan.name))
                    dataSum += np.array(chan.data)
                    if not useSum:
                        self.m_sp_plotter.plot(self.m_sp_plotter.bins, np.array(chan.data), pen = pg.mkPen(\
                            color = self.m_sp_plotter.clr_cycle[plotIndex], width=2), name=chan.name)
                plotIndex += 1

        time = self.m_sp_plotter.bins
        counts = np.array(dataSum)          
        if useSum:
            self.m_sp_plotter.pltgraph.setData(time, counts)
        print("Spectrum dumped")

class PlSpectrometer(PlotWidget):
    clr_cycle = ['#000', '#c77', '#0f0', '#00f','#054', '#d21', '#6f0', '#712', '#912', '#a3e', '#f21', '#840']

    def __init__(self):
        super().__init__()
        self.setBackground('w')
        self.setXRange(0, 1024, padding=0)
        self.setYRange(0, 100, padding=0)
        self.setMouseEnabled(x=True, y=True)
        self.setLimits(yMin=0)
        self.setLabel('left', 'Counts')
        self.setLabel('bottom', 'Channel ID')  

        self.showGrid(x=True, y=True, alpha=0.5)
        self.setTitle("Spectrum")
        self.addLegend()

        self.is_dumping = False
        self.waves_to_dump = 1
        self.dataset = np.array([0] * 1024)
        self.bins = np.array( range(0, len(self.dataset)))
        self.pen = pg.mkPen(color=(255, 0, 0))
        self.pltgraph = self.plot(self.bins, self.dataset, name="Test", pen = self.pen )


class Spectro(QObject):
    finished = pyqtSignal()
    signal_dataReady = pyqtSignal(object)
    nEntries = 3
    def __init__(self, devicesMap, isCont):
        super().__init__()
        self.devicesMap = devicesMap
        self.isContinuous = isCont

    @pyqtSlot()
    def run(self):
        self.get_spectrum(self.nEntries)
        self.finished.emit()

    @pyqtSlot(object, object, object, object)
    def get_spectrum(self, nEntries):
        #self.settings = settings
        #for deviceIP in self.devicesMap:
        #    self.settings["ip"] = deviceIP
        #    self.devicesMap[deviceIP].board.connect(self.settings)

        data = dict()
        for i in range(nEntries):
            for device in self.devicesMap.values():
                device.board.transport.client.write('SPEC?')             #query spectra
                data.update({device.ip: device.board.transport.read_data()})  #get spectra from device
                #for each channel data length is 1024 bytes + 3 bytes per channel + 6 ending bytes after the whole data array
                #data is within ranges nChannel*1027 : nChannel*1027 + 1024
                #or nChannel*1027 : (nChannel+1)*1027 - 3
                nActiveChannels = int(((len(data[device.ip]) - 6)/1027))
                for chan in range(0, nActiveChannels):
                    dataChunk = data[device.ip][chan*1027:(chan+1)*1027-3]
                    if self.isContinuous:
                        device.channels[chan].data = np.add(device.channels[chan].data, dataChunk)
                        #self.m_graphWidget.dataSets = self.m_graphWidget.addPlot(device.channels[chan].name)
                    else:
                        device.channels[chan].data = dataChunk
            self.signal_dataReady.emit(self.devicesMap)