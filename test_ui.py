'''  
  Project       : Spectrometer
  Author        : vve
  Contacts      : vve14@tpu.ru
  Workfile      : test_ui.py
  Description   : main ui file for Spectrometer client
'''

from PyQt5 import QtCore, QtGui, QtWidgets

import oscilloscope.oscilloscope as oscope
import spectrometer.spmeters as spmeters

from spectrometer.spmeter_base import SpectraDAQ
from widgets.widgets import ConnectionWidget, DaqWidget
from devices.devices import DeviceConn_MasterSlave, DevicesMap, Device, Channel, ChannelWindow, BoardsManager, BoardWindow

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        MainWindow.setContentsMargins(0, 0, 0, 0)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.win_lyout = QtWidgets.QVBoxLayout()
        self.win_lyout.setContentsMargins(0, 0, 0, 0)
        self.win_lyout.setSpacing(0)

        self.menu_lyout = QtWidgets.QVBoxLayout()
        self.menu_lyout.setObjectName("menulyout")
        self.menu_lyout.setContentsMargins(0, 0, 0, 0)
        self.menu_lyout.setSpacing(0)
        self.menu_lyout.setAlignment(QtCore.Qt.AlignTop)

        self.menu_btn_1 = QtWidgets.QPushButton()
        self.menu_btn_1.setText("")
        self.menu_btn_1.setCheckable(True)
        self.menu_btn_1.setChecked(True)
        self.menu_btn_1.setAutoExclusive(False)
        self.menu_btn_1.setObjectName("menu_btn_1")
        self.menu_btn_1.clicked.connect(self.activate_menu_1)

        self.menu_btn_2 = QtWidgets.QPushButton()
        self.menu_btn_2.setText("")
        self.menu_btn_2.setCheckable(True)
        self.menu_btn_2.setAutoExclusive(True)
        self.menu_btn_2.setObjectName("menu_btn_2")
        self.menu_btn_2.pressed.connect(self.activate_menu_2)

        self.menu_btn_3 = QtWidgets.QPushButton()
        self.menu_btn_3.setText("")
        self.menu_btn_3.setCheckable(True)
        self.menu_btn_3.setAutoExclusive(True)
        self.menu_btn_3.setObjectName("menu_btn_3")
        self.menu_btn_3.pressed.connect(self.activate_menu_3)

        self.menu_btn_4 = QtWidgets.QPushButton()
        self.menu_btn_4.setText("")
        self.menu_btn_4.setCheckable(True)
        self.menu_btn_4.setAutoExclusive(True)
        self.menu_btn_4.setObjectName("menu_btn_4")
        self.menu_btn_4.pressed.connect(self.activate_menu_4)

        self.menu_lyout.addWidget(self.menu_btn_1)
        self.menu_lyout.addWidget(self.menu_btn_2)
        self.menu_lyout.addWidget(self.menu_btn_3)
        self.menu_lyout.addWidget(self.menu_btn_4)

        #make colored background of menu
        self.color_filler = QtWidgets.QWidget()
        self.color_filler.setObjectName("menucolor")
        self.color_filler.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        self.color_filler.setMaximumWidth(50)
        self.menu_lyout.addWidget(self.color_filler)

        self.cwidget = ConnectionWidget()
        self.cwidget.setObjectName("cwidget")
        self.boards_mgr = BoardsManager()
        self.boards_mgr.setObjectName("boards_mgr")
        #self.boards_mgr.setContentsMargins(0, 0, 0, 0)
        self.boards_mgr.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.devicesMap = self.cwidget.tbl_devices_list.devicesMap #!!!connect DeviceMap from table to main container
        self.daqwidget = DaqWidget(self.devicesMap)
        self.daqwidget.setObjectName("daqwidget")

        self.oscope_widget = oscope.OscilloscopeW()
        self.m_specWidget = spmeters.ChanSpectrometer()
        self.m_specWidget.setObjectName("ChanSpectrometer")
        self.m_sumSpectrometer = spmeters.SumSpectrometer()
        self.m_sumSpectrometer.setObjectName("SumSpectrometer")

        self.hlayout = QtWidgets.QHBoxLayout()
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.hlayout.setSpacing(0)
        self.hlayout.addLayout(self.menu_lyout) # add menu with stack widget buttons
        self.hlayout.addLayout(self.win_lyout)  # add connection widgets

        self.stack_wid = QtWidgets.QStackedWidget()
        self.stack_wid.setObjectName("stack_wid")
        self.stack_wid.addWidget(self.oscope_widget)
        self.stack_wid.addWidget(self.m_specWidget)
        self.stack_wid.addWidget(self.m_sumSpectrometer)
        self.hlayout.addWidget(self.stack_wid) # add stack widget with oscope and spec

        if self.stack_wid.currentIndex() == 0:
            self.menu_btn_2.setChecked(True)
        #elif self.stack_lyout.currentIndex() == 1:
        #    self.menu_btn_3.setChecked(True)
        #elif self.stack_lyout.currentIndex() == 2:
        #    self.menu_btn_4.setChecked(True)

        self.con_daq_lyout = QtWidgets.QVBoxLayout()
        self.con_daq_lyout.setContentsMargins(0, 0, 0, 0)
        self.con_daq_lyout.setSpacing(0)
        self.con_daq_lyout.addWidget(self.cwidget)
        self.con_daq_lyout.addWidget(self.daqwidget)
        self.con_daq_lyout.addWidget(self.boards_mgr)

        self.con_daq_wid = QtWidgets.QFrame()
        self.con_daq_wid.setMaximumWidth(410)
        self.con_daq_wid.setObjectName("con_daq_wid")
        self.con_daq_wid.setLayout(self.con_daq_lyout)

        self.win_lyout.addWidget(self.con_daq_wid)
        
        self.centralwidget.setLayout(self.hlayout)

        self.worker = SpectraDAQ(self.devicesMap, True)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def activate_menu_1(self):
        hide = self.menu_btn_1.isChecked()
        self.con_daq_wid.setVisible(hide)
        self.boards_mgr.setVisible(hide)
            
    def activate_menu_2(self):
        self.stack_wid.setCurrentIndex(0)
        #print(str(self.menu_btn_2.group()))

    def activate_menu_3(self):
        self.stack_wid.setCurrentIndex(1)
        #print(self.menu_btn_3.group())

    def activate_menu_4(self):
        self.stack_wid.setCurrentIndex(2)
        #print(self.menu_btn_4.group())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MultiSpec"))
        #self.tabs_lyout.setTabText(self.tabs_lyout.indexOf(self.oscope_widget), _translate("Oscilloscope","Oscilloscope"))
        #self.tabs_lyout.setTabText(self.tabs_lyout.indexOf(self.m_specWidget), _translate("Spectrometer","Spectrometer"))
        #self.tabs_lyout.setTabText(self.tabs_lyout.indexOf(self.m_sumSpectrometer), _translate("SMeter (SUM)","Sum. Spectrum"))