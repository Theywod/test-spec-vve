"""
  Project       : Spectometer client
  Author        : Borshch Vladislav
  Contacts      : borchsh.vn@gmail.com
  Workfile      : ethernet.py
  Description   : Low level API for Ethernet based transport
"""

import time
import socket
import logging
from PyQt5.QtCore import QObject, pyqtSignal

# User
from api_param import *

class ethernet(QObject):
    signal_popup_message = pyqtSignal(str)
    attempts_max = 5
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def __init__(self, debug):
        super(ethernet, self).__init__()
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
            #self.logger.debug("check_connect() " + str(self.client.__getstate__))
            fd_ = self.client.fileno()
            #self.logger.debug("check_connect() client.fileno(): " +str(fd_))
            if fd_ > 0:
                return True            

        return False

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def set_timeout(self, timeout):
        if self.client:
            self.logger.debug('set_timeout = ' + str(timeout))
            return self.client.settimeout(timeout)
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
        tx_bytes = list(self.ints_to_bytes([addr]))
        tx_bytes[2] = self.channel_id        
        addr_with_channel = self.bytes_to_ints(tx_bytes)[0]

        self.logger.debug('addr_wr. Address: 0x%02X, Data: 0x%02X, channel: %d, raw: %s' % (addr, data, self.channel_id, addr_with_channel))        

        msg = self.transaction([CMD_ADDR_WR, addr_with_channel, data], True)        
        if (msg[0] != 0):
            res = False
        else:
            res = True
        
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
        
        msg = self.transaction([CMD_ADDR_RD, addr], True)
        if (msg[0] != 0):
            res = False
            self.logger.error('addr_rd() error: ' + str(msg[0]))
        else:
            res = msg[1]
        return res

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def eeprom_wr(self, channel, data):
        try:
            msg = self.transaction([CMD_WRITE_EEPROM, channel, data], True)
            if (msg[0] != 0):                
                self.logger.error('eeprom_wr error: ' + str(msg[0]))
        except Exception as e:
            self.logger.error('eeprom_wr exception: ' + str(e))
            res = False        

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def dac_wr(self, channel, data):
        self.logger.debug('Writing DAC: 0x%02X, Data: 0x%02X' % (channel, data))
        res = False

        msg = self.transaction([CMD_WRITE_DAC, channel, data], True)
            
        if not msg:
            return False

        if (msg[0] == 0):
            return True
            
        return res

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def dac_rd(self, channel):        
        res = 0

        msg = self.transaction([CMD_READ_DAC, channel], True)                        
        if (msg[0] != 0):
            self.logger.debug("Read error DAC %02d" % channel)
            res = -1
        else:
            res = msg[1]
        
        return res

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def run_daq(self):                
        try:
            self.transaction([CMD_RUN_DAQ])                     
        except Exception as e:
            self.logger.error('run_daq() exception: ' + str(e))
            time.sleep(0.5)
            return False            
        return True
    
    def stop_daq(self):
        try:                        
            self.transaction([CMD_STOP_DAQ])
        except Exception as e:
            self.logger.error('stop_daq exception: ' + str(e))
            time.sleep(0.5)
            return False            
        return True

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def read_data(self):
        '''
        Here is a reading handler for communicate with TCP server and
        convert readed data to the common data format
        '''
        #self.logger.debug('Start data reading')
        try:
            # Sent start DAQ message
            # self.send_msg(CMD_RUN_DAQ)

            #self.set_timeout(1)
            #self.logger.info("Timeout = " + str(self.client.timeout))
            #self.client.send(CMD_RUN_DAQ.to_bytes(VAL_SIZE, byteorder='little'))

            # Waiting for data...
            raw_data = bytearray()
            size = 0
            self.logger.debug("Starting reading data")
            if not self.check_connect():
                self.logger.debug("!!!! Reconnecting TCP client !!!!")
                self.connect(self.last_settings)
            
            while((size - INFO_SIZE) % SPECTRUM_SIZE != 0) and self.check_connect():
                # remaining_size = BUF_SIZE-size                
                raw_data.extend(self.client.recv(256))
                size = len(raw_data)
                # self.logger.debug(f"read_data(): received {str(size)} bytes, remain {str(remaining_size)}")

            # Stop DAQ message
            # self.send_msg(CMD_STOP_DAQ, 0)

            self.logger.debug("Total receive: " + str(size) + " bytes")                
            number_of_int = int(len(raw_data)/VAL_SIZE)
            data = [0 for i in range(number_of_int)]
            for i in range(number_of_int):
                data[i] = int.from_bytes(raw_data[i*VAL_SIZE:i*VAL_SIZE + VAL_SIZE-1], byteorder='little')
                        
            self.logger.debug("Data length " + str(len(data)))
            
            #col_num = 8
            #for i in range(int(len(data)/col_num)):
            #    row_shift = i*col_num                
            #    self.logger.debug("%04d: %08d %08d %08d %08d %08d %08d %08d %08d" % (row_shift, data[row_shift + 0],
            #    data[row_shift + 1], data[row_shift + 2], data[row_shift + 3], data[row_shift + 4], data[row_shift + 5], data[row_shift + 6], data[row_shift + 7]))
            #row_shift = 129*8
            #self.logger.debug("%04d: %08d" % (row_shift, data[row_shift + 0]))
            
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
            raw_data = bytearray()
            size = 0
            #self.logger.debug('Dumping waveform in %d samples (%d bytes)' % (samples_num, reply_size))
            self.transaction([CMD_DUMP_WAVE, channel_id, samples_num])
            
            read_timeout = 1.0
            time_start = time.perf_counter()
            while (size < reply_size) and self.check_connect():
                remaining_size = reply_size - size                
                raw_data.extend(self.client.recv(remaining_size))
                
                size = len(raw_data)
                #self.logger.debug("read_wave(): received " + str(size) + " bytes")
                time_current = time.perf_counter()
                if (time_current - time_start) > read_timeout:
                    self.logger.debug("read_data(): can't read data during %f sec" % (read_timeout))
                    break
                                 
            number_of_int = int(len(raw_data)/VAL_SIZE)
            data = [0 for i in range(number_of_int)]
            
            for i in range(number_of_int):
                data[i] = int.from_bytes(raw_data[i*VAL_SIZE:i*VAL_SIZE + VAL_SIZE-1], byteorder='little', signed=True)
                        
            #self.logger.debug("Data length " + str(len(data)))            
                        
            return data
        except Exception as e:
            self.logger.error('Exception read_wave: ' + str(e))
            time.sleep(0.5)

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def connect(self, settings):
        self.logger.debug("Connecting with parameters:")
        self.logger.debug(settings)
        self.last_settings = settings
        try:            
            old_socket = self.client
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(1)
            self.client.connect((settings["ip"], settings["port"]))            
            self.client.settimeout(None)
            #self.logger.debug('Clients Socket address: ' + hex(id(self.client)))
            #self.logger.debug('Clients OldSocket address: ' + hex(id(old_socket)))
            if (old_socket):
                old_socket.close()                
            #self.logger.debug('Clients OldSocket address: ' + hex(id(old_socket)))
            
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
        res = False
        attempts = 0
        while (not res) and (attempts < self.attempts_max):            
            try:
                self.send_msg(cmd_with_params)                
                if want_reply:
                    res = self.read_msg()
                    return res
                res = True             
            except Exception as e:
                self.logger.error('transaction() exception: ' + str(e))
                self.logger.debug("Attempt:" + str(attempts) + " res=" + str(res))
                attempts += 1

        return res

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------

    def send_msg(self, cmd_with_params):
        msg = [0 for i in range(MSG_SIZE)]
        for i in range(len(cmd_with_params)):
            msg[i] = cmd_with_params[i]
        
        self.logger.debug("send_msg() " + str(msg))
        
        res = False
        attempts = 0
        while (not res) and (attempts < self.attempts_max):            
            try:                                
                #raw_stream = b''.join([x.to_bytes(4, byteorder='little', signed=True) for x in msg])
                raw_stream = self.ints_to_bytes(msg)
                self.logger.debug("client.send() " + str(raw_stream))
                self.client.send(raw_stream)                
                res = True
            except Exception as e:
                self.logger.error('send_msg() exception: ' + str(e))
                self.logger.debug("Attempt:" + str(attempts))
                attempts += 1

        return res

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def read_msg(self):        
        buf_size = (RPL_SIZE_MAX)*VAL_SIZE
        self.logger.debug("client.recv() buf_size:" + str(buf_size))
        data = self.client.recv(buf_size)
        self.logger.debug("Readed message with size = " + str(len(data)) + " bytes")
        self.logger.debug(data)
        msg = [0 for i in range(int(len(data)/VAL_SIZE))]
        for i in range(len(msg)):
            msg[i] = int.from_bytes(data[i*VAL_SIZE:i*VAL_SIZE + VAL_SIZE-1], byteorder='little')            
        
        self.logger.debug(msg)
        return msg

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
    #
    #--------------------------------------------------------------------------------
    def bytes_to_ints(self, bytes, signed_int=True):        
        number_of_int = len(bytes)//4
        data = [0 for i in range(number_of_int)]
        for i in range(number_of_int):
            bb = bytes[i*VAL_SIZE:i*VAL_SIZE + VAL_SIZE]            
            data[i] = int.from_bytes(bb, byteorder='little', signed=signed_int)        
        return data
    
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def ints_to_bytes(self, ints, bytes_num=4, signed_int=True):        
        bytes = b''.join([x.to_bytes(bytes_num, byteorder='little', signed=signed_int) for x in ints])
        return bytes
    