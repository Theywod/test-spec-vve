"""
  Project       : Spectometer client
  Author        : 
  Contacts      : 
  Workfile      : scpi.py
  Description   : Low level API for Ethernet based transport
"""

import time
import socket
import logging
import pyvisa
import struct
from PyQt5.QtCore import QObject, pyqtSignal

# User
from api_param import *

class scpi(QObject):
    signal_popup_message = pyqtSignal(str)
    attempts_max = 5
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def __init__(self, debug):
        super(scpi, self).__init__()
        self.client = None
        self.channel_id = 0

        self.logger = logging.getLogger(__name__)
        if debug:
            self.logger.setLevel(logging.DEBUG)

        self.logger.debug('__init__()')

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def check_connect(self):        
        if self.client:
            fd_ = self.client.session
            if fd_ > 0:
                return True            

        return False
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def set_timeout(self, timeout):
        if self.client:
            self.logger.debug('set_timeout = ' + str(timeout))
            self.client.settimeout = timeout
            return self.client.settimeout
        return True

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def select_channel(self, id):
        self.channel_id = id
        return True

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def write(self, addr, data):
        self.logger.debug("Writing to address: 0x%02X (%02X) channel:%d" % (addr, int(addr), self.channel_id))
        self.addr_wr(int(addr), data)

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def addr_wr(self, addr, data):
        msg = self.client.write('SP:{0}{1}:WRITE:ADDR '.format('CH',self.channel_id) + str(addr) +", "+ str(data))
        if (msg > 0):
            res = True
        else:
            res = False
        
        return res

        

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def read(self, addr):
        res = self.addr_rd(int(addr))
        return res

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def addr_rd(self, addr):
        self.logger.debug('Ethernet reading: 0x%02x' % addr)
        self.client.write('SP:{0}{1}:READ:ADDR? '.format('CH',self.channel_id) + str(addr))
        msg = self.client.read_raw()
        if (len(msg) > 0):
            res = int(msg)
        else:
            res = False
        
        return res


    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def eeprom_wr(self, channel, data):
        try:
            msg = self.client.write(SCPI_WRITE_EEPROM + str(channel) +", "+ str(data))
            if (msg[0] <= 0):                
                self.logger.error('eeprom_wr error: ' + str(msg[0]))
        except Exception as e:
            self.logger.error('eeprom_wr exception: ' + str(e))
            res = False        

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def dac_wr(self, channel, data):
        self.logger.debug('Writing DAC: 0x%02X, Data: 0x%02X' % (channel, data))
        msg = self.client.write(SCPI_WRITE_DAC + str(channel) +", "+ str(data))  
        if (msg > 0):
            res = True
        else:
            res = False
        
        return res

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    # def dac_rd(self, channel):        
    #     res = 0

    #     msg = self.transaction([CMD_READ_DAC, channel], True)                        
    #     if (msg[0] != 0):
    #         self.logger.debug("Read error DAC %02d" % channel)
    #         res = -1
    #     else:
    #         res = msg[1]
        
    #     return res

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def run_daq(self):                
        try:
            msg = self.client.write(SCPI_RUN_DAQ)                  
        except Exception as e:
            self.logger.error('run_daq() exception: ' + str(e))
            time.sleep(0.5)
            return False            
        return True
    
    def stop_daq(self):
        return True

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def read_data(self):
        '''
        Here is a reading handler for communicate with TCP server and
        convert readed data to the common data format
        '''
        try:
            # Sent start DAQ message
            size = 0
            self.logger.debug("Starting reading data")
            if not self.check_connect():
                self.logger.debug("!!!! Reconnecting TCP client !!!!")
                self.connect(self.last_settings)
            
            data = self.client.read_binary_values(datatype='I', is_big_endian=True)              
            self.logger.debug("Data length " + str(len(data)))
            
            #Ok, it's over now
            return data
        except Exception as e:
            self.logger.error('Exception read_data: ' + str(e))
            time.sleep(0.5)
        return False

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------

    def read_wave(self, samples_num, channel_id = 0):
        try:
            reply_size = samples_num*4
            size = 0
            msg = self.client.write(SCPI_WAVE_DUMP + str(channel_id) +", "+ str(samples_num))
            data = self.client.read_binary_values(datatype='i', is_big_endian=True)
            return data
        except Exception as e:
            self.logger.error('Exception read_wave: ' + str(e))
            #time.sleep(0.5)

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def connect(self, settings):
        self.logger.debug("Connecting with parameters:")
        self.logger.debug(settings)
        self.last_settings = settings
        
        try:             
            old_socket = self.client
            self.client = pyvisa.ResourceManager()
            self.client = self.client.open_resource('TCPIP::{}::{}::SOCKET'.format(settings["ip"], settings["port"]), read_termination = '\r\n')
            if (old_socket):
                old_socket.close()                
            
        except Exception as e:
            self.signal_popup_message.emit("Can`t connect to RedPitaya board %s:%d - " % (settings["ip"], settings["port"]) + str(e))
            self.logger.error("connect() exception: " + str(e))
            time.sleep(0.5)
            return False
        return True

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def transaction(self, cmd_with_params, want_reply = False):     
        if (cmd_with_params[0] == (SCPI_GET_UPTIME)):
            self.client.write(cmd_with_params[0])
            msg = self.client.read_raw()
            if (len(msg) > 0):
                res = [0,int(msg)]
            else:
                res = False

        elif (cmd_with_params[0] == SCPI_GET_DAEMON_VERSION):
            self.client.write(cmd_with_params[0])
            msg = self.client.read_raw()
            if (len(msg) > 0):
                res = [0,int(msg)]
            else:
                res = False

        elif (cmd_with_params[0] == SCPI_READ_ADC):
            self.client.write(cmd_with_params[0] + str(cmd_with_params[1]))
            msg = self.client.read_raw()
            if (len(msg) > 0):
                res = [0,int(msg)]
            else:
                res = False     

        elif (cmd_with_params[0] == SCPI_READ_TMP):
            self.client.write(cmd_with_params[0])
            msg = self.client.read_raw()
            if (len(msg) > 0):
                res = [0,int(msg)]
            else:
                res = False              
        return res         
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def disconnect(self):
        try:
            if self.client:
                self.logger.debug("disconnect() !")
                self.client.close()                
                return 
                
        except Exception as e:
            self.logger.error("disconnect error: " + str(e))
        return True

    #--------------------------------------------------------------------------------

    