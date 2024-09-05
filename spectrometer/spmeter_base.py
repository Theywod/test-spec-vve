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
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QSettings, QObject, pyqtSlot
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QCheckBox, QTabWidget, QSpacerItem
from pyqt_instruments import ui_data_saver
from pyqtgraph import PlotWidget
from PyQt5.QtGui import QFont

import pyqtgraph as pg

from pybaselines import Baseline, utils
from scipy.optimize import curve_fit
import numpy as np

def gauss(x: np.ndarray, a: float, mu: float, sigma: float, b: float) -> np.ndarray:
    return (a/sigma/np.sqrt(2*np.pi))*np.exp(-0.5 * ((x-mu)/sigma)**2) + b

class PeakIntegrator(QObject):
    def __init__(self):
        self.gateBegin = 0
        self.gateEnd = 200

        self.lam = 5e7
        self.tol = 1e-7
        self.max_iter = 50
        self.dataX = [0] * 1024

    def setParams(self, gateBegin, gateEnd):
        self.gateBegin = gateBegin
        self.gateEnd = gateEnd
        self.dataX = np.arange(self.gateBegin, self.gateEnd, 1)

    def processData(self, data):
        self.dataFull = np.arange(0, 1024, 1)
        baseline_fitter = Baseline(x_data=self.dataFull)
        dataChunk = data[self.gateBegin:self.gateEnd]

        raw_bline, params = baseline_fitter.modpoly(data, poly_order=3, use_original=True)

        # self.bline, params_1 = baseline_fitter.aspls(dataChunk, lam=self.lam,\
        #                                 tol=self.tol, max_iter=self.max_iter)
        self.bline = raw_bline[self.gateBegin:self.gateEnd]
        dataCorrected = dataChunk - self.bline
        dataCenter = (self.gateBegin + self.gateEnd) / 2
        dataWidth = (self.gateBegin - self.gateEnd) / 2
        popt, pcov = curve_fit(gauss, self.dataX, dataCorrected, p0 = [2e4,dataCenter, dataWidth, 0.0],\
                       bounds=((-np.inf, -100, -np.inf, -1e-9), (np.inf, np.inf, np.inf, 0)))
        self.fitData = gauss(self.dataX,*popt)
        self.centroid = str(int(popt[1]))
        print("Center: {0}".format(self.centroid))
        self.integral = np.sum(self.fitData)
        print("Integral: {0}".format(self.integral))

class Spectrometer(QWidget):
    name = 'Spectrometer'
    signal_dataReady = pyqtSignal(object, object)
    def __init__(self):
        super().__init__()
        self.m_sp_plotter = PlSpectrometer()
        self.m_sp_plotter.setObjectName("m_sp_plotter")

        #self.frameTime = 1.0 #frame time = 1 s by default
        
        self.btn_clear = QPushButton("Clear plot")
        self.btn_replot_act = QPushButton("Replot only active")
        self.btn_replot_act.setEnabled(False)

        self.lbl_entries = QLabel("0/0 entries")

        self.devicesMap = None
        self.useSum = True

        self.btn_clear.clicked.connect(self.m_sp_plotter.clear)

class PlSpectrometer(PlotWidget):
    clr_cycle = ['#c77', '#0f0', '#00f','#054', '#d21', '#6c5', '#712', '#912', '#a3e', '#f21', '#840']

    def __init__(self):
        super().__init__()

        self.setBackground(None)
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

    def addROI(self):
        #ROI
        self.region_peak = pg.LinearRegionItem(brush=(50,50,200,25), values=[0, 1023], bounds=[0, 1023])
        self.label0 = pg.InfLineLabel(self.region_peak.lines[1], "None", position=0.95, rotateAxis=(0,0), anchor=(1, 1))
        font = QFont()
        font.setFamily("FreeMono")
        font.setPointSize(10)
        font.setBold(True)
        self.label0.setFont(font)
        self.addItem(self.region_peak, ignoreBounds=True)


class PeakTrends(QWidget):
    def __init__(self):
        super().__init__()
        self.pl_trends = PlTrend()
        self.tabwid = TabWid()
        #self.trParams = TrendsParams()
        self.setupUI()

    def setupUI(self):
        self.layout = QVBoxLayout()

        #self.layout.addWidget(self.chk_enable)
        self.layout.addWidget(self.tabwid)
        self.layout.addWidget(self.pl_trends)
        self.setLayout(self.layout)
        self.setMaximumHeight(400)

class TabWid(QTabWidget):
    def __init__(self):
        super().__init__()
        self.tab_TrendsParams = TrendsParams()
        self.tab_PeakArea = PeakArea()
        self.setupUI()

    def setupUI(self):
        self.setTabPosition(QTabWidget.North)
        self.addTab(self.tab_PeakArea, "Peak area")
        self.addTab(self.tab_TrendsParams, "Spectrum info")

class TrendsParams(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
    def setupUI(self):
        self.layout = QVBoxLayout()
        self.groupBox_PeakStab = QtWidgets.QGroupBox()
        #self.groupBox_PeakStab.setTitle("Peak stabilization")
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

class PeakArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
    def setupUI(self):
        self.layout = QVBoxLayout()
        self.groupBox_PeakArea = QtWidgets.QGroupBox()
        self.gridLayout_PeakArea = QtWidgets.QGridLayout(self.groupBox_PeakArea)

        #Peak area
        self.label_peak_area = QtWidgets.QLabel(self.groupBox_PeakArea)
        self.label_peak_area.setText("Peak area")
        self.label_peak_area.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.gridLayout_PeakArea.addWidget(self.label_peak_area, 0, 0, 1, 1)
            #begin
        #self.spin_peak_area_begin = QtWidgets.QSpinBox(self.groupBox_PeakArea)
        self.spin_peak_area_begin = pg.SpinBox(self.groupBox_PeakArea)
        self.spin_peak_area_begin.setRange(0,1023)
        self.spin_peak_area_begin.setProperty("value", 0)
        self.spin_peak_area_begin.setOpts(step = 1)
        self.gridLayout_PeakArea.addWidget(self.spin_peak_area_begin, 0, 1, 1, 1)
            #end
        #self.spin_peak_area_end = QtWidgets.QSpinBox(self.groupBox_PeakArea)
        self.spin_peak_area_end = pg.SpinBox(self.groupBox_PeakArea)
        self.spin_peak_area_end.setRange(0,1023)
        self.spin_peak_area_end.setProperty("value", 1023)
        self.spin_peak_area_end.setOpts(step = 1)
        self.gridLayout_PeakArea.addWidget(self.spin_peak_area_end, 0, 2, 1, 1)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.spin_peak_area_begin.setSizePolicy(sizePolicy)
        self.spin_peak_area_begin.setMinimumSize(QtCore.QSize(25, 25))
        
        self.spin_peak_area_end.setSizePolicy(sizePolicy)
        self.spin_peak_area_end.setMinimumSize(QtCore.QSize(25, 25))

        self.layout.addWidget(self.groupBox_PeakArea)
        self.setLayout(self.layout)
        self.setMaximumHeight(400)
        #self.setMaximumWidth(400)

class PlTrend(PlotWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.is_dumping = False
        self.waves_to_dump = 1
        self.dataset = np.array([0] * 1)
        self.bins = np.array( range(0, len(self.dataset)))
        self.pen = pg.mkPen(color=(10, 0, 250))
        self.pltgraph = self.plot(self.bins, self.dataset, name="Test", pen = self.pen )

    def setupUI(self):
        self.setBackground('w')
        self.setXRange(0, 1, padding=0)
        self.setYRange(-20, 100, padding=0)
        self.enableAutoRange(axis='x')
        self.enableAutoRange(axis='y')
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
        self.settings = {'ip':'192.168.0.20', 'port':5000}
        for entry in range(nEntries):
            nCountsPerSecondTotal = 0
            for device in self.devicesMap.values():
                self.settings["ip"] = device.ip
                device.board.connect(self.settings)
                device.board.transport.client.write('SPEC?')             #query spectra

                data.update({device.ip: device.board.transport.read_data()})  #get spectra from device
                #for each channel data length is 1024 bytes + 3 bytes per channel + 6 ending bytes after the whole data array
                #data is within ranges nChannel*1027 : nChannel*1027 + 1024
                #or nChannel*1027 : (nChannel+1)*1027 - 3
                nActiveChannels = int(((len(data[device.ip]) - 6)/1027))
                for chan in range(0, nActiveChannels):
                    dataChunk = data[device.ip][chan*1027:(chan+1)*1027-3]
                    chanIntegral = np.sum(dataChunk)    #calculate number of events per frame for each channel
                    nCountsPerSecondTotal += chanIntegral
                    print("Channel {0} CPF: {1}".format(device.channels[chan].name, chanIntegral))
                    if self.isContinuous:
                        device.channels[chan].data = np.add(device.channels[chan].data, dataChunk)
                    else:
                        device.channels[chan].data = dataChunk
            print("Total CPF: {0}".format(nCountsPerSecondTotal))
            self.signal_dataReady.emit(self.devicesMap, (entry+1))

            if self.setStop:                          
                self.setStop = False
                break