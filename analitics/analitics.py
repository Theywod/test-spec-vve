"""
  Project       : Spectrometer Analitics Module
  Author        : CSG
  Contacts      : csg@tpu.ru
  Workfile      : analitics.py
  Description   : Class for interaction with different analitical algorithms
"""

import time
import csv
import logging
import numpy as np
import threading 
from PyQt5.QtCore import pyqtSignal, QObject, QThread

from analitics.algorithm_abc import AlgorithmAbc
from analitics.gauss_search_fit.algorithm_gaussFitter import GaussFitter
from analitics.gauss_search_fit.algorithm_peak_search import peak_search

class Analitics(QObject):    
    signal_analitics_start = pyqtSignal(object) 
    signal_analitics_done  = pyqtSignal(object) 
       
    isConnected = False
    isBusy = False

    spectrumFile = object
    gaussFile    = object

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def __init__(self):
        super(Analitics, self).__init__()
        self.isBusy = False        
        self.peaks = GaussFitter()
        self.peak = peak_search()        

        self.algorithm_dict = {}
        self.algorithm_dict.update({self.peaks.__class__.__name__: self.peaks})
        self.algorithm_dict.update({self.peak.__class__.__name__: self.peak})

        self.lastData = [] 
        self.peakAreas = []  
        self.foundedGausses = [] 

        self.signal_analitics_start.connect(self.processData)

        self.logger = logging.getLogger(__name__)
    
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def set_params(self, params):        
        a = self.algorithm_dict[params['algorithm_name']]
        a.set_params(params)
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def addData(self, data):  

        self.lastData = data
        d = np.array([data])
        d.transpose()
        #np.savetxt(self.spectrumFile, d, delimiter=",")

        #if not self.isConnected:
        #     self.signal_analitics_start.connect(self.processData)
        #     self.isConnected = True  

        if self.isBusy:
            print("Warning analitics is Busy!!!!!")
            return         
        else:          
            self.isBusy = True              
            self.signal_analitics_start.emit(data)
    
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def processData(self, data):
        for a in self.algorithm_dict.values():
            if a.is_enabled:
                result = a.process_data(data, self.peakAreas)
                self.signal_analitics_done.emit(result)


        #m = self.algorithm_dict['peak_search']
        #result = m.process_data(data, self.peakAreas)
        #self.signal_analitics_done.emit(result)

        #r = np.array(result)
        #result_ = np.reshape(result, -1)
        #d = np.array([result_])
        #d.transpose()
                
        #np.savetxt(self.gaussFile, d, delimiter=",")
        #self.gaussFile.flush()        

        self.isBusy = False
    
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def reset(self):
        self.foundedGausses.clear()
        self.lastData.clear()
        self.peakAreas.clear()
        
        #stamp = time.strftime("%Y-%m-%d_%H_%M_%S")
        #filenameS = "spect_" + stamp + ".txt"
        #self.spectrumFile = open(filenameS, 'w')
        #self.spectrumFile.close()                
        #self.spectrumFile = open(filenameS, 'a')
        
        #filenameG = "gauss_" + stamp + ".txt"
        #self.gaussFile = open(filenameG, 'w')
        #self.gaussFile.close()
        #self.gaussFile = open(filenameG, 'a')      

        






