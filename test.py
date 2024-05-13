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
    QTabWidget, QToolBar, QCheckBox
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
from analitics.analitics import Analitics

from transport import api, api_param
from devices.devices import DeviceConn_MasterSlave, DevicesMap, Device, Channel, ChannelWindow, BoardsManager, BoardWindow

import numpy as np

class ConnectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.conn_window = DeviceConn_MasterSlave()
        self.tbl_devices_list = DevicesMap()        #contains info about devices
        self.chk_use_master = QCheckBox("Use master-slave configuration")
        self.chk_use_master.setChecked(True)

        self.btn_get_spectrum = QPushButton("Get spectrum")

        layout = QVBoxLayout()
        layout.addWidget(self.chk_use_master)
        self.chk_use_master.stateChanged.connect(lambda: self.show_connect())
        layout.addWidget(self.conn_window)
        layout.addWidget(self.tbl_devices_list)
        layout.addWidget(self.btn_get_spectrum)
        layout.addStretch()

        hlayout = QHBoxLayout()
        hlayout.addLayout(layout)
        #cont = QGroupBox(self)
        self.setLayout(hlayout)
        self.setMinimumSize(450,400)

        #if "Connect" button is pressed, content of devices list is updated in major widget



#change type of connection widget if checkbox is checked, currently is a placeholder
    def show_connect(self):
        if self.chk_use_master.isChecked():
            print("Will use master-slave configuration")
        else:
            print("Will not use master-slave configuration")
#add data in table for new device
    def addFullData_on_Connected(self, isConnected, uptime):
        props = Device()
        props.setIP(self.conn_window.lne_ip_edit.text())
        props.setRole(self.conn_window.cmb_role.currentText())
        props.setStatus('Undefined')
        props.setUptime(0.0)

        if isConnected:
            props.setStatus('Connected')
            props.setUptime(uptime)
        #refresh table + add new device
        self.tbl_devices_list.addData(
            self.conn_window.lne_ip_edit.text(), 
            props
        )
#for existing device, update info
    def updFullData_on_Connected(self, isConnected, uptime, devicesMap):
        props = devicesMap[self.conn_window.lne_ip_edit.text()]
        props.setRole(self.conn_window.cmb_role.currentText())

        if isConnected:
            props.setStatus('Connected')
            props.setUptime(uptime)
        #refresh table
        self.tbl_devices_list.addData(
            self.conn_window.lne_ip_edit.text(), 
            props
        )

class MainWindow(QMainWindow):
    signal_dump_wave     = pyqtSignal(object, object, object)
    signal_dump_spec     = pyqtSignal(object, object, object)

    def __init__(self):
        super().__init__()
        self.initUI()

        self.transport_param = {'comname':'', 'speed':'', 'stopbits':'', 'ip':'', 'user':'', 'password':'', 'transport':2, 'port':5000}
        self.daq_cont = {'runned':False, 'need_reset':True, 'dumping_wave':False}
        self.settings = {'ip':'192.168.0.20', 'port':5000}

        self.board_thread = QThread()
        self.board = api.api(self.daq_cont, self.transport_param, False, False)
        self.board.moveToThread(self.board_thread)

        self.oscope_widget.signal_dump_wave.connect(self.slot_dump_wave)
        self.signal_dump_wave.connect(self.board.dump_wave)
        self.oscope_widget.signal_dump_wave_stop.connect(self.slot_dump_wave_done)
        self.board.signal_upd_wave.connect(self.oscope_widget.slot_on_wave_update)

        self.cwidget.conn_window.btn_connect.clicked.connect(lambda: self.connectDevice(self.cwidget.conn_window))
        self.cwidget.conn_window.btn_delete.clicked.connect(lambda: self.removeDevice(self.cwidget.conn_window))

        self.board_thread.start() 

        self.thr_daq_widget = QThread()
        self.worker = SpectraDAQ(self.devicesMap, True)
        self.worker.moveToThread(self.thr_daq_widget)

        self.worker.signal_dataReady.connect(lambda devicesMap, useSum=True: self.m_sumSpectrometer.slot_on_spec_update(devicesMap, useSum))
        self.worker.signal_dataReady.connect(lambda devicesMap, useSum=False: self.m_specWidget.slot_on_spec_update(devicesMap, useSum))
        self.worker.finished.connect(self.thr_daq_widget.terminate)

        self.thr_daq_widget.started.connect(self.worker.run)
        self.cwidget.btn_get_spectrum.clicked.connect(self.thr_daq_widget.start)        

    def slot_dump_wave_done(self):
        self.daq_cont['dumping_wave'] = False 

    def slot_dump_wave(self, samples_num, waves_num, channel_id):
        self.signal_dump_wave.emit(samples_num, waves_num, channel_id)

    def slot_dump_spec(self, samples_num, waves_num):
        self.signal_dump_spec.emit(samples_num, waves_num)

    def initUI(self):
        self.setWindowTitle("Multi-channel spectrometer")
        self.cwidget = ConnectionWidget()

        win_lyout = QVBoxLayout()

        self.boards_mgr = BoardsManager()
        self.devicesMap = self.cwidget.tbl_devices_list.devicesMap #!!!connect DeviceMap from table to main container

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
            self.cwidget.addFullData_on_Connected(self.board.check_connect(), uptime_seconds)
        else:
            self.cwidget.updFullData_on_Connected(self.board.check_connect(), uptime_seconds, self.devicesMap)

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

