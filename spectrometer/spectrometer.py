
import os
import time
import csv
import logging
import numpy as np
from PyQt5.QtCore import pyqtSignal, QSettings, QObject
from PyQt5 import QtWidgets
from pyqt_instruments import ui_data_saver
from pyqtgraph import PlotWidget

import pyqtgraph as pg

class Spectrometer(PlotWidget):
    clr_cycle = ['#000', '#c77', '#0f0', '#00f','#054', '#d21', '#6f0', '#712', '#912', '#a3e', '#f21', '#840']
    name = 'Spectrometer'
    signal_dump_spec = pyqtSignal(object, object, object)
    signal_dump_spec_stop = pyqtSignal()

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

    def slot_on_spec_update(self, data):
        self.dumped_waves_num += 1
                
        time = np.array( range(0, len(data)) )*8
        counts = np.array(data)
        if self.m_checkBox_autoClear.isChecked():
            self.m_plot_oscilloscope.clear()            
        self.m_plot_oscilloscope.plot(time, counts, pen = pg.mkPen('y', width=2))
        print("Spectrum dumped")
        
        self.waves_to_dump = self.waves_to_dump - 1
        if self.waves_to_dump == 0:
            self.dump_end()