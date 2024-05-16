'''
  Project       : Spectrometer
  Author        : chumadan
  Contacts      : dkc1@tpu.ru
  Workfile      : devices.py
  Description   : Classes describing various objects used for multi-channel spectrometer
'''
import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, 
    QAction, QLabel, QMessageBox, 
    QTreeWidget, QSpinBox, QFileDialog, 
    QPushButton, QWidget, QVBoxLayout, QGroupBox,
    QLineEdit, QGridLayout, QTableWidget,
    QListWidget, QTableWidgetItem, QComboBox,
    QHBoxLayout, QTabWidget, QToolBar, QCheckBox, QSpacerItem, QDoubleSpinBox
)
from PyQt5.QtCore import (
    pyqtSignal, QThread, 
    QThreadPool, QSettings, 
    QEvent, Qt, pyqtSlot, QSettings
)
from PyQt5.QtGui import (
    QPixmap, QFont, QIcon
)

def conv_v_to_adc(val):
    adc_v_pp = 2
    adc_bitwidth = 2**14

    #self.adc_step = 1/8192*1000

    res = val * adc_bitwidth / adc_v_pp

    return int(res)

def conv_adc_to_v(val):
    adc_v_pp = 2
    adc_bitwidth = 2**14        
    res = adc_v_pp * val / adc_bitwidth

    return res


#Roles: master/slave
class RolesList(QComboBox):
    def __init__(self):
        super().__init__()
        self.addItems(["Master", "Slave"])


class ChannelWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        #calculates value of threshold in adc ticks
        self.lne_threshold.valueChanged.connect(lambda: self.lbl_threshold_ticks.setText(str(conv_v_to_adc(self.lne_threshold.value()))))
        self.lne_bline.valueChanged.connect(lambda: self.lbl_bline_ticks.setText(str(conv_v_to_adc(self.lne_bline.value()))))

        self.lne_bias.valueChanged.connect(lambda: self.lbl_bias.setText(str(self.lne_bias.value())))
        self.lne_ampl.valueChanged.connect(lambda: self.lbl_ampl.setText(str(self.lne_ampl.value())))

        self.setInitValues()


    def setupUI(self):
        self.channel_id = QLabel("")
        self.isChannelActive = QCheckBox("Channel is active")
        self.isChannelActive.setChecked(False)
        self.chan_number = QLabel("")

        self.grid_chProps = QGridLayout()

        #threshold settings
        self.lbl_threshold_capt = QLabel("Threshold value")
        self.lne_threshold = QDoubleSpinBox()
        self.lne_threshold.setSingleStep(1e-3)
        self.lne_threshold.setDecimals(3)
        self.lbl_threshold_ticks = QLabel("0")
        self.chk_hyst = QCheckBox("Enable hystheresis")
        self.lbl_pretrig = QLabel("Pretrigger, bins")
        self.lne_pretrig = QSpinBox()
        self.lne_pretrig.setRange(0,255)
        #gate settings
        self.lbl_gate_start = QLabel("Gate start, bins")
        self.lne_gate_start = QSpinBox()
        self.lne_gate_start.setRange(0,255)
        self.lbl_gate_end = QLabel("Gate end, bins")
        self.lne_gate_end = QSpinBox()
        self.lne_gate_end.setRange(0,255)
        self.lbl_movavg = QLabel("Moving average, bins")
        self.lne_gate_movavg = QSpinBox()
        self.lne_gate_movavg.setRange(0,255)
        #baseline settings
        self.lbl_bline = QLabel("Baseline value")
        self.lne_bline = QDoubleSpinBox()
        self.lne_bline.setSingleStep(1e-3)
        self.lne_bline.setDecimals(3)
        self.lbl_bline_ticks = QLabel("0")
        #if shield is connected, set bias voltage and amplification
            #bias
        self.lbl_bias_capt = QLabel("Bias voltage, ticks")
        self.lne_bias = QSpinBox()
        self.lne_bias.setRange(0,255)
        self.lbl_bias = QLabel("0")
            #amplification
        self.lbl_ampl_capt = QLabel("Amplification, ticks")
        self.lne_ampl = QSpinBox()
        self.lne_ampl.setRange(0,255)
        self.lbl_ampl = QLabel("0")
        #positioning in layout
        self.grid_chProps.addWidget(self.channel_id, 0, 0, 1, 1)
        self.grid_chProps.addWidget(self.isChannelActive, 0, 1, 1, 1)
        self.grid_chProps.addWidget(self.chan_number, 0, 2, 1, 1)


        self.grid_chProps.addWidget(self.lbl_threshold_capt, 1, 0, 1, 1)
        self.grid_chProps.addWidget(self.lne_threshold, 1, 1, 1, 1)
        self.grid_chProps.addWidget(self.lbl_threshold_ticks, 1, 2, 1, 1)
        self.grid_chProps.addWidget(self.lbl_pretrig, 2, 0, 1, 1)
        self.grid_chProps.addWidget(self.lne_pretrig, 2, 1, 1, 1)
        self.grid_chProps.addWidget(self.chk_hyst, 2, 2, 1, 1)

        self.grid_chProps.addWidget(self.lbl_gate_start, 3, 0, 1, 1)
        self.grid_chProps.addWidget(self.lne_gate_start, 3, 1, 1, 1)
        self.grid_chProps.addWidget(self.lbl_gate_end, 4, 0, 1, 1)
        self.grid_chProps.addWidget(self.lne_gate_end, 4, 1, 1, 1)

        self.grid_chProps.addWidget(self.lbl_movavg, 5, 0, 1, 1)
        self.grid_chProps.addWidget(self.lne_gate_movavg, 5, 1, 1, 1)
        self.grid_chProps.addWidget(self.lbl_bline, 6, 0, 1, 1)
        self.grid_chProps.addWidget(self.lne_bline, 6, 1, 1, 1)
        self.grid_chProps.addWidget(self.lbl_bline_ticks, 6, 2, 1, 1)

        self.grid_chProps.addWidget(self.lbl_bias_capt, 7, 0, 1, 1)
        self.grid_chProps.addWidget(self.lne_bias, 7, 1, 1, 1)
        self.grid_chProps.addWidget(self.lbl_bias, 7, 2, 1, 1)
        self.grid_chProps.addWidget(self.lbl_ampl_capt, 8, 0, 1, 1)
        self.grid_chProps.addWidget(self.lne_ampl, 8, 1, 1, 1)
        self.grid_chProps.addWidget(self.lbl_ampl, 8, 2, 1, 1)


        layout = QVBoxLayout(self)
        layout.addLayout(self.grid_chProps)
        layout.addStretch()

        self.setLayout(layout)

    def updUI(self, channel):
        self.isChannelActive.setChecked(channel.isActive)

    def setInitValues(self):
        self.lne_threshold.setValue(conv_adc_to_v(250))
        self.lne_threshold.valueChanged.emit(self.lne_threshold.value())
        self.lne_bline.setValue(conv_adc_to_v(0))
        self.lne_bline.valueChanged.emit(self.lne_bline.value())
        self.lne_gate_start.setValue(0)
        self.lne_gate_end.setValue(128)
        self.lne_pretrig.setValue(0)
        self.lne_gate_movavg.setValue(3)
        self.lne_bias.setValue(100)
        self.lne_bias.valueChanged.emit(self.lne_bias.value())
        self.lne_ampl.setValue(100)
        self.lne_ampl.valueChanged.emit(self.lne_ampl.value())


class BoardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.board_ip = QLabel("")
        self.channels_tab = QTabWidget()
        self.btn_sendData = QPushButton("Send data to board")
        self.btn_loadData = QPushButton("Load from INI")


        layout = QVBoxLayout(self)
        #layout.addWidget(self.board_ip)
        layout.addWidget(self.channels_tab)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.btn_sendData)
        hlayout.addWidget(self.btn_loadData)
        layout.addLayout(hlayout)

        self.setLayout(layout)
        self.setEnabled(True)

#container for device tabs
class BoardsManager(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(350)
        self.setFixedWidth(450)
        self.setEnabled(True)


#Channel of board: its number, should we use its data, data container,
#name to be used as label in main window, tab
class Channel:
    def __init__(self):
        self.number = 0
        self.isActive = True
        self.data = [0] * 1024
        self.name = ""
        self.channelTab = None
    def change_name(self, name):
        self.name = name
    def changeStatus(self, status):
        self.isActive = status
        print("Current status: {0}".format(self.isActive))
    def updUI(self):
        self.channelTab.isChannelActive.setChecked(self.isActive)
        self.channelTab.chan_number.setText("On board chan. No. {0}".format(self.number))
    def connectActive(self):
        isChecked = self.channelTab.isChannelActive.isChecked
        self.channelTab.isChannelActive.stateChanged.connect(lambda: self.changeStatus(isChecked()))

class ChanParams:
    def __init__(self):
            self.threshold = "0"
            self.pretrigger = "0"
            self.gate_begin = "0"
            self.gate_end = "0"
            self.movaver_bypass = 0
            self.movaver_win = "0"
            self.bline = "0"
            self.hystChecked = 0

    def getValuesLines(self, chan):
        self.threshold = chan.channelTab.lbl_threshold_ticks.text()
        self.pretrigger = chan.channelTab.lne_pretrig.text()
        self.gate_begin = chan.channelTab.lne_gate_start.text()
        self.gate_end = chan.channelTab.lne_gate_end.text()
        self.movaver_bypass = 0
        self.movaver_win = chan.channelTab.lne_gate_movavg.text()
        self.bline = chan.channelTab.lbl_bline_ticks.text()
        self.hystChecked = int(chan.channelTab.chk_hyst.checkState()/2)

    def getValuesIni(self, ini_sets, ip, chan):
        ini_sets.beginGroup(ip)
        ini_sets.beginGroup(str(chan))
        print(ini_sets.allKeys())

        print("{0} - {1}".format(chan, ini_sets.value("threshold")))
        self.threshold = ini_sets.value("threshold")
        self.pretrigger = ini_sets.value("pretrigger")
        self.gate_begin = ini_sets.value("gate_begin")
        self.gate_end = ini_sets.value("gate_end")
        self.movaver_bypass = 0
        self.movaver_win = ini_sets.value("movaver_win")
        self.bline = ini_sets.value("bline")
        self.hystChecked = int(ini_sets.value("hystChecked"))
        ini_sets.endGroup()
        ini_sets.endGroup()
        
        

#Device describes specific board with its IP address, current role, connection status,
#uptime, connection port, its instance in memory after connection, number of channels
# and list of Channel instances, tab widget
class Device:
    def __init__(self):
        self.ip = '192.168.0.20'
        self.role = "Slave"
        self.status = 'Not connected'
        self.uptime = 0.0
        self.port = '5000'
        self.board = None
        self.nChannels = 0
        self.channels = []
        self.deviceTab = None
        self.ini_sets = QSettings("devices.ini", QSettings.IniFormat)
        self.params = ChanParams()

    def setIP(self, ip):
        self.ip = ip
    def setRole(self, role):
        self.role = role
    def setStatus(self, status):
        self.status = status
    def setUptime(self, uptime):
        self.uptime = uptime
    
    #when our device is recognized by system and its tab widget is created, make connections to deal with data from widget
    def updTab(self, value):
        self.deviceTab = value
        self.deviceTab.btn_sendData.clicked.connect(self.sendData)
        self.deviceTab.btn_loadData.clicked.connect(self.getData)

    def getData(self):
        self.settings = {'ip':'127.0.0.1', 'port':5000}
        self.settings['ip'] = self.ip
        self.board.connect(self.settings)
        self.board.transport.client.write('*IDN?')
        print("Connected with device {0}: {1}".format(self.ip, \
                self.board.transport.client.read_raw().decode('utf-8').rstrip()))

        for chan in self.channels:
            self.params.getValuesIni(self.ini_sets, self.ip, str(chan.number))
            chan.channelTab.lne_threshold.setValue(conv_adc_to_v(int(self.params.threshold)))
            chan.channelTab.lne_pretrig.setValue(int(self.params.pretrigger))
            chan.channelTab.lne_gate_start.setValue(int(self.params.gate_begin))
            chan.channelTab.lne_gate_end.setValue(int(self.params.gate_end))
            self.params.movaver_bypass = 0
            chan.channelTab.lne_gate_movavg.setValue(int(self.params.movaver_win))
            chan.channelTab.lne_bline.setValue(conv_adc_to_v(int(self.params.bline)))
            hystChecked = False
            if self.params.hystChecked == 1:
                hystChecked = True
            else:
                hystChecked = False 
            chan.channelTab.chk_hyst.setChecked(hystChecked)


    def sendData(self):
        self.settings = {'ip':'127.0.0.1', 'port':5000}
        self.settings['ip'] = self.ip
        self.board.connect(self.settings)
        self.board.transport.client.write('*IDN?')
        print("Connected with device {0}: {1}".format(self.ip, \
                self.board.transport.client.read_raw().decode('utf-8').rstrip()))
        self.ini_sets.beginGroup(self.ip)

        for chan in self.channels:
            self.ini_sets.beginGroup(str(chan.number))
            self.params.getValuesLines(chan)

            query = "GATE{0}:THR {1}".format(chan.number, self.params.threshold)
            self.board.transport.client.write(query)
            self.ini_sets.setValue("threshold", self.params.threshold)
            print("Threshold: {0}".format(self.params.threshold))

            query = "GATE{0}:PRETRIG {1}".format(chan.number, self.params.pretrigger)
            self.board.transport.client.write(query)
            self.ini_sets.setValue("pretrigger", self.params.pretrigger)
            print("Pretrigger: {0}".format(self.params.pretrigger))

            query = "GATE{0} {1},{2}".format(chan.number, self.params.gate_begin,\
                                             self.params.gate_end)
            self.board.transport.client.write(query)
            self.ini_sets.setValue("gate_begin", self.params.gate_begin)
            self.ini_sets.setValue("gate_end", self.params.gate_end)
            print("Gate start: {0}".format(self.params.gate_begin))
            print("Gate end: {0}".format(self.params.gate_end))

            query = "ACQ{0}:MOVAVER:BYPASS {1}".format(chan.number, self.params.movaver_bypass)   
            self.board.transport.client.write(query)
            query = "ACQ{0}:MOVAVER:WIN {1}".format(chan.number, self.params.movaver_win)   
            self.board.transport.client.write(query)
            self.ini_sets.setValue("movaver_bypass", self.params.movaver_bypass)
            self.ini_sets.setValue("movaver_win", self.params.movaver_win)
            print("Moving avg: {0}".format(self.params.movaver_win))

            query = "GATE{0}:BASELINE {1}".format(chan.number,self.params.bline)  
            self.board.transport.client.write(query) 
            self.ini_sets.setValue("bline", self.params.bline)          
            print("Baseline: {0}".format(self.params.bline))

            query = "GATE{0}:HYST {1}".format(chan.number, self.params.hystChecked)
            self.board.transport.client.write(query)   
            self.ini_sets.setValue("hystChecked", self.params.hystChecked)              
            print("Check state:{0}".format(self.params.hystChecked))  
            self.ini_sets.endGroup()
        self.ini_sets.endGroup()



#Basic widget for connection to single device
#contains line for device IP, connection and deletion buttons
class DeviceConn(QWidget):
    def __init__(self):
        super().__init__()
        self.isTableDevices = False

        self.properties = Device()

        lbl_ip_info = QLabel("Device IP & port")
        self.lne_ip_edit = QLineEdit()
        self.lne_ip_edit.setInputMask('000.000.000.000;_')
        self.lne_ip_edit.setText(self.properties.ip)
        self.lne_port_edit = QLineEdit()
        self.lne_port_edit.setText(self.properties.port)

        self.lbl_status = QLabel(self.properties.status)
        self.lbl_uptime = QLabel('Uptime: 0.0 hrs')

        self.btn_connect = QPushButton("Connect")

        self.ly_box = QGridLayout()
        self.ly_box.addWidget(lbl_ip_info, 0, 0, 1, 1)
        self.ly_box.addWidget(self.lne_ip_edit, 0, 1, 1, 1)
        self.ly_box.addWidget(self.lne_port_edit, 0, 2, 1, 1)

        self.ly_box.addWidget(self.lbl_status, 2,0, 1,1)
        self.ly_box.addWidget(self.lbl_uptime, 2,1,1,1)
        self.ly_box.addWidget(self.btn_connect, 1,1,1,1)

        self.setLayout(self.ly_box)
        self.setFixedSize(400,100)   

        self.updUI()

#after Connect button is pressed, updates uptime and status of 
#device and shows it on the widget
    def setValuesAfterConnection(self, uptime, connStatus):
        if connStatus:
            self.properties.uptime = uptime
            self.properties.status = 'Connected'
        else:
            self.properties.uptime = 0.0
            self.properties.status = 'Not connected'
        self.updUI()
    
    def updUI(self):
        self.lbl_uptime.setText('Uptime: {:10.3f} hrs'.format(self.properties.uptime/3600))
        self.lbl_status.setText(self.properties.status)

#widget for connection to device taking into account master/slave configuration
class DeviceConn_MasterSlave(DeviceConn):
    def __init__(self):
        super().__init__()

        self.isTableDevices = True
        self.cmb_role = RolesList()
        self.cmb_role.setCurrentIndex(1)

        self.btn_delete = QPushButton("Delete")

        self.ly_box.addWidget(self.cmb_role, 1,0, 1, 1)
        self.ly_box.addWidget(self.btn_delete, 1,2, 1, 1)

        self.setLayout(self.ly_box)
        self.setFixedSize(400,100)  

    #create signal on connection established that fills the table  

#container (map or dict) for connected devices
class DevicesMap(QTableWidget):
    devicesMap = dict()
    def __init__(self):
        super().__init__()
        self.initUI()
 

    def initUI(self):
        self.setColumnCount(4)
        self.setRowCount(len(self.devicesMap))

        self.setHorizontalHeaderLabels([
            "Device IP", "Role", "Status", "Uptime"
        ])
        for item in range (0, self.rowCount()):
            list_roles = QLabel("Undefined")
            line_ip_device_tbl = QLabel('000.000.000.000;_')
            self.setCellWidget(item, 0, line_ip_device_tbl)
            self.setCellWidget(item, 1, list_roles)

#updates UI redrawing it fow all the dictionary entries
    def updUI(self):
        self.setRowCount(len(self.devicesMap))
        for index, (ip, props) in enumerate(self.devicesMap.items()):
            list_roles = QLabel(props.role)
            line_ip_device_tbl = QLabel(props.ip)
            list_status = QLabel(props.status)
            line_uptime = QLabel('{:10.3f} hrs'.format(props.uptime/3600))

            print(props.role, props.ip, props.status, str(props.uptime))

            self.setCellWidget(index, 0, line_ip_device_tbl)
            self.setCellWidget(index, 1, list_roles)
            self.setCellWidget(index, 2, list_status)
            self.setCellWidget(index, 3, line_uptime)


#add info about device in container
    def addData(self, ip, devProps):
        #only one master can be connected
        if devProps.role == "Master":
            for k in self.devicesMap:
                prop = Device()
                prop.ip = k
                prop.role = "Slave"
                prop.status = self.devicesMap[k].status
                prop.uptime = self.devicesMap[k].uptime
                self.devicesMap.update({k: prop})
        self.devicesMap.update({ip: devProps})
        self.updUI()

    def removeData(self, ip):
        #only one master can be connected
        if ip in self.devicesMap:
            self.devicesMap.pop(ip)
        self.updUI()
