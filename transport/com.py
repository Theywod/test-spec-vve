"""
  Project       : Spectometer client
  Author        : Borshch Vladislav
  Contacts      : borchsh.vn@gmail.com
  Workfile      : com.py
  Description   : Low level API for COM port based transport
"""

import serial
import time
import logging
from PyQt5.QtCore import QObject, pyqtSignal

# User
from api_param import *

class com(QObject):
    signal_popup_message = pyqtSignal(str)

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def __init__(self, debug):
        super(com, self).__init__()
        self.comport = serial.Serial()
        self.logger = logging.getLogger(__name__)
        if debug:
            logging.basicConfig(format="%(asctime)s | %(name)s | %(levelname)s : %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z",
            level=logging.DEBUG)
            logging.debug("Debugging messages activated")
        else:
            logging.basicConfig(format="%(asctime)s | %(levelname)s : %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z",
            level=logging.INFO)

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def check_connect(self):
        if (self.comport):
            if (self.comport.isOpen()):
                return True
        return False

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def addr_wr(self, addr, data):
        self.logger.debug('COM writing. Address: 0x%02X, Data: 0x%02X' % (int(addr), int(data)))
        try:
            _addr = bytes([addr])
            _data = bytes([data])
            self.comport.reset_output_buffer()
            self.comport.write(_addr)
            self.comport.write(_data)
            return True
        except Exception as e:
            self.logger.error('! addr_wr error: ' + str(e))
            return False

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def addr_rd(self, addr):
        try:
            _addr = bytes([0xFF])
            _data = bytes([addr])
            self.comport.reset_output_buffer()
            self.comport.reset_input_buffer()
            self.comport.write(_addr)
            self.comport.write(_data)
            time.sleep(0.01)  # minimum
            readed = self.comport.read(size=3)
            # print('COM reading: %s' % addr)
            # if readed:
            #     print('COM readed: %s' % readed)
            self.comport.reset_input_buffer()
            readed = int.from_bytes(readed, 'big')
            readed &= 0xFF  # we need only LSB
            return readed
        except Exception as e:
            # print('! addr_rd error: ' + str(e))
            return None

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def read_data(self, samples_num, timeout, req):
        self.addr_wr(pADDR_DAQ_START, req)
        try:
            data = self.comport.read(size=samples_num)
            # for i, x in enumerate(data):
            #     if (i < 1024):
            #         print("%d: 0x%02X" % (i, x))
            return data
        except Exception as e:
            self.logger.error('read_data Exception error' + str(e))
            return False

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def connect(self, settings):
        try:
            if (self.check_connect()):
                self.disconnect()
        except Exception as e:
            self.logger.error("connect disconnection error: " + str(e))

        try:
            self.comport.port     = settings['comname']
            self.comport.baudrate = int(settings['speed'])
            self.comport.timeout  = pTIMEOUT
            self.comport.parity   = serial.PARITY_NONE
            self.comport.stopbits = int(settings['stopbits'])
            self.comport.bytesize = serial.EIGHTBITS
            self.comport.open()
            self.logger.debug("com_connect with parameters:")
            self.logger.debug(self.comport)
        except Exception as e:
            self.signal_popup_message.emit("com_connect error: " + str(e))
            self.logger.error("com_connect error: " + str(e))
            return False
        return True

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def disconnect(self):
        try:
            if (self.comport):
                self.logger.debug("Disconnect: " + str(self.comport.port))
                self.comport.flush()
                self.comport.close()
        except Exception as e:
            self.logger.error("disconnect error: " + str(e))
        return True
