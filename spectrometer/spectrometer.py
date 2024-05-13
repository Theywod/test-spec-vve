'''
  Project       : Spectrometer
  Author        : chumadan
  Contacts      : dkc1@tpu.ru
  Workfile      : spectrometer.py
  Description   : Data acquisition interface for multi-channel spectrometer
'''

import os
import sys
import time
import csv
import logging
import re
import numpy as np
from PyQt5.QtCore import pyqtSignal, QSettings, QObject, pyqtSlot
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from pyqt_instruments import ui_data_saver
from pyqtgraph import PlotWidget

import pyqtgraph as pg

class Spectrometer(QWidget):
    name = 'Spectrometer'
    signal_dataReady = pyqtSignal(object, object)
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.devicesMap = None
        self.useSum = True

        self.btn_clear.clicked.connect(self.m_sp_plotter.clear)
        self.btn_replot_act.clicked.connect(self.replot)

    def setupUI(self):
        self.m_sp_plotter = PlSpectrometer()
        self.btn_clear = QPushButton("Clear plot")
        self.btn_replot_act = QPushButton("Replot only active")
        self.btn_replot_act.setEnabled(False)
        self.lbl_entries = QLabel("0/0 entries")

        self.layout = QVBoxLayout()

        self.layout_btns = QHBoxLayout()
        self.layout_btns.addWidget(self.btn_clear)
        self.layout_btns.addWidget(self.btn_replot_act)
        self.layout_btns.addWidget(self.lbl_entries)

        self.layout.addLayout(self.layout_btns)
        self.layout.addWidget(self.m_sp_plotter)
        self.setLayout(self.layout)

    def replot(self):
        text = self.lbl_entries.text()
        entries = re.findall(r'\d+', text)[0]
        self.slot_on_spec_update(self.devicesMap, entries, self.useSum)

    @pyqtSlot(object, object)
    def slot_on_spec_update(self, devicesMap, entry, useSum):
        self.devicesMap = devicesMap
        self.useSum = useSum

        dataSum = 0
        plotIndex = 0
        self.m_sp_plotter.clear()
        for device in self.devicesMap.values():
            for chan in device.channels:
                if chan.isActive:
                    print("Channel name: {0}".format(chan.name))
                    dataSum += np.array(chan.data)
                    if not useSum:
                        self.m_sp_plotter.plot(self.m_sp_plotter.bins, np.array(chan.data), pen = pg.mkPen(\
                            color = self.m_sp_plotter.clr_cycle[plotIndex], width=2), name=chan.name)
                plotIndex += 1

        bins = self.m_sp_plotter.bins
        counts = np.array(dataSum)          
        if self.useSum:
            self.m_sp_plotter.plot(bins,counts, pen = self.m_sp_plotter.pen, name = "Summary spectrum")
        
        self.lbl_entries.setText("{0} frames".format(entry))

        self.btn_replot_act.setEnabled(True)
        print("Spectrum plotted")

class PlSpectrometer(PlotWidget):
    clr_cycle = ['#000', '#c77', '#0f0', '#00f','#054', '#d21', '#6c5', '#712', '#912', '#a3e', '#f21', '#840']

    def __init__(self):
        super().__init__()
        self.setBackground('w')
        self.setXRange(0, 1024, padding=0)
        self.setYRange(0, 100, padding=0)
        self.enableAutoRange(axis='y')
        self.setMouseEnabled(x=False, y=True)
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


class SpectraDAQ(QObject):
    finished = pyqtSignal()
    signal_dataReady = pyqtSignal(object, int)
    nEntries = 10
    def __init__(self, devicesMap, isCont):
        super().__init__()
        self.devicesMap = devicesMap
        self.isContinuous = isCont
        self.setStop = False

    @pyqtSlot()
    def run(self):
        self.get_spectrum(self.nEntries)
        self.setStop = False
        print("Data acquisition finished")
        self.finished.emit()



    def get_spectrum(self, nEntries):
        data = dict()
        for entry in range(nEntries):
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
            self.signal_dataReady.emit(self.devicesMap, (entry+1))

            if self.setStop:                          
                self.setStop = False
                break