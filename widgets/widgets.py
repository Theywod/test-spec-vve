'''
  Project       : Spectrometer
  Author        : chumadan
  Contacts      : dkc1@tpu.ru
  Workfile      : widgets.py
  Description   : Graphical and connection widgets for multi-channel spectrometer
'''
from PyQt5.QtWidgets import (
    QLabel,QPushButton, QWidget, 
    QVBoxLayout, QHBoxLayout, 
    QTabWidget, QToolBar, QCheckBox, QGridLayout, QLineEdit
)
from PyQt5.QtCore import (
    pyqtSignal, Qt, pyqtSlot
)

from transport import api, api_param
from devices.devices import DeviceConn_MasterSlave, DevicesMap, Device, Channel, ChannelWindow, BoardsManager, BoardWindow


class ConnectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.chk_use_master.stateChanged.connect(lambda: self.show_connect())

        self.tbl_devices_list.cellClicked.connect(self.onClicked)
        #if "Connect" button is pressed, content of devices list is updated in major widget

    def setupUI(self):
        self.conn_window = DeviceConn_MasterSlave()
        self.tbl_devices_list = DevicesMap()        #contains info about devices
        self.chk_use_master = QCheckBox("Use master-slave configuration")
        self.chk_use_master.setChecked(True)

        #self.btn_get_spectrum = QPushButton("Get spectrum")

        layout = QVBoxLayout()
        layout.addWidget(self.chk_use_master)
        layout.addWidget(self.conn_window)
        layout.addWidget(self.tbl_devices_list)
        #layout.addWidget(self.btn_get_spectrum)
        #layout.addStretch()

        #cont = QGroupBox(self)
        self.setLayout(layout)
        self.setMinimumHeight(300)
        self.setFixedWidth(450)
        
    #change type of connection widget if checkbox is checked, currently is a placeholder
    def show_connect(self):
        if self.chk_use_master.isChecked():
            print("Will use master-slave configuration")
        else:
            print("Will not use master-slave configuration")
    #add data in table for new device
    def setupData_onConnected(self, isConnected, uptime, devicesMap, exists):
        props = Device()
        if exists:
            props = devicesMap[self.conn_window.lne_ip_edit.text()]
            props.setRole(self.conn_window.cmb_role.currentText())
        else:
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
    @pyqtSlot(int, int)
    def onClicked(self, row, col):
        deviceIP = self.tbl_devices_list.cellWidget(row, 0).text()
        self.conn_window.lne_ip_edit.setText(deviceIP)

class DaqWidget(QWidget):
    def __init__(self, devicesMap):
        super().__init__()
        self.nFrames = 0

        self.setupUI()
        self.lne_single_daq_time.textChanged.connect(self.recalcTicks)
        self.lne_full_daq_time.textChanged.connect(self.recalcFrames)
        self.btn_updAcqTime.clicked.connect(self.setAcqTime)
        self.devicesMap = devicesMap
    
    def setupUI(self):
        layout = QGridLayout()
        self.lne_single_daq_time = QLineEdit()
        self.lne_single_daq_time.setText("1000")
        self.lbl_single_daq_ticks = QLabel("0")
        self.lbl_single_daq_ticks.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_single_daq_time = QLabel("Single DAQ frame time, ms:")
        self.lbl_ticks = QLabel("ticks")

        self.lne_full_daq_time = QLineEdit("100")
        self.lbl_full_daq_time = QLabel("Data acquisition time, sec:")
        self.lbl_full_daq_frames = QLabel("frames")
        self.lbl_full_daq_frames.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.lbl_frames = QLabel("frames")

        self.btn_updAcqTime = QPushButton("Send acq times")
        self.btn_get_single_spectrum = QPushButton("Get single spectrum")
        self.btn_get_full_spectrum = QPushButton("Start data acquisition")
        self.btn_interrupt = QPushButton("Stop data acquisition")

        layout.addWidget(self.lbl_single_daq_time, 0, 0, 1, 1)
        layout.addWidget(self.lne_single_daq_time, 0, 1, 1, 1)
        layout.addWidget(self.lbl_single_daq_ticks, 0, 2, 1, 1)
        layout.addWidget(self.lbl_ticks, 0, 3, 1, 1)

        layout.addWidget(self.lbl_full_daq_time, 1, 0, 1, 1)
        layout.addWidget(self.lne_full_daq_time, 1, 1, 1, 1)
        layout.addWidget(self.lbl_full_daq_frames, 1, 2, 1, 1)
        layout.addWidget(self.lbl_frames, 1, 3, 1, 1)

        layout.addWidget(self.btn_updAcqTime, 2, 0, 1, 1)
        layout.addWidget(self.btn_get_single_spectrum, 2, 1, 1, 1)
        layout.addWidget(self.btn_get_full_spectrum, 2, 2, 1, 2)
        layout.addWidget(self.btn_interrupt, 3, 1, 1, 2)
        self.recalcTicks()
        self.recalcFrames()

        self.setLayout(layout)
        self.setMinimumHeight(150)
        self.setFixedWidth(450)

    def setAcqTime(self):
        if(len(self.devicesMap.values()) > 0):
            for device in self.devicesMap.values():
                device.board.transport.client.write('*IDN?')
                print("{0}".format(device.board.transport.client.read_raw().decode('utf-8').rstrip()))
                for chan in device.channels:
                    query = "ACQusition{0}:TIMEout {1}".format(chan.number, self.lbl_single_daq_ticks.text())
                    device.board.transport.client.write(query)
        else:
            print("Devices map is empty")


    def recalcTicks(self):
        time = int(float(self.lne_single_daq_time.text())/(8e-6))
        self.lbl_single_daq_ticks.setText("{0}".format(str(time)))
        self.recalcFrames()

    def recalcFrames(self):
        self.nFrames = int(float(self.lne_full_daq_time.text())*1000/float(self.lne_single_daq_time.text()))
        self.lbl_full_daq_frames.setText(str(self.nFrames))
