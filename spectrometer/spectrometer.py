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
import numpy as np
from PyQt5.QtCore import pyqtSignal, QSettings, QObject, pyqtSlot
from PyQt5 import QtWidgets, QtCore
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
        self.layout = QVBoxLayout()

        self.groupBox_PeakStab = QtWidgets.QGroupBox()
        self.groupBox_PeakStab.setTitle("Peak stabilization")
        self.gridLayout_PeakStab = QtWidgets.QGridLayout(self.groupBox_PeakStab)

        #Enable
        self.m_check_keep_on_channel = QtWidgets.QCheckBox(self.groupBox_PeakStab)
        self.m_check_keep_on_channel.setText("Enable")
        #self.m_check_keep_on_channel.setObjectName("m_check_keep_on_channel")
        self.gridLayout_PeakStab.addWidget(self.m_check_keep_on_channel, 0, 0, 1, 1)

        #Peak in area
        self.m_label_peak_stabil2 = QtWidgets.QLabel(self.groupBox_PeakStab)
        self.m_label_peak_stabil2.setEnabled(False)
        #self.m_label_peak_stabil2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.m_label_peak_stabil2.setText("Peak in area")
        #self.m_label_peak_stabil2.setObjectName("m_label_peak_stabil2")
        self.gridLayout_PeakStab.addWidget(self.m_label_peak_stabil2, 1, 0, 1, 1)
        self.m_spin_area_to_track = QtWidgets.QSpinBox(self.groupBox_PeakStab)
        self.m_spin_area_to_track.setEnabled(False)
        self.m_spin_area_to_track.setMinimum(1)
        self.m_spin_area_to_track.setMaximum(3)
        self.m_spin_area_to_track.setProperty("value", 2)
        #self.m_spin_area_to_track.setObjectName("m_spin_area_to_track")
        self.gridLayout_PeakStab.addWidget(self.m_spin_area_to_track, 1, 1, 1, 1)

        #Step size
        self.m_label_peak_stabil_step_size = QtWidgets.QLabel(self.groupBox_PeakStab)
        self.m_label_peak_stabil_step_size.setEnabled(False)
        #self.m_label_peak_stabil_step_size.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.m_label_peak_stabil_step_size.setText("Step size")
        self.gridLayout_PeakStab.addWidget(self.m_label_peak_stabil_step_size, 2, 0, 1, 1)
        self.m_spin_peak_stabil_step_size = QtWidgets.QSpinBox(self.groupBox_PeakStab)
        self.m_spin_peak_stabil_step_size.setEnabled(False)
        self.m_spin_peak_stabil_step_size.setMinimum(1)
        self.m_spin_peak_stabil_step_size.setMaximum(32)
        #self.m_spin_peak_stabil_step_size.setObjectName("m_spin_peak_stabil_step_size")
        self.gridLayout_PeakStab.addWidget(self.m_spin_peak_stabil_step_size, 2, 1, 1, 1)

        #Avg frames for search
        self.m_label_peak_stabil1 = QtWidgets.QLabel(self.groupBox_PeakStab)
        self.m_label_peak_stabil1.setEnabled(False)
        #self.m_label_peak_stabil1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.m_label_peak_stabil1.setText("Avg frames for search")
        #self.m_label_peak_stabil1.setObjectName("m_label_peak_stabil1")
        self.gridLayout_PeakStab.addWidget(self.m_label_peak_stabil1, 1, 2, 1, 1)
        self.m_spin_compensate_avg_frames = QtWidgets.QSpinBox(self.groupBox_PeakStab)
        self.m_spin_compensate_avg_frames.setEnabled(False)
        #self.m_spin_compensate_avg_frames.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.m_spin_compensate_avg_frames.setMaximum(600)
        self.m_spin_compensate_avg_frames.setProperty("value", 60)
        #self.m_spin_compensate_avg_frames.setObjectName("m_spin_compensate_avg_frames")
        self.gridLayout_PeakStab.addWidget(self.m_spin_compensate_avg_frames, 1, 3, 1, 1)

        #keep on channel
        self.m_label_peak_stabil3 = QtWidgets.QLabel(self.groupBox_PeakStab)
        self.m_label_peak_stabil3.setEnabled(False)
        #self.m_label_peak_stabil3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.m_label_peak_stabil3.setText("keep on channel")
        #self.m_label_peak_stabil3.setObjectName("m_label_peak_stabil3")
        self.gridLayout_PeakStab.addWidget(self.m_label_peak_stabil3, 2, 2, 1, 1)
        self.m_spin_keep_channel = QtWidgets.QSpinBox(self.groupBox_PeakStab)
        self.m_spin_keep_channel.setEnabled(False)
        #self.m_spin_keep_channel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.m_spin_keep_channel.setMaximum(1023)
        self.m_spin_keep_channel.setProperty("value", 150)
        #self.m_spin_keep_channel.setObjectName("m_spin_keep_channel")
        self.gridLayout_PeakStab.addWidget(self.m_spin_keep_channel, 2, 3, 1, 1)

        #Peak found on channel
        self.m_label_peak_stabil4 = QtWidgets.QLabel(self.groupBox_PeakStab)
        self.m_label_peak_stabil4.setEnabled(False)
        #self.m_label_peak_stabil4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.m_label_peak_stabil4.setText("Peak found on channel")
        #self.m_label_peak_stabil4.setObjectName("m_label_peak_stabil4")
        self.gridLayout_PeakStab.addWidget(self.m_label_peak_stabil4, 0, 1, 1, 1)
        self.m_label_peak_stabil_channel = QtWidgets.QLabel(self.groupBox_PeakStab)
        self.m_label_peak_stabil_channel.setEnabled(False)
        #self.m_label_peak_stabil_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.m_label_peak_stabil_channel.setText("0.00")
        #self.m_label_peak_stabil_channel.setObjectName("m_label_peak_stabil_channel")
        self.gridLayout_PeakStab.addWidget(self.m_label_peak_stabil_channel, 0, 2, 1, 1)

        self.layout.addWidget(self.groupBox_PeakStab)
        self.m_pi_plotter = PeakIntegSpec()
        self.layout.addWidget(self.m_pi_plotter)
        self.m_sp_plotter = PlSpectrometer()
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

class PeakIntegSpec(PlotWidget):
    def __init__(self):
        super().__init__()
        self.setBackground('w')
        self.enableAutoRange(axis='x')
        self.setXRange(0, 1, padding=0)
        self.setYRange(-20, 100, padding=0)
        self.setMouseEnabled(x=True, y=True)
        self.setLimits(xMin=0)
        self.setLabel('left', 'Counts') 
        self.setLabel('bottom', 'Frame number')  
        self.showGrid(x=True, y=True, alpha=0.5)
        self.setTitle("Peak integrals")
        self.addLegend()

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.is_dumping = False
        self.waves_to_dump = 1
        self.dataset = np.array([0] * 1024)
        self.bins = np.array( range(0, len(self.dataset)))
        self.pen = pg.mkPen(color=(255, 0, 0))
        self.pltgraph = self.plot(self.bins, self.dataset, name="Test", pen = self.pen )


class SpectraDAQ(QObject):
    finished = pyqtSignal()
    signal_dataReady = pyqtSignal(object)
    nEntries = 10
    def __init__(self, devicesMap, isCont):
        super().__init__()
        self.devicesMap = devicesMap
        self.isContinuous = isCont

    @pyqtSlot()
    def run(self):
        self.get_spectrum(self.nEntries)
        self.finished.emit()

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