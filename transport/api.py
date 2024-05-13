"""
  Project       : Spectometer client
  Author        : Borshch Vladislav
  Contacts      : borchsh.vn@gmail.com
  Workfile      : api.py
  Description   : API for communication with different boards through different transports
"""

import time
import csv
import logging
import numpy as np
import traceback
import pprint
import os
import copy

from PyQt5.QtCore import pyqtSignal, QObject

from com import com
from ethernet import ethernet
from scpi import scpi
from api_param import *

from regmap.include.regmap import *

import filters.payload_correction as pc

class api(QObject):
    signal_upd_gui_ver = pyqtSignal(object)
    signal_upd_gui_adc = pyqtSignal(object)
    signal_upd_gui_shield_temp = pyqtSignal(object)
    signal_upd_graph = pyqtSignal(object)
    signal_upd_areas = pyqtSignal(object)
    signal_upd_trends = pyqtSignal(object)
    signal_connection_state = pyqtSignal(object)
    signal_statusbar_message = pyqtSignal(object)
    signal_popup_message = pyqtSignal(object)
    signal_daq_done = pyqtSignal()
    signal_spi_rd = pyqtSignal(object)
    signal_upd_wave = pyqtSignal(object)

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def __init__(self, daq_status, transport_params, debug_api, debug_transport):
        super(api, self).__init__()        
        self.cont_daq = daq_status
        self.transport_params = transport_params
        self.samples_to_read = 0
        self.exposition = 0

        self.logger = logging.getLogger(__name__)
        if debug_api:
            self.logger.setLevel(logging.DEBUG)

        self.settings_loaded = {}
        self.last_frame_number = 0        
        self.payload_corrector = pc.payload_correction()

        ##########################################
        ## file handlers for data output
        self.pf = object()
        self.csv_writer_trends = object()
        self.fh_spec = object()
        self.csv_writer_spectr = object()
        self.fh_trend = object()
        self.csv_writer_vt = object()

        if self.transport_params["transport"] == 1:
            self.transport = ethernet(debug_transport)
        elif self.transport_params["transport"] == 2:
            self.transport = scpi(debug_transport)
        else:
            self.transport = com(debug_transport)

        self.registers_map = RegMap(self.transport)
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def check_connect(self):
        res = False
        try:
            res = self.transport.check_connect()           
        except Exception as e:
            self.logger.error('check_connect error: ' + str(e))

        if (False == res):
            self.signal_connection_state.emit(False)
        else:
            self.signal_connection_state.emit(True)

        return res
    
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def eeprom_wr(self, dac_settings):        
        self.logger.debug('EEPROM write DAC settings: ' + str(dac_settings))
        try:
            if self.connect(self.transport_params):            
                for i in range(len(dac_settings)):
                    res = self.transport.eeprom_wr(i, dac_settings[i])        
        except Exception as e:
            self.logger.error('eeprom_wr() exception: ' + str(e))            

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def dac_wr(self, addr, data):
        self.logger.debug('DAC write: 0x%02X, Data: 0x%02X' % (int(addr), int(data)))
        try:
            self.transport.dac_wr(addr, data)
            return True
        except Exception as e:
            self.logger.error('dac_wr() exception: ' + str(e))
        return False

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def dac_rd(self, addr):
        self.logger.debug('DAC read: 0x%02X' % (int(addr)))
        try:                  
            res = self.transport.dac_rd(addr)                           
            return res
        except Exception as e:
            self.logger.error('dac_rd exception: ' + str(e))
            return False


    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def addr_wr(self, addr, data):
        self.logger.debug('addr_wr(): 0x%02X, Data: 0x%02X' % (int(addr), int(data)))
        try:            
            self.transport.addr_wr(addr, data)            
            return True
        except Exception as e:
            self.logger.error('addr_wr error: ' + str(e))
            return False   

    
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def addr_rd(self, addr):
        self.logger.debug('Reading. Address: 0x%02X' % int(addr))
        try:
            data = self.transport.addr_rd(addr)
            return data
        except Exception as e:
            self.logger.error('addr_rd() exception: ' + str(e))
            return None

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def set_timeout(self, timeout):
        #self.logger.debug('set_timeout(): ' + str(timeout))
        if self.check_connect():            
            try:                
                self.transport.set_timeout(timeout)                
                return True
            except Exception as e:
                self.logger.error('set_timeout() exception: ' + str(e))
        return False    

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def get_fpga_version(self):
        ver = [0]*6
        if self.connect(self.transport_params):   
            ver[0] = str(self.registers_map.ver)
            ver[1] = str(self.registers_map.sub)
            ver[2] = str(self.registers_map.rev)

            daemon_ver = self.read_daemon_version()             
            ver[3] = (daemon_ver) & 0xFFFF
            ver[4] = (daemon_ver >>  16) & 0xFFFF

            uptime = self.read_uptime()
            ver[5] = uptime
            
            self.disconnect()
        
        self.signal_upd_gui_ver.emit(ver)


    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def read_adc(self, adc_num):
        self.logger.debug('Reading adc: 0x%02X' % int(adc_num))
        try:
            if (self.transport_params["transport"] == 2):         
                data = self.transport.transaction([SCPI_READ_ADC, adc_num], True)
                error_status = data[0]
            elif (self.transport_params["transport"] == 1): 
                data = self.transport.transaction([CMD_READ_ADC, adc_num], True)
                error_status = data[0]
            else:
                self.logger.error('addr_rd error: unknown transport')

            if (error_status != 0):
                    self.logger.error('read_adc error: ' + str(error_status))
                    return -1

            return data[1]
        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            self.logger.error(traceback_str)
            self.logger.error('addr_rd exception: ' + str(e))
            return -1


    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def read_daemon_version(self):
        self.logger.debug('Reading daemon version')
        try:  
            if (self.transport_params["transport"] == 2):         
                data = self.transport.transaction([SCPI_GET_DAEMON_VERSION], True)
                error_status = data[0]
            else: 
                data = self.transport.transaction([CMD_GET_DAEMON_VERSION], True)
                error_status = data[0]
            if (error_status != 0):
                self.logger.error('read_adc error: ' + str(error_status))
                return -1            
            return data[1]
        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            self.logger.error(traceback_str)
            self.logger.error('read_daemon_version() exception: ' + str(e))
            return -1

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def read_uptime(self):
        self.logger.debug('read_uptime()')
        try:   
            if (self.transport_params["transport"] == 2):         
                data = self.transport.transaction([SCPI_GET_UPTIME], True)
                error_status = data[0]
            else: 
                data = self.transport.transaction([CMD_GET_UPTIME], True)
                error_status = data[0]
            if (error_status != 0):
                self.logger.error('read_uptime() error: ' + str(error_status))
                return -1            
            return data[1]
        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            self.logger.error(traceback_str)
            self.logger.error('read_uptime() exception: ' + str(e))
            return -1


    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def read_shield_temp(self):
        self.logger.debug('Reading temp')
        try:
            if self.connect(self.transport_params):  
                if (self.transport_params["transport"] == 2):         
                    data = self.transport.transaction([SCPI_READ_TMP], True)                                   
                    self.signal_upd_gui_shield_temp.emit(data[1])
                    self.disconnect()
                    return data[1]
                else: 
                    data = self.transport.transaction([CMD_READ_TMP], True)                                   
                    self.signal_upd_gui_shield_temp.emit(data[1])
                    self.disconnect()
                    return data[1]
        except Exception as e:
            self.logger.error('read_shield_temp() exception: ' + str(e))
            return -1

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def get_adc_data(self):
        adc_data = [0 for i in range(ADC_NUMBER)]        
        if self.connect(self.transport_params):
            for i in range(len(adc_data)):
                adc_data[i] = self.read_adc(i)       
            self.disconnect()

        self.signal_upd_gui_adc.emit(adc_data)
        return adc_data

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def dacs_wr(self, dac_settings):
        res = False
        if self.connect(self.transport_params):
            self.logger.debug("Sleeping 1 sec...")
            time.sleep(1)

            for i in range(len(dac_settings)):
                res  = self.dac_wr(i, dac_settings[i])

            self.disconnect()
            # Wait until new values will be loaded
            time.sleep(0.5)
        return res

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def spi_wr(self, dac_settings):
        res = False
        if self.connect(self.transport_params):            
            time.sleep(0.5)
        return res

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def spi_rd(self, data, sel_mask):
        res = False
        if self.connect(self.transport_params):
            spi_dat_lsb = (data     ) & 0xFF
            spi_dat_msb = (data >> 8) & 0xFF
            #
            res  = self.addr_wr(pADDR_SPI_LSB, spi_dat_lsb)
            res &= self.addr_wr(pADDR_SPI_MSB, spi_dat_msb)
            res &= self.addr_wr(pADDR_SPI_SEL, sel_mask)
            #
            res &= self.addr_wr(pADDR_SPI_SOP, 0x01)
            # Wait until SPI will be loaded
            time.sleep(0.5)
            # Read SPI register
            spi_lsb = self.addr_rd(pADDR_SPI_R_LSB)
            spi_msb = self.addr_rd(pADDR_SPI_R_MSB)
            self.disconnect()

            spi_dat = (spi_msb << 8) | spi_lsb
            self.signal_spi_rd.emit(spi_dat)
        return res


    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def load_settings(self, settings):
        ''' Load DAQ settings into FPGA '''
        self.logger.debug('================  Load DAQ settings into FPGA ===================')
        #self.logger.debug("Previous: " + str(self.settings_loaded))
        #self.logger.debug("New sett: " + str(settings))
        
        res = False
        if self.connect(self.transport_params):        

            self.transport.select_channel(0)
            
            # Load setting into FPGA

            if self.settings_loaded.get("samples")     != settings["samples"]:                
                self.registers_map.sampl_num   = settings["samples"]                
            if self.settings_loaded.get("area_begin0") != settings["area_begin0"]:
                self.registers_map.area0_start = settings["area_begin0"]
            if self.settings_loaded.get("area_end0")   != settings["area_end0"]:
                self.registers_map.area0_end   = settings["area_end0"]
            if self.settings_loaded.get("area_begin1") != settings["area_begin1"]:
                self.registers_map.area1_start = settings["area_begin1"]
            if self.settings_loaded.get("area_end1")   != settings["area_end1"]:                
                self.registers_map.area1_end   = settings["area_end1"]
            if self.settings_loaded.get("area_begin2") != settings["area_begin2"]:                
                self.registers_map.area2_start = settings["area_begin2"]
            if self.settings_loaded.get("area_end2")   != settings["area_end2"]:
                self.registers_map.area2_end   = settings["area_end2"]

            #self.logger.debug("regmap: dec_rate %d" % settings["dec_rate"])
            #self.registers_map.dec_rate      = settings["dec_rate"]
                                        
            if self.settings_loaded.get("gate_begin") != settings["gate_begin"]:
                self.logger.debug("regmap: gate_begin %d" % settings["gate_begin"])
                self.registers_map.acc_start     = settings["gate_begin"]
            
            if self.settings_loaded.get("gate_end") != settings["gate_end"]:
                self.logger.debug("regmap: gate_end %d" % settings["gate_end"])
                self.registers_map.acc_stop      = settings["gate_end"]
            
            if self.settings_loaded.get("gate_ctrl") != settings["gate_ctrl"]:
                self.logger.debug("regmap: gate_ctrl %d" % settings["gate_ctrl"])
                self.registers_map.gate_ctrl     = settings["gate_ctrl"]
            
            if self.settings_loaded.get("adc_threshold") != settings["adc_threshold"]:
                self.logger.debug("regmap: adc_threshold %d" % settings["adc_threshold"])
                self.registers_map.adc_th = settings["adc_threshold"]
            
            if self.settings_loaded.get("mov_average") != settings["mov_average"]:
                self.logger.debug("regmap: mov_average %d" % settings["mov_average"])
                self.registers_map.adc_filter    = settings["mov_average"]
            
            if self.settings_loaded.get("bline_lvl") != settings["bline_lvl"]:
                self.logger.debug("regmap: bline_lvl %d" % settings["bline_lvl"])
                self.registers_map.bline_manual  = settings["bline_lvl"]

            if self.settings_loaded.get("bline_acc_lvl") != settings["bline_acc_lvl"]:
                self.logger.debug("regmap: bline_acc %d" % settings["bline_acc_lvl"])
                self.registers_map.bline_acc     = settings["bline_acc_lvl"]

            if (self.settings_loaded.get("bline_avr_num") != settings["bline_avr_num"]) or (self.settings_loaded.get("bline_auto") != settings["bline_auto"]):
                bline_auto_calc = (settings["bline_avr_num"]) & 0x7F
                if settings["bline_auto"]:
                    bline_auto_calc = (settings["bline_avr_num"]) | 0x80  
                self.logger.debug("regmap: bline_average %d" % bline_auto_calc)
                self.registers_map.bline_average = bline_auto_calc   

            if self.settings_loaded.get("bline_trend_delay") != settings["bline_trend_delay"]:
                self.logger.debug("regmap: bline_trend_delay %d" % settings["bline_trend_delay"])
                self.registers_map.bline_trend_delay = settings["bline_trend_delay"]

            if self.settings_loaded.get("pileups_acc_lvl") != settings["pileups_acc_lvl"]:
                self.logger.debug("regmap: pileups_acc %d" % settings["pileups_acc_lvl"])
                self.registers_map.pileup_acc         = settings["pileups_acc_lvl"]

            if self.settings_loaded.get("pileups_trend_delay") != settings["pileups_trend_delay"]:
                self.logger.debug("regmap: pileup_trend_delay %d" % settings["pileups_trend_delay"])
                self.registers_map.pileup_trend_delay = settings["pileups_trend_delay"]

            ###############################################################################################
            self.transport.select_channel(1)
            if self.settings_loaded.get("samples") != settings["samples"]:
                self.registers_map.sampl_num   = settings["samples"]
            if self.settings_loaded.get("area_begin0") != settings["area_begin0"]:
                self.registers_map.area0_start = settings["area_begin0"]
            if self.settings_loaded.get("area_end0") != settings["area_end0"]:
                self.registers_map.area0_end   = settings["area_end0"]
            if self.settings_loaded.get("area_begin1") != settings["area_begin1"]:
                self.registers_map.area1_start = settings["area_begin1"]
            if self.settings_loaded.get("area_end1") != settings["area_end1"]:
                self.registers_map.area1_end   = settings["area_end1"]
            if self.settings_loaded.get("area_begin2") != settings["area_begin2"]:
                self.registers_map.area2_start = settings["area_begin2"]
            if self.settings_loaded.get("area_end2") != settings["area_end2"]:
                self.registers_map.area2_end   = settings["area_end2"]

            if self.settings_loaded.get("gate_begin2") != settings["gate_begin2"]:
                self.registers_map.acc_start     = settings["gate_begin2"]
            if self.settings_loaded.get("gate_end2") != settings["gate_end2"]:
                self.registers_map.acc_stop      = settings["gate_end2"]
            if self.settings_loaded.get("gate_ctrl2") != settings["gate_ctrl2"]:
                self.registers_map.gate_ctrl     = settings["gate_ctrl2"]
            #self.logger.debug("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            #self.logger.debug("loaded adc_threshold2" + str(self.settings_loaded.get("adc_threshold2")) )
            #self.logger.debug("new    adc_threshold2" + str(settings["adc_threshold2"]) )
            if self.settings_loaded.get("adc_threshold2") != settings["adc_threshold2"]:                
                self.registers_map.adc_th        = settings["adc_threshold2"]
            if self.settings_loaded.get("mov_average2") != settings["mov_average2"]:
                self.registers_map.adc_filter    = settings["mov_average2"]
            if self.settings_loaded.get("bline_lvl2") != settings["bline_lvl2"]:
                self.registers_map.bline_manual  = settings["bline_lvl2"]
            if self.settings_loaded.get("bline_acc_lvl2") != settings["bline_acc_lvl2"]:
                self.registers_map.bline_acc     = settings["bline_acc_lvl2"]
            
            if (self.settings_loaded.get("bline_avr_num2") != settings["bline_avr_num2"]) or (self.settings_loaded.get("bline_auto2") != settings["bline_auto2"]):
                bline_auto_calc2 = (settings["bline_avr_num2"]) & 0x7F
                if settings["bline_auto2"]:
                    bline_auto_calc2 = (settings["bline_avr_num2"]) | 0x80                 
                self.registers_map.bline_average      = bline_auto_calc2
            
            if self.settings_loaded.get("bline_trend_delay2") != settings["bline_trend_delay2"]:
                self.registers_map.bline_trend_delay  = settings["bline_trend_delay2"]            
            if self.settings_loaded.get("pileups_acc_lvl2") != settings["pileups_acc_lvl2"]:
                self.registers_map.pileup_acc         = settings["pileups_acc_lvl2"]
            if self.settings_loaded.get("pileups_trend_delay2") != settings["pileups_trend_delay2"]:
                self.registers_map.pileup_trend_delay = settings["pileups_trend_delay2"]

            self.disconnect()
            res = True

        if (res):
            self.logger.debug("Settings is loaded!")
            self.settings_loaded = copy.deepcopy(settings)
            return res
        else:
            self.logger.error("Settings loading error!")
            return res


    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def daq(self, settings):
        self.logger.debug("DAQ starting...")
        self.logger.debug("Settings:" + str(settings))
        # Read data from FPGA
        frame_cnt = 0
        area_vals = []        
        events = 0
        lost_frames = 0 
        elapsed_time = 0
        exposition = settings["samples"]/100e6        
        fast_daq = False
        
        if exposition < 0.5:
            self.logger.debug("Fast daq is True")
            fast_daq = True
        
        # Create file if we need it        
        stamp = time.strftime("%Y-%m-%d_%H_%M_%S")
        self.logger.debug("!!! " + str( settings["save_to_file"] ) + " " + str( settings["reset_data"] ) )
        if (settings["save_to_file"] and settings["reset_data"]):
            self.logger.debug("Creating out files for data")
            data_dir = 'data'
            if (not os.path.isdir(data_dir)):
                os.mkdir(data_dir)

            filename = "trends_" + stamp + ".csv"
            self.pf  = open(data_dir + '/' + filename, "w")
            self.csv_writer_trends = csv.writer(self.pf, delimiter=';', quoting=csv.QUOTE_NONE, lineterminator='\n')
            self.csv_writer_trends_data = []
            
            filename = "spectr_" + stamp + ".csv"
            self.fh_spec = open(data_dir + '/' + filename, "w")
            self.csv_writer_spectr = csv.writer(self.fh_spec, delimiter=';', quoting=csv.QUOTE_NONE, lineterminator='\n')
            self.csv_writer_spectr_data = []       

            filename = "spectr_" + stamp + "_corr.csv"
            self.fh_spec_c = open(data_dir + '/' + filename, "w")
            self.csv_writer_spectr_c = csv.writer(self.fh_spec_c, delimiter=';', quoting=csv.QUOTE_NONE, lineterminator='\n')
            self.csv_writer_spectr_data_c = []     

            filename = "vt_" + stamp + ".csv"
            self.fh_trend = open(data_dir + '/' + filename, "w")
            self.csv_writer_vt = csv.writer(self.fh_trend, delimiter=';', quoting=csv.QUOTE_NONE, lineterminator='\n')
            self.csv_writer_vt_data = []

        if settings["payload_correction"]:
            self.payload_corrector.load_peacs_pos_from_payload(settings["payload_correction_file"])

        # Save DAQ settings if we need it
        # self.logger.debug("!!!!!!!!!!!!!!!!!!!!!!!! " + str( settings["save_to_file"] ) + " " + str( self.cont_daq["need_reset"] ) )
        
        if (settings["save_settings_to_file"] and settings["reset_data"]):
            data_dir = 'data'
            if (not os.path.isdir(data_dir)):
                os.mkdir(data_dir)
            filename = "settings_" + stamp + ".txt"
            self.save_daq_settings(data_dir + '/' + filename)            
        
        #last_frame_num = 0
            
        start_time = time.time()        
        if (self.connect(self.transport_params)):                        
            self.exposition_elapsed = False
            
            self.set_timeout(2*exposition)
            last_update_time = time.time()
            while True:               
                self.logger.debug('Starting reading spectrums cycle')
                # Send command to start aquisition process for one exposition time                
                # Read data
                self.transport.run_daq()                
                data = self.transport.read_data()

                # If data frame has incorrect size or something else we can't process it,
                # just increment lost frames counter and drop current frame
                if data:
                    if len(data) < DAQ_SAMPLES_NUM:
                        self.logger.warning(f'api read_data {len(data)} bytes out of {DAQ_SAMPLES_NUM} readed')
                        self.logger.warning("Current data frame has been dropped")
                        lost_frames += 1
                    # Otherwise we can process it
                    else:
                        data_info = data[-6:]
                        frame_num = data[-1]
                        data = data[:-6]
                        self.logger.debug("info length: " + str(len(data_info)) )
                        self.logger.debug("data length: " + str(len(data)) )

                        # Get last bytes with areas sizes if we have request of it
                        self.logger.debug("Type of data " + str(type(data)))
                        
                        spectra_list = np.array_split(data, len(data) / SPECTRUM_NUM)
                        
                        si = 0
                        for s in spectra_list:
                            self.logger.debug("Spectra_list: %d %d" % (si, len(s)))
                            si = si + 1
                        
                        area_vals_list = []
                        spectrum_vals_list = []         
                        spectrum_vals_c = []

                        for spectrum in spectra_list:
                            area_vals      = spectrum[pTABLE_SIZE:pTABLE_SIZE + pAREAS_SIZE]                            
                            spectrum_vals  = spectrum[0:pTABLE_SIZE]
                            
                            area_vals_list.append(area_vals)
                            if settings["payload_correction"] and not fast_daq:
                                spectrum_vals_c = self.payload_corrector.apply(spectrum_vals)
                                spectrum_vals_list.append(spectrum_vals_c)
                            else:
                                spectrum_vals_list.append(spectrum_vals)

                            if (settings["save_to_file"]):
                                if fast_daq:                                                                    
                                    self.csv_writer_trends_data.append(area_vals)
                                    self.csv_writer_spectr_data.append(spectrum_vals)
                                else:
                                    self.csv_writer_trends.writerow(area_vals)
                                    self.csv_writer_spectr.writerow(spectrum_vals)
                                    if settings["payload_correction"]:
                                        self.csv_writer_spectr_c.writerow(spectrum_vals_c)                                                    

                        #self.logger.debug("Area values: " + str(area_vals_list))                        
                        #self.logger.debug("!!! Two spectra size = %d" % len(spectrum_vals_list))

                        # Some statistic for GUI
                        frame_cnt += 1
                        elapsed_time = float(time.time() - start_time)
                        if elapsed_time > 0:
                            fps = frame_cnt/elapsed_time
                        else:
                            fps = 0
                        
                        statusbar_msg = ("DAQ status: %04.3f seconds, %d frames, %02.1f FPS, %5d lost frames, events/frame: "
                                        % (elapsed_time, frame_cnt, fps, lost_frames))                        
                        for s in spectra_list:
                            statusbar_msg = statusbar_msg + " " + str(sum(s[:pTABLE_SIZE]))    

                        adc_data = data_info[0:5]

                        # Update pictures
                        # self.signal_upd_trends.emit(area_vals_list)
                        self.signal_upd_gui_adc.emit(adc_data)
                        
                        if (time.time()  - last_update_time) > 0.5:
                            # self.signal_upd_areas.emit(area_vals_list)                                                    
                            self.signal_upd_graph.emit(spectrum_vals_list)
                            self.signal_statusbar_message.emit(statusbar_msg)                                                        
                            self.logger.debug("ADC + Temp data: " + str(adc_data))
                            self.logger.debug("Area vals: " + str(area_vals_list))
                            self.logger.debug("Frame number: " + str(frame_num))                            
                            last_update_time = time.time()                        
                        
                        if ((frame_num - self.last_frame_number) > 1):
                            self.logger.error("Frame is lost! Losted frames number = " + str(frame_num - self.last_frame_number))
                            self.logger.error("Last good frame number: " + str(self.last_frame_number))
                        self.last_frame_number = frame_num

                        if (settings["save_to_file"]):
                            to_send = [0 for i in range(5)]
                            to_send[0] = adc_data[0]
                            to_send[1] = adc_data[1]
                            to_send[2] = adc_data[2]
                            to_send[3] = adc_data[3]
                            to_send[4] = adc_data[4]
                            self.csv_writer_vt.writerow(to_send)                                            
                
                # Ok, we have enough
                if (elapsed_time > settings["exposition"]):
                    self.logger.debug("api: elapsed_time > exposition")
                    self.exposition_elapsed = True
                    break

                # Check break of DAQ                
                #self.logger.debug("check cont_daq: {}" % self.cont_daq['runned'])
                if not self.cont_daq['runned']:
                    break
            
            self.set_timeout(1)
            self.transport.stop_daq()
        # Anyway, we have disconnect from device and set short timeout back
        self.disconnect()
        
        self.logger.debug("Stopping Daq: save_to_file " + str(settings["save_to_file"]) + ' need_reset ' + str(self.cont_daq['need_reset']))
        if (settings["save_to_file"] and self.cont_daq['need_reset']):            
            if fast_daq:
                self.logger.debug("Fast daq: saving data after stop...")                
                self.csv_writer_trends.writerows(self.csv_writer_trends_data)
                self.csv_writer_spectr.writerows(self.csv_writer_spectr_data)
                self.logger.debug('Corecting spectres')
                self.payload_corrector.set_exposition(exposition)

                if settings["payload_correction"]:                    
                    for s in self.csv_writer_spectr_data:
                        self.csv_writer_spectr_data_c.append(self.payload_corrector.apply(s))                        
                    self.csv_writer_spectr_c.writerows(self.csv_writer_spectr_data_c)
                

            self.pf.close()
            self.fh_spec.close()
            self.fh_trend.close()
            self.fh_spec_c.close()
        
        if self.exposition_elapsed:
            self.signal_daq_done.emit()    

        return True

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def dump_wave(self, samples_num, waves_num, channel_id):        
        #self.logger.debug("dump_wave(%d, %d)" % (samples_num, waves_num) )
        if self.cont_daq['runned']:
            return

        self.cont_daq['dumping_wave'] = True
        i = 0
        #self.logger.debug("dumping_wave %s" % str(self.cont_daq['dumping_wave']) )
        if self.connect(self.transport_params):
            while i < waves_num and self.cont_daq['dumping_wave']:
                #self.logger.debug("wave %00d" % (i))        
                wave = self.transport.read_wave(samples_num, channel_id)
                i = i + 1
                #self.logger.debug("dump_wave() " + str(wave))
                self.signal_upd_wave.emit(wave)
                time.sleep(0.05)
        #self.disconnect()
        

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    # def read_data(self, samples_num, timeout, req):        
    #     try:            
    #         data = self.transport.read_data()            
    #         return data
    #     except Exception as e:
    #         self.logger.error("".join(['DAQ SerialException error! ', e]))
    #         return False


    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def data_parse(self, data):
        ''' Parses data to positive integers.
            A little tricky, because we have LSB format for RedPitaya device
            and MSB format for MAX10 devices.
            Probably, I have to align firmwares, but I do not want to
            change anything there because of ongoing testing in the industry
        '''
        tmp_arr = []
        if self.transport_params["transport"] == 1:
            for i in range(0, len(data), pBYTE_PER_WORD):
                sample  = 0
                sample |= (data[i+0] & 0xFF) <<  0
                sample |= (data[i+1] & 0xFF) <<  8
                sample |= (data[i+2] & 0xFF) << 16
                tmp_arr.append(sample)
        elif self.transport_params["transport"] == 0:
            for i in range(0, len(data), pBYTE_PER_WORD):
                sample  = 0
                sample |= (data[i+0] & 0xFF) << 16
                sample |= (data[i+1] & 0xFF) <<  8
                sample |= (data[i+2] & 0xFF) <<  0
                tmp_arr.append(sample)
        return tmp_arr


    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def connect(self, settings):
        if self.transport_params["transport"] == 1:
            self.transport = ethernet(False)
        elif self.transport_params["transport"] == 2:
            self.transport = scpi(False)
        else:
            self.transport = com(debug_transport)
        
        self.registers_map = RegMap(self.transport)
        res = self.transport.connect(settings)
        if not self.check_connect():
            return False
        return res

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def disconnect(self):        
        self.transport.disconnect()        
        self.signal_connection_state.emit(False)
        return True

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def save_file(self, data):
        # Saving to file...
        channels = dict()
        a_file = open("data.dat", "wb")
        pickle.dump(data, a_file)
        a_file.close()

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def save_daq_settings(self, filename):
        self.logger.info("Saving DAQ settings into: " + filename)
        #a_file = open(filename, "w")           
        
        if (len(self.settings_loaded) > 0):
            import json
            with open(filename, "w") as outfile:
                json.dump(self.settings_loaded, outfile)            

   