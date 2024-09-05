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

from .spmeter_base import Spectrometer, PeakTrends, PeakIntegrator

class ChanSpectrometer(Spectrometer):
    name = 'ChanSpectrometer'
    signal_dataReady = pyqtSignal(object, object)
    def __init__(self):
        super().__init__()
        #self.frameTime = 1.0 #frame time = 1 s by default
        self.setupUI()

        self.btn_replot_act.clicked.connect(self.replot)

        self.devicesMap = None
        self.useSum = True

    def setupUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 0, 0)

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
        self.update_plot()

    @pyqtSlot(object, object)
    def slot_on_spec_update(self, devicesMap, entry, useSum):
        self.devicesMap = devicesMap
        self.useSum = useSum
        self.m_sp_plotter.clear()

        plotIndex = 0
        for device in self.devicesMap.values():
            for chan in device.channels:
                if chan.isActive:
                    self.m_sp_plotter.plot(self.m_sp_plotter.bins, np.array(chan.data), pen = pg.mkPen(\
                        color = self.m_sp_plotter.clr_cycle[plotIndex], width=2), name=chan.name)
                plotIndex += 1
        self.lbl_entries.setText("{0} frames".format(entry))
        self.btn_replot_act.setEnabled(True)

    def update_plot(self):
        self.m_sp_plotter.clear()

        plotIndex = 0
        for device in self.devicesMap.values():
            for chan in device.channels:
                if chan.isActive:
                    self.m_sp_plotter.plot(self.m_sp_plotter.bins, np.array(chan.data), pen = pg.mkPen(\
                        color = self.m_sp_plotter.clr_cycle[plotIndex], width=2), name=chan.name)
                plotIndex += 1


class SumSpectrometer(Spectrometer):
    name = 'SumSpectrometer'
    signal_dataReady = pyqtSignal(object, object)
    def __init__(self):
        super().__init__()
        self.m_sp_plotter.addROI()
        self.trends = PeakTrends()
        #self.frameTime = 1.0 #frame time = 1 s by default
        self.setupUI()

        self.devicesMap = None
        self.useSum = True

        self.trendFramesY = []
        self.trendFramesX = []

        self.btn_clear.clicked.connect(self.trends.pl_trends.clear)
        self.btn_clear.clicked.connect(self.clear_data)

        self.btn_replot_act.clicked.connect(self.replot)
        self.chk_enableTrends.stateChanged.connect(self.enableTrends)

        #ROI changing
        self.m_sp_plotter.region_peak.sigRegionChanged.connect(self.regionUpdated)
        self.trends.tabwid.tab_PeakArea.spin_peak_area_begin.sigValueChanging.connect(self.spinUpdated)
        self.trends.tabwid.tab_PeakArea.spin_peak_area_end.sigValueChanging.connect(self.spinUpdated)

    def regionUpdated(self):
        lo,hi = self.m_sp_plotter.region_peak.getRegion()
        #print (lo,hi)
        self.trends.tabwid.tab_PeakArea.spin_peak_area_begin.setValue(int(lo))
        self.trends.tabwid.tab_PeakArea.spin_peak_area_end.setValue(int(hi))
    
    def spinUpdated(self):
        rng = []
        rng.append(self.trends.tabwid.tab_PeakArea.spin_peak_area_begin.value())
        rng.append(self.trends.tabwid.tab_PeakArea.spin_peak_area_end.value())
        #print(rng)
        self.m_sp_plotter.region_peak.setRegion(rng)

    def enableTrends(self):
        if self.chk_enableTrends.isChecked():
            self.trends.setHidden(False)
        else:
            self.trends.setHidden(True)

    def setupUI(self):
        #self.btn_clear = QPushButton("Clear plot")
       # self.btn_replot_act = QPushButton("Replot only active")
        #self.btn_replot_act.setEnabled(False)
        self.chk_enableTrends = QCheckBox("Enable trends analyzer")
        self.trends.setHidden(True)

        #self.lbl_entries = QLabel("0/0 entries")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 0, 0)

        self.layout_btns = QHBoxLayout()
        self.layout_btns.addWidget(self.btn_clear)
        self.layout_btns.addWidget(self.btn_replot_act)
        self.layout_btns.addWidget(self.lbl_entries)
        self.layout_btns.addWidget(self.chk_enableTrends)

        self.layout.addLayout(self.layout_btns)
        self.layout.addWidget(self.trends)
        self.layout.addWidget(self.m_sp_plotter)
        self.setLayout(self.layout)

    @pyqtSlot(object, object)
    def slot_on_spec_update(self, devicesMap, entry, useSum):
        self.devicesMap = devicesMap
        self.useSum = useSum

        dataSum = 0
        self.m_sp_plotter.clear()
        for device in self.devicesMap.values():
            for chan in device.channels:
                if chan.isActive:
                    dataSum += np.array(chan.data)

        bins = self.m_sp_plotter.bins
        counts = np.array(dataSum)          
        if self.useSum:
            self.m_sp_plotter.plot(bins,counts, pen = self.m_sp_plotter.pen, name = "Summary spectrum")

            if (self.chk_enableTrends.isChecked()):
                self.integrator = PeakIntegrator()
                gateBegin = int(self.trends.tabwid.tab_PeakArea.spin_peak_area_begin.value())
                gateEnd = int(self.trends.tabwid.tab_PeakArea.spin_peak_area_end.value())
                self.integrator.setParams(gateBegin, gateEnd)

                try:
                    entry % 100
                except:
                    text = self.lbl_entries.text()
                    entries = re.findall(r'\d+', text)[0]
                    entry = entries
                else:
                    if (entry % 100 == 1):
                        self.trendFramesX.clear()
                        self.trendFramesY.clear()
                        self.trends.pl_trends.clear()

                self.trendFramesX.append(entry)
                try:
                    self.integrator.processData(counts)
                    print(self.integrator.integral)
                except:
                    self.trendFramesY.append(0)
                    self.trends.pl_trends.plot(self.trendFramesX, self.trendFramesY, pen=self.trends.pl_trends.pen)
                else:
                    self.m_sp_plotter.plot(self.integrator.dataX, self.integrator.bline, pen=pg.mkPen(\
                        color = "#0F0", width=2))
                    self.m_sp_plotter.label0.setFormat(self.integrator.centroid)
                    self.m_sp_plotter.plot(self.integrator.dataX, (self.integrator.bline + self.integrator.fitData), pen=pg.mkPen(\
                                    color = "#0FF", width=2))
                    self.trendFramesY.append(self.integrator.integral)
                    self.trends.pl_trends.plot(self.trendFramesX, self.trendFramesY, pen=self.trends.pl_trends.pen)
            
                self.m_sp_plotter.addItem(self.m_sp_plotter.region_peak, ignoreBounds=True)

        self.lbl_entries.setText("{0} frames".format(entry))
        self.btn_replot_act.setEnabled(True)

    def update_plot(self):
        dataSum = 0
        self.m_sp_plotter.clear()
        for device in self.devicesMap.values():
            for chan in device.channels:
                if chan.isActive:
                    dataSum += np.array(chan.data)

        bins = self.m_sp_plotter.bins
        counts = np.array(dataSum)     

        self.m_sp_plotter.plot(bins,counts, pen = self.m_sp_plotter.pen, name = "Summary spectrum")
        if (self.chk_enableTrends.isChecked()):
            self.integrator = PeakIntegrator()
            gateBegin = int(self.trends.tabwid.tab_PeakArea.spin_peak_area_begin.value())
            gateEnd = int(self.trends.tabwid.tab_PeakArea.spin_peak_area_end.value())
            self.integrator.setParams(gateBegin, gateEnd)

            try:
                self.integrator.processData(counts)
            except:
                print("Integrator exception!")
            else:
                self.m_sp_plotter.plot(self.integrator.dataX, self.integrator.bline, pen=pg.mkPen(\
                    color = "#0F0", width=2))
                self.m_sp_plotter.label0.setFormat(self.integrator.centroid)
                self.m_sp_plotter.plot(self.integrator.dataX, (self.integrator.bline + self.integrator.fitData), pen=pg.mkPen(\
                                color = "#0FF", width=2))
            self.m_sp_plotter.addItem(self.m_sp_plotter.region_peak, ignoreBounds=True)
        
    def replot(self):
        text = self.lbl_entries.text()
        entries = re.findall(r'\d+', text)[0]
        self.update_plot()

    def clear_data(self):
        self.trendFramesX.clear()
        self.trendFramesY.clear()
        self.trends.pl_trends.clear()