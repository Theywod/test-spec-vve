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
from PyQt5.QtCore import Qt, pyqtSignal, QSettings, QObject, pyqtSlot
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QCheckBox
from pyqt_instruments import ui_data_saver
from pyqtgraph import PlotWidget

import pyqtgraph as pg

class Spectrometer(QWidget):
    name = 'Spectrometer'
    signal_dataReady = pyqtSignal(object, object)
    def __init__(self):
        super().__init__()
        self.m_sp_plotter = PlSpectrometer()
        self.trends = PeakTrends()
        self.setupUI()

        self.devicesMap = None
        self.useSum = True

        self.btn_clear.clicked.connect(self.m_sp_plotter.clear)
        self.btn_replot_act.clicked.connect(self.replot)
        self.chk_enableTrends.stateChanged.connect(self.enableTrends)

    def enableTrends(self):
        if self.chk_enableTrends.isChecked():
            self.trends.setHidden(False)
        else:
            self.trends.setHidden(True)


    def setupUI(self):
        self.btn_clear = QPushButton("Clear plot")
        self.btn_replot_act = QPushButton("Replot only active")
        self.btn_replot_act.setEnabled(False)
        self.chk_enableTrends = QCheckBox("Enable trends analyzer")
        self.trends.setHidden(True)

        self.lbl_entries = QLabel("0/0 entries")

        self.layout = QVBoxLayout()

        self.layout_btns = QHBoxLayout()
        self.layout_btns.addWidget(self.btn_clear)
        self.layout_btns.addWidget(self.btn_replot_act)
        self.layout_btns.addWidget(self.lbl_entries)
        self.layout_btns.addWidget(self.chk_enableTrends)

        self.layout.addLayout(self.layout_btns)
        self.layout.addWidget(self.trends)
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

class PeakTrends(QWidget):
    def __init__(self):
        super().__init__()
        self.pl_trends = PlTrend()
        self.trParams = TrendsParams()
        self.setupUI()


    def setupUI(self):
        self.layout = QVBoxLayout()

        # self.chk_enable = QCheckBox()
        # self.chk_enable.setText("Enable analyzer")
        #self.trParams.setEnabled(False)

        #self.layout.addWidget(self.chk_enable)
        self.layout.addWidget(self.trParams)
        self.layout.addWidget(self.pl_trends)
        self.setLayout(self.layout)
        self.setMaximumHeight(400)


class TrendsParams(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
    def setupUI(self):
        self.layout = QVBoxLayout()
        self.groupBox_PeakStab = QtWidgets.QGroupBox()
        self.groupBox_PeakStab.setTitle("Peak stabilization")
        self.gridLayout_PeakStab = QtWidgets.QGridLayout(self.groupBox_PeakStab)

        #Peak in area
        self.m_label_peak_stabil2 = QtWidgets.QLabel(self.groupBox_PeakStab)
        self.m_label_peak_stabil2.setText("Peak in area")
        self.gridLayout_PeakStab.addWidget(self.m_label_peak_stabil2, 1, 0, 1, 1)
        self.m_spin_area_to_track = QtWidgets.QSpinBox(self.groupBox_PeakStab)
        self.m_spin_area_to_track.setRange(1,3)
        self.m_spin_area_to_track.setProperty("value", 2)
        self.gridLayout_PeakStab.addWidget(self.m_spin_area_to_track, 1, 1, 1, 1)

        #Step size
        self.m_label_peak_stabil_step_size = QtWidgets.QLabel(self.groupBox_PeakStab)
        self.m_label_peak_stabil_step_size.setText("Step size")
        self.gridLayout_PeakStab.addWidget(self.m_label_peak_stabil_step_size, 2, 0, 1, 1)
        self.m_spin_peak_stabil_step_size = QtWidgets.QSpinBox(self.groupBox_PeakStab)
        self.m_spin_peak_stabil_step_size.setMinimum(1)
        self.m_spin_peak_stabil_step_size.setMaximum(32)
        self.gridLayout_PeakStab.addWidget(self.m_spin_peak_stabil_step_size, 2, 1, 1, 1)

        #Avg frames for search
        self.m_label_peak_stabil1 = QtWidgets.QLabel(self.groupBox_PeakStab)
        self.m_label_peak_stabil1.setText("Avg frames for search")
        self.gridLayout_PeakStab.addWidget(self.m_label_peak_stabil1, 1, 2, 1, 1)
        self.m_spin_compensate_avg_frames = QtWidgets.QSpinBox(self.groupBox_PeakStab)
        self.m_spin_compensate_avg_frames.setMaximum(600)
        self.m_spin_compensate_avg_frames.setProperty("value", 60)
        self.gridLayout_PeakStab.addWidget(self.m_spin_compensate_avg_frames, 1, 3, 1, 1)

        #keep on channel
        self.m_label_peak_stabil3 = QtWidgets.QLabel(self.groupBox_PeakStab)
        self.m_label_peak_stabil3.setText("keep on channel")
        self.gridLayout_PeakStab.addWidget(self.m_label_peak_stabil3, 2, 2, 1, 1)
        self.m_spin_keep_channel = QtWidgets.QSpinBox(self.groupBox_PeakStab)
        self.m_spin_keep_channel.setMaximum(1023)
        self.m_spin_keep_channel.setProperty("value", 150)
        self.gridLayout_PeakStab.addWidget(self.m_spin_keep_channel, 2, 3, 1, 1)

        #Peak found on channel
        self.m_label_peak_stabil4 = QtWidgets.QLabel(self.groupBox_PeakStab)
        self.m_label_peak_stabil4.setText("Peak found on channel")
        self.gridLayout_PeakStab.addWidget(self.m_label_peak_stabil4, 0, 1, 1, 1)
        self.m_label_peak_stabil_channel = QtWidgets.QLabel(self.groupBox_PeakStab)
        self.m_label_peak_stabil_channel.setText("0.00")
        self.gridLayout_PeakStab.addWidget(self.m_label_peak_stabil_channel, 0, 2, 1, 1)

        self.layout.addWidget(self.groupBox_PeakStab)
        self.setLayout(self.layout)
        self.setMaximumHeight(400)

class PlTrend(PlotWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.is_dumping = False
        self.waves_to_dump = 1
        self.dataset = np.array([0] * 1024)
        self.bins = np.array( range(0, len(self.dataset)))
        self.pen = pg.mkPen(color=(10, 0, 250))
        self.pltgraph = self.plot(self.bins, self.dataset, name="Test", pen = self.pen )

    def setupUI(self):
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
        #self.setFixedHeight(150)




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