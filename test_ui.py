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
        self.con_daq_wid.setMaximumWidth(450)
        self.con_daq_wid.setObjectName("con_daq_wid")
        self.con_daq_wid.setLayout(self.con_daq_lyout)

        self.win_lyout.addWidget(self.con_daq_wid)
        
        self.applayout = QtWidgets.QVBoxLayout()
        self.applayout.setContentsMargins(0, 0, 0, 0)
        self.applayout.setSpacing(0)
        self.titleBar = MyBar(self)
        self.applayout.addWidget(self.titleBar)
        self.applayout.addLayout(self.hlayout)
        
        self.centralwidget.setLayout(self.applayout)

        self.worker = SpectraDAQ(self.devicesMap, True)

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)

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

    def changeEvent(self, event):
        if event.type() == event.WindowStateChange:
            self.titleBar.windowStateChanged(self.windowState())

    def resizeEvent(self, event):
        self.titleBar.resize(self.width(), self.titleBar.height())

class MyBar(QtWidgets.QWidget):
    homeAction = None
    clickPos = None
    def __init__(self, parent):
        super(MyBar, self).__init__(parent)
        #self.setAutoFillBackground(True)
        
        #self.setBackgroundRole(QtGui.QPalette.Shadow)
        # alternatively:
        # palette = self.palette()
        # palette.setColor(palette.Window, Qt.black)
        # palette.setColor(palette.WindowText, Qt.white)
        # self.setPalette(palette)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addStretch()

        self.title = QtWidgets.QLabel("My Own Bar", self, alignment=QtCore.Qt.AlignLeft)
        self.title.setObjectName("titleBar_text")
        # if setPalette() was used above, this is not required
        #self.title.setForegroundRole(QtGui.QPalette.Light)

        style = self.style()
        ref_size = self.fontMetrics().height()
        ref_size += style.pixelMetric(style.PM_ButtonMargin) * 2
        self.setMaximumHeight(ref_size + 2)
        ref_size_w = 40
        ref_size_h = 20

        btn_size = QtCore.QSize(ref_size_w, ref_size_h)
        for target in ('min', 'normal', 'max', 'close'):
            btn = QtWidgets.QToolButton(self, focusPolicy=QtCore.Qt.NoFocus)
            layout.addWidget(btn)
            btn.setFixedSize(btn_size)

            iconType = QtGui.QIcon()
            iconType.addFile("resources/images/{}.png".format(target))
            btn.setIcon(iconType)

            if target == 'close':
                colorNormal = 'rgba(32, 34, 37, 255)'
                colorHover = 'red'
            else:
                colorNormal = 'rgba(32, 34, 37, 255)'
                colorHover = 'rgba(32, 34, 37, 255)'
            btn.setStyleSheet('''
                QToolButton {{
                    background-color: {};
                    border: none;
                }}
                QToolButton:hover {{
                    background-color: {}
                    border: none;
                }}
            '''.format(colorNormal, colorHover))

            signal = getattr(self, target + 'Clicked')
            btn.clicked.connect(signal)

            setattr(self, target + 'Button', btn)

        self.normalButton.hide()

        self.updateTitle(parent.windowTitle())
        parent.windowTitleChanged.connect(self.updateTitle)

    def updateTitle(self, title=None):
        if title is None:
            title = self.window().windowTitle()
        width = self.title.width()
        width -= self.style().pixelMetric(QtWidgets.QStyle.PM_LayoutHorizontalSpacing) * 2
        self.title.setText(self.fontMetrics().elidedText(
            title, QtCore.Qt.ElideRight, width))

    def windowStateChanged(self, state):
        self.normalButton.setVisible(state == QtCore.Qt.WindowMaximized)
        self.maxButton.setVisible(state != QtCore.Qt.WindowMaximized)

    def mousePressEvent(self, event):
        self.clickPos = event.pos()

    def mouseReleaseEvent(self, event):
        self.clickPos = None

    def mouseMoveEvent(self, event):
        if self.window().isMaximized():
            return
        if event.buttons() == QtCore.Qt.LeftButton and self.clickPos:
            pos = event.pos() - self.clickPos
            self.window().move(self.window().pos() + pos)

    """def mousePressEvent(self, event):
        self.clickPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.clickPos)
        posy = QtCore.QPoint(self.window().x() + delta.x(), self.window().y() + delta.y())
        self.window().move(posy)
        self.clickPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.clickPos = event.globalPos()"""

    def closeClicked(self):
        self.window().close()

    def maxClicked(self):
        self.window().showMaximized()

    def normalClicked(self):
        self.window().showNormal()

    def minClicked(self):
        self.window().showMinimized()

    def resizeEvent(self, event):
        self.title.resize(self.minButton.x(), self.height())
        self.updateTitle()