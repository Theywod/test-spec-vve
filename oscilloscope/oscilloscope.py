"""
  Project       : Spectrometer Analitics Module
  Author        : CSG
  Contacts      : csg@tpu.ru
  Workfile      : oscilloscope.py
  Description   : Class for oscilloscope
"""

if __debug__ is True:
    import oscilloscope.oscilloscope_convert_ui as oscilloscope_convert_ui
    oscilloscope_convert_ui.convert_package_ui()

import os
import time
import csv
import logging
import numpy as np
from PyQt5.QtCore import pyqtSignal, QSettings, QObject
from PyQt5 import QtWidgets
from pyqt_instruments import ui_data_saver

from .forms.waveform import Ui_WaveformWidget
import pyqtgraph as pg

class OscilloscopeW(QtWidgets.QWidget, Ui_WaveformWidget):
    name = 'Oscilloscope'
    signal_dump_wave = pyqtSignal(object, object, object)
    signal_dump_wave_stop = pyqtSignal()

    def __init__(self, *args, obj=None, **kwargs):
        super(QtWidgets.QWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.m_push_get_wave.clicked.connect(self.slot_on_getwave_pressed)
        self.m_check_wave_repeat.stateChanged.connect(self.slot_on_wave_repeat)
        self.m_push_clear.clicked.connect(self.slot_on_clear_plot)
        self.m_checkBox_saveToFile.stateChanged.connect(self.slot_on_save_to_file)

        #self.m_plot_oscilloscope.setXRange(0, 1, padding=0)
        #self.m_plot_oscilloscope.setYRange(-20, 100, padding=0)
        self.m_plot_oscilloscope.setMouseEnabled(x=True, y=True)
        self.m_plot_oscilloscope.setLimits(xMin=0)
        self.m_plot_oscilloscope.setLabel('left', 'U, mV')
        self.m_plot_oscilloscope.setLabel('bottom', 'Time, ns')        
        
        self.m_plot_oscilloscope.showGrid(x=True, y=True, alpha=0.5)
        self.m_plot_oscilloscope.setTitle("Wave form")
        #self.pl_trends.setAutoVisible(x=False, y=False)
        self.m_plot_oscilloscope.addLegend()
        
        self.adc_step = 1/8192*1000
        self.is_dumping = False
        self.waves_to_dump = 1
        self.get_wave_text = self.m_push_get_wave.text()
        self.dumped_waves_num = 0
        
        self.pf = object()
        self.csv_writer_waves = object()

    def slot_on_getwave_pressed(self):
        if self.is_dumping:
            self.signal_dump_wave_stop.emit()
            self.dump_end()
            return
        
        self.prepare_to_save_waves()
        
        self.dumped_waves_num = 0
        #self.m_label_dumped.setText("Dumped: " + str(self.dumped_waves_num))
        samples_num = self.m_spin_smples_num.value()
        waves_num = 1
        if self.m_check_wave_repeat.isChecked():
            waves_num = self.m_spin_repeat_waves.value()
            self.dump_begin()

        channel_id = self.m_comboBox_channel_id.currentIndex()
        self.signal_dump_wave.emit(samples_num, waves_num, channel_id)

    def slot_on_wave_update(self, wave):
        self.dumped_waves_num += 1
                
        self.m_label_dumped.setText("Dumped: " + str(self.dumped_waves_num))
        
        if self.m_checkBox_saveToFile.isChecked():
            self.csv_writer_waves.writerow(wave)            
        else:
            time = np.array( range(0, len(wave)) )*8
            volts = np.array(wave) * self.adc_step
            if self.m_checkBox_autoClear.isChecked():
                self.m_plot_oscilloscope.clear()            
            self.m_plot_oscilloscope.plot(time, volts, pen = pg.mkPen('y', width=2))
            print("Wave dumped")
        
        self.waves_to_dump = self.waves_to_dump - 1
        if self.waves_to_dump == 0:
            self.dump_end()

    def slot_on_clear_plot(self):                
        self.m_plot_oscilloscope.clear()

    def slot_on_wave_repeat(self):
        if self.m_check_wave_repeat.isChecked():
            self.m_spin_repeat_waves.setEnabled(True)
        else:
            self.m_spin_repeat_waves.setEnabled(False)

    def dump_begin(self):
        self.is_dumping = True
        self.m_push_get_wave.setText("Stop")
        self.waves_to_dump = self.m_spin_repeat_waves.value()

    def dump_end(self):
        self.is_dumping = False
        self.m_push_get_wave.setText(self.get_wave_text)
        self.pf.close()
        self.csv_writer_waves = None
        
    def prepare_to_save_waves(self):
        if self.m_checkBox_saveToFile.isChecked():
            #self.logger.debug("Saving waves to file")
            data_dir = 'data'
            if (not os.path.isdir(data_dir)):
                os.mkdir(data_dir)
            stamp = time.strftime("%Y-%m-%d_%H_%M_%S")
            filename = "waves_" + stamp + ".csv"
            self.pf = open(data_dir + '/' + filename, "w")
            self.csv_writer_waves = csv.writer(self.pf, delimiter=';', quoting=csv.QUOTE_NONE, lineterminator='\n')
            
    def slot_on_save_to_file(self):
        if self.m_checkBox_saveToFile.isChecked():
            self.m_plot_oscilloscope.setEnabled(False)
        else:
            self.m_plot_oscilloscope.setEnabled(True)

    
