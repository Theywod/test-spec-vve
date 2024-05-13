'''
  Project       : Spectrometer
  Author        : chumadan
  Contacts      : dkc1@tpu.ru
  Workfile      : test.py
  Description   : Main file for multi-channel spectrometer
'''

import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, 
    QLabel,QPushButton, QWidget, 
    QVBoxLayout, QHBoxLayout, 
    QTabWidget, QToolBar, QCheckBox, QTableWidgetItem, QGridLayout, QLineEdit
)
from PyQt5.QtCore import (
    pyqtSignal, QThread, 
    QThreadPool, QSettings, 
    QEvent, Qt, pyqtSlot
)
from PyQt5.QtGui import (
    QPixmap, QFont, QIcon
)

sys.path.append("./transport/")

import oscilloscope.oscilloscope as oscope
import spectrometer.spectrometer as spmeter

from spectrometer.spectrometer import SpectraDAQ
from widgets.widgets import ConnectionWidget, DaqWidget

from transport import api, api_param
from devices.devices import DeviceConn_MasterSlave, DevicesMap, Device, Channel, ChannelWindow, BoardsManager, BoardWindow

import numpy as np

class MainWindow(QMainWindow):
    signal_dump_wave     = pyqtSignal(object, object, object)

    def __init__(self):
        super().__init__()
        self.setupUI()

        self.transport_param = {'comname':'', 'speed':'', 'stopbits':'', 'ip':'', 'user':'', 'password':'', 'transport':2, 'port':5000}
        self.daq_cont = {'runned':False, 'need_reset':True, 'dumping_wave':False}
        self.settings = {'ip':'192.168.0.20', 'port':5000}

        self.board_thread = QThread()
        self.thr_daq = QThread()

        self.board = api.api(self.daq_cont, self.transport_param, False, False)
        self.board.moveToThread(self.board_thread)

        self.oscope_widget.signal_dump_wave.connect(self.slot_dump_wave)
        self.signal_dump_wave.connect(self.board.dump_wave)
        self.oscope_widget.signal_dump_wave_stop.connect(self.slot_dump_wave_done)
        self.board.signal_upd_wave.connect(self.oscope_widget.slot_on_wave_update)

        self.cwidget.conn_window.btn_connect.clicked.connect(lambda: self.connectDevice(self.cwidget.conn_window))
        self.cwidget.conn_window.btn_delete.clicked.connect(lambda: self.removeDevice(self.cwidget.conn_window))

        self.board_thread.start() 

        self.worker = SpectraDAQ(self.devicesMap, True)
        self.worker.moveToThread(self.thr_daq)

        self.worker.signal_dataReady.connect(lambda devicesMap, entry, useSum=True: self.m_sumSpectrometer.slot_on_spec_update(devicesMap, entry, useSum))
        self.worker.signal_dataReady.connect(lambda devicesMap, entry, useSum=False: self.m_specWidget.slot_on_spec_update(devicesMap, entry, useSum))
        self.worker.finished.connect(self.thr_daq.terminate)

        self.thr_daq.started.connect(self.worker.run)
        self.daqwidget.btn_get_single_spectrum.clicked.connect(self.get_single_spectrum)     
        self.daqwidget.btn_get_full_spectrum.clicked.connect(self.get_series_of_spectra)     
        self.daqwidget.btn_interrupt.clicked.connect(self.setStop)     
        self.m_specWidget.btn_clear.clicked.connect(self.clear_spec)
        self.m_sumSpectrometer.btn_clear.clicked.connect(self.clear_spec)

    def clear_spec(self):
        for device in self.devicesMap.values():
            for chan in device.channels:
                chan.data = [0] * 1024
                print("Data cleared")
    
    def setStop(self):
        self.worker.setStop = True

    def get_single_spectrum(self):
        self.worker.nEntries = 1
        self.thr_daq.start()

    def get_series_of_spectra(self):
        self.worker.nEntries = self.daqwidget.nFrames
        self.thr_daq.start()


    def slot_dump_wave_done(self):
        self.daq_cont['dumping_wave'] = False 

    def slot_dump_wave(self, samples_num, waves_num, channel_id):
        self.signal_dump_wave.emit(samples_num, waves_num, channel_id)

    def setupUI(self):
        self.setWindowTitle("Multi-channel spectrometer")
        self.cwidget = ConnectionWidget()

        win_lyout = QVBoxLayout()

        self.boards_mgr = BoardsManager()
        self.devicesMap = self.cwidget.tbl_devices_list.devicesMap #!!!connect DeviceMap from table to main container
        self.daqwidget = DaqWidget(self.devicesMap)


        self.oscope_widget = oscope.OscilloscopeW()
        self.m_specWidget = spmeter.Spectrometer()
        self.m_sumSpectrometer = spmeter.Spectrometer()
        
        toolbar = QToolBar("Main toolbar")
        self.addToolBar(toolbar)

        hlayout = QHBoxLayout()
        hlayout.addLayout(win_lyout)
        tabs_lyout = QTabWidget()

        tabs_lyout.addTab(self.oscope_widget, "Oscilloscope")
        tabs_lyout.addTab(self.m_specWidget, "Spectrometer")
        tabs_lyout.addTab(self.m_sumSpectrometer, "SMeter (SUM)")

        hlayout.addWidget(tabs_lyout)
        centerwidget = QWidget()
        win_lyout.addWidget(self.cwidget)
        win_lyout.addWidget(self.daqwidget)
        win_lyout.addWidget(self.boards_mgr)
        centerwidget.setLayout(hlayout)
        self.setCentralWidget(centerwidget)

    def connectDevice(self, window):
        #set connection configuration and connect to device
        self.settings["ip"] = window.lne_ip_edit.text()
        self.transport_param["ip"] = self.settings["ip"]
        self.transport_param["port"] = self.settings["port"]
        self.board.connect(self.settings)
        self.board.transport.client.timeout = 20000

        #get uptime and connection status
        uptime_seconds = self.board.transport.transaction([api_param.SCPI_GET_UPTIME], True)[1]
        window.setValuesAfterConnection(uptime_seconds, self.board.check_connect())

        #if device was noe connected previously, add it to the devices table,
        #otherwise update information in devices table
        if not self.settings["ip"] in self.devicesMap:
            self.cwidget.setupData_onConnected(self.board.check_connect(), uptime_seconds, self.devicesMap, False)
        else:
            self.cwidget.setupData_onConnected(self.board.check_connect(), uptime_seconds, self.devicesMap, True)

        isConnected = self.board.check_connect()
        print("Connection:", isConnected)

        if window.isTableDevices and isConnected:
            #fill table with connected devices
            #assign board in devices table to currently connected device
            device = self.devicesMap[self.settings["ip"]]
            if device.board == None:
                device.board = self.board
                device.board.transport.client.write('sp:channels?')
                numChannels = int(device.board.transport.client.read_raw().decode('utf-8').rstrip())
                device.nChannels = numChannels
                device.channels = [None] * numChannels

            self.buildBoardTab(device)

            for deviceIP in self.devicesMap:
                self.devicesMap[deviceIP].board.transport.client.write('*IDN?')
                print("{0}: {1}".format(deviceIP, self.devicesMap[deviceIP].board.transport.client.read_raw().decode('utf-8').rstrip()))

    def removeDevice(self, window):
        for i in range(self.boards_mgr.count()):
            if  self.boards_mgr.tabText(i) == window.lne_ip_edit.text():
                self.boards_mgr.removeTab(i)
            else:
                pass
        self.cwidget.tbl_devices_list.removeData(window.lne_ip_edit.text())

    def buildBoardTab(self, device):
        if device.deviceTab == None:
            newtab = BoardWindow()
            device.updTab(newtab)
            device.deviceTab.board_ip.setText(self.settings["ip"])
            self.boards_mgr.addTab(device.deviceTab, device.ip)

            for numCh in range(device.nChannels):
                channel = Channel()
                channelWin = ChannelWindow()

                channel.number = numCh
                channel.change_name("Ch{0}".format(channel.number))

                device.channels[numCh] = channel
                channel.channelTab = channelWin
                channelWin.isChannelActive.setChecked(device.channels[numCh].isActive)
                device.deviceTab.channels_tab.addTab(device.channels[numCh].channelTab, device.channels[numCh].name)
                device.channels[numCh].connectActive()

            self.updateChannelNames()


    def updateChannelNames(self):
        i = 0
        for device in self.devicesMap.values():
            for channel in device.channels:
                channel.change_name("Channel{0}".format(i))
                channel.channelTab.channel_id.setText(channel.name)
                device.deviceTab.channels_tab.setTabText(channel.number, channel.name)
                channel.updUI()
                i += 1

     
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

