"""
  Project       : Spectometer client
  Author        : CSG
  Contacts      : csg@tpu.ru
  Workfile      : algorithm_gaussFitter.py
  Description   : Class for calculating gaussian peaks in spectrum data
"""

import time
import csv
import logging
import timeit
import numpy as np
from scipy.optimize import curve_fit

from analitics.algorithm_abc import AlgorithmAbc
    
class GaussFitter(AlgorithmAbc):
    def __init__(self,):
        self.padding = 5        
        self.previousResults = []
        self.logger = logging.getLogger(__name__)     
        self.is_enabled = False   
    
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def set_params(self, params):
        ...

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def process_data(self, data, peakAreas):      
        d = np.array(data)

        # config variables
        padding = self.padding        

        d_ = d[padding:-padding]

        dataLength = d_.shape[0]
        g1_ = self.gauss1D(dataLength, 10.0)
        c_ = np.convolve(d_, g1_, 'same')
        
        maxs, mins = self.getExtremums(c_)
                
        start_ = 0
        peaksNum = maxs.shape[0]        


        result = []
        
        
        for areaId in range(len(peakAreas)):
            maxPeakId = 0
            maxPeakHeight = 0            
            for peakId in range(0, peaksNum):
                areaId_ = self.determineArea(maxs[peakId], peakAreas)
                if areaId_ != areaId:
                    continue
                
                if peakId == 0:
                    start_ = 0
                else:
                    start_ = mins[peakId - 1]

                if peakId == peaksNum-1:
                    end_ = dataLength
                else:
                    end_ = mins[peakId]
                
                ms = maxs[peakId]-5
                me = maxs[peakId]+5
                if ms < 0:
                    ms = 0
                if me >= len(d_):
                    me = len(d_)-1
                peakMeanMax = d_[ms:me].mean()
                peakHeight = peakMeanMax - d_[start_:end_].min()                
                
                if peakHeight > maxPeakHeight:
                    maxPeakHeight = peakHeight
                    maxPeakId = peakId                                            
            
            width = self.getFWHM(c_, maxs[maxPeakId])

            sigmaFromW = width/2.35482
            smoothedPeakHeight = c_[maxs[maxPeakId]]

            smoothedIntegral2sigma = sum(c_[maxs[maxPeakId]:maxs[maxPeakId]+int(sigmaFromW)*2])*2

            smoothedIntegral = smoothedPeakHeight * width * np.sqrt(np.pi/(4*np.log(2)))

            # print("!!!!!!", smoothedPeakHeight, width, sigmaFromW, integral2sigma, gaussIntegral )

            channelIdx = padding + maxs[maxPeakId]
            sigmaA = peakAreas[areaId][2]

            sumStart = int(channelIdx - 2*sigmaA)
            sumEnd   = int(channelIdx + 2*sigmaA)
            if sumStart < 0:
                sumStart = 0
            if sumEnd >= len(data):
                sumEnd = len(data) - 1

            dataStart = int(channelIdx - sigmaA)
            dataEnd   = int(channelIdx + 2*sigmaA)
            meanIdx = sigmaA
            peakData = data[dataStart:dataEnd]
            
            x = np.arange(len(peakData))
            popt,pcov = curve_fit(self.gauss, x, peakData, p0=[peakMeanMax, meanIdx, sigmaA])
            a = popt[0]
            b = popt[1]
            c = popt[2]

            peakMean_   = dataStart + b
            peakHeight_ = a
            peakSigma_  = c/np.sqrt(2) 
            gaussIntegral_ = a*c*np.sqrt(np.pi)

            
            sumLeftRight = sum(data[sumStart:sumEnd])
            sumRightDouble = 1.1663*sum(data[channelIdx - int(sigmaA):sumEnd])

            #peakAreaHalfWidth = int((peakAreas[areaId][1] - peakAreas[areaId][0])/2)
            #sourceSum2 = sum(data[channelIdx - peakAreaHalfWidth:channelIdx + peakAreaHalfWidth])
            #result.append([channelIdx, gSigma, gWeight, gIntegral, sourceSum, sourceSum2])
            #result.append([channelIdx, maxPeakHeight, sumLeftRight, sumRightDouble, width, gaussIntegral])
            #result.append([channelIdx, maxPeakHeight, sumLeftRight, smoothedIntegral, smoothedIntegral2sigma])
            result.append([peakMean_, peakHeight_, peakSigma_, gaussIntegral_])
        
        return result
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def gauss(self, x, a, b, c):
        return a*np.exp(-(x-b)**2/c**2)
    
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def weightedMean(self, data):
        x = np.arange(len(data))
        return sum(x * data)/sum(data)


    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def determineArea(self, peakIdx, peakAreas):
        areaId = -1
        i = 0
        for area in peakAreas:
            areaStart = area[0] - self.padding
            areaEnd = area[1] - self.padding
            if areaStart < peakIdx and peakIdx < areaEnd:
                areaId = i
                break
            i += 1
        return areaId

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def gauss1D(self, pointsNum, sigma):
        h = int(pointsNum/2)
        x      = np.zeros(pointsNum)
        gauss_ = np.zeros(pointsNum)
            
        x = np.arange(-h, h)

        c = 1/(sigma * np.sqrt(2*np.pi))
        for i in range(pointsNum):
            gauss_[i] = c*np.exp(-1/2*(x[i]/sigma)**2)

        return gauss_  

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def getExtremums(self, data):
        maxsIdx = []
        minsIdx = []

        dx = 0
        w = 5   
        gradient = 0        
    
        dataLength = data.shape[0]
        #print(type(data), dataLength)

        for i in range(0, dataLength-1):
            gradient_ = data[i + 1] - data[i]
            if gradient > 0 and gradient_ <= 0:
                maxsIdx.append(i)                
            
            if gradient < 0 and gradient_ >= 0: 
                minsIdx.append(i)
            
            gradient = gradient_

        return np.array(maxsIdx), np.array(minsIdx)

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def fitGauss(self, data, peakIdx):

        pointsNum = data.shape[0]
        expectaion = 0
        sigma = 0
        weight = 0
        
        meanStart = peakIdx
        sigmaStart = self.getStd(data, meanStart)
        weightStart = 1
        
        sigmaN = 100
        sigmaStart = 1
        sigmaRange = 100
        sigmaStep = sigmaRange/sigmaN
        sigmas = np.arange(sigmaStart, sigmaStart + sigmaRange, sigmaStep)
        
        #weightN = 2000
        weightN = 2000
        weightStart = 1
        weightRange = 40000
        weightStep = weightRange/weightN
        weights = np.arange(weightStart, weightStart + weightRange, weightStep)
    
        sqrDiffs = np.zeros((sigmaN, weightN))

        for i in range(0, sigmaN):
            startT = time.process_time()
            meanGT = 0
            meanSDT = 0
            for j in range(0, weightN):
                t1 = time.process_time()
                gauss_ = self.getGaussData(pointsNum, meanStart, sigmas[i], weights[j])
                t2 = time.process_time()
                sqrDiffs[i, j] = self.sqrDifference(data, gauss_)
                t3 = time.process_time()
                meanGT  = meanGT + t2-t1
                meanSDT = meanSDT + t3-t2
                #print("Times:", j, t2-t1, t3-t2)

            finishT = time.process_time()
            print("One line time:", i, finishT - startT)
            print("Mean times:", str(meanGT/weightN), str(meanSDT/weightN))
        
        v, x, y = self.getLocalMinimum(sqrDiffs, 1, 1)       
        
        expectaion = meanStart;
        sigma = sigmas[x];
        weight = weights[y];

        return expectaion, sigma, weight

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def fitParams(self, data, peak, areaId):
        params = {}

        if len(self.previousResults) > areaId:
            params = {"sigmaStart" : self.previousResults[areaId][0],
                    "sigmaStepMax" : self.previousResults[areaId][1],
                    "weightStart"  : self.previousResults[areaId][2],
                    "weightStepMax": self.previousResults[areaId][3],
                    #"meanStart"    : self.previousResults[areaId][4],
                    "meanStart"    : peak,
                    "meanStepMax"  : 0.1
                    }
        else:
            peakHeght = data[peak]
            params = {"sigmaStart"   : 20,
                      "sigmaStepMax" : 1,
                      "weightStart"  : 1,
                      "weightStepMax": peakHeght*7,
                      "meanStart"    : peak,
                      "meanStepMax"  : 0.1
                     }

        return params
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def fitGauss2(self, data, fitParams):
        
        sigmaStart    = fitParams["sigmaStart"]
        sigmaStepMax  = fitParams["sigmaStepMax"]        
        weightStart   = fitParams["weightStart"]
        weightStepMax = fitParams["weightStepMax"]
        meanStart     = fitParams["meanStart"]
        meanStepMax   = fitParams["meanStepMax"]

        #print(fitParams)

        pointsNum = data.shape[0]
        expectaion = 0
        sigma = 0
        weight = 0                                 
        
        sigmaC  = sigmaStart
        weightC = weightStart        
        stepsDone = 0
        stepValues = np.zeros((3,3))

        maxStepsNum = 50
        ratio = 1
        minRatio = 0.001
        sigmaStep  = sigmaStepMax*ratio
        weightStep = weightStepMax*ratio
        gradDesc = 1

        while stepsDone < maxStepsNum and ratio > minRatio and gradDesc > 0:
            gradDesc = -1000
            while gradDesc < 0 and stepsDone < maxStepsNum:
                
                for s in range(-1, 2):
                    for w in range(-1, 2):
                        sigma_  = sigmaC + s*sigmaStep
                        weight_ = weightC + w*weightStep

                        mean_ = int(sigma_*2)
                        dStart = meanStart - mean_
                        dEnd   = meanStart + mean_

                        if dStart < 0:
                            dStart = 0
                            mean_ = meanStart
                        if dEnd >= len(data):
                            dEnd = len(data) - 1

                        data_  = data[dStart:dEnd]

                        if len(data_) > 0:
                            gauss_  = self.getGaussData(len(data_), mean_, sigma_, weight_)
                            stepValues[s+1, w+1] = self.sqrDifference(data_, gauss_)
                        else:
                            stepValues[s+1, w+1] = 100000000

                [gradDesc, s_, w_] = self.getMaxGradient(stepValues, 1, 1)

                stepsDone = stepsDone + 1                                            
                #print(stepsDone, "grad=", gradDesc, 'r=', ratio, 'wStep', weightStep ,'s & w =', sigmaC, weightC)

                sigmaC = sigmaC + (s_-1)*sigmaStep
                weightC = weightC + (w_-1)*weightStep

                if sigmaC < 0:
                    print("Alarm! Sigma=", sigmaC)

            ratio = abs(gradDesc/stepValues[1,1])
            sigmaStepMax = sigmaStepMax/2
            sigmaStep = sigmaStepMax
            weightStepMax = weightStep/2
            weightStep = weightStepMax

        #print("Steps:", stepsDone, "Ratio:", ratio, "SigmaStep:", sigmaStep, "WeightStep:", weightStep)
        expectaion = meanStart
        sigma = sigmaC
        weight = weightC
        integral = self.gaussIntegral(sigma, weight)       
        return expectaion, sigma, weight, integral

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def getStd(self, data, mean):        
        x = np.arange(len(data))    
        std_ = np.sqrt(sum(data*(x-mean))/(sum(data)-1))
        print('Standart deviation', std_)
        return std_

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def getGaussData(self, pointsNum, peakPos, sigma, weight):
        out = np.zeros(pointsNum)        

        mean_ = peakPos - int(pointsNum/2)        
        sigma_ = sigma

        if sigma_ == 0:
            sigma_ = 0.000000001

        x = np.arange(-pointsNum/2, pointsNum/2)
        
        if x.shape[0] > pointsNum:
            x = x[1:-1]        
            
        c = 1/(sigma_*np.sqrt(2*np.pi))

        for i in range(x.shape[0]):
            out[i] = weight*c*np.exp(-1/2*((x[i] - mean_)/sigma_)**2)
        
        #out = out*weight
        return out
    
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def gaussIntegral(self, sigma, weight):

        pointsNum = int(sigma*6)
        mean_ = int(0)
        sigma_ = sigma

        if sigma_ == 0:
            sigma_ = 0.000000001

        x = np.arange(-pointsNum/2, pointsNum/2)
        
        if x.shape[0] > pointsNum:
            x = x[1:-1]        
            
        c = 1/(sigma_*np.sqrt(2*np.pi))
        integral = 0

        for i in range(x.shape[0]):            
            integral = integral + weight*c*np.exp(-1/2*((x[i] - mean_)/sigma_)**2)
                
        return integral
    
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def sqrDifference(self, in1, in2):
        sum_ = 0    
        for i in range(in1.shape[0]):
            sum_ = sum_ + (in1[i]-in2[i])**2
                
        return sum_

    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def getLocalMinimum(self, data, xStart, yStart):
        grad_ = -1
        x_ = xStart
        y_ = yStart
        
        steps = 0
        x = 0
        y = 0

        while grad_ < 0:
            [grad_, x_, y_] = self.getMaxGradient(data, x_, y_)
            steps = steps + 1
            if grad_ < 0:
                x = x_
                y = y_            
        v = data[x, y]

        return v, x, y
    
    #--------------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------------
    def getMaxGradient(self, data, x, y):

        xSize = data.shape[0]
        ySize = data.shape[1]

        gOut = 0
        xOut = 0
        yOut = 0

        ########
        g_ = 0
        x_ = x - 1
        y_ = y - 1    
        if x_ >= 0 and y_ >= 0:
            gOut = data[x_,y_] - data[x,y]
            xOut = x_
            yOut = y_               
        
        x_ = x
        y_ = y - 1
        if x_ >= 0 and y_ >= 0:
            g_ = data[x_,y_] - data[x,y]
            if g_ < gOut:
                gOut = g_
                xOut = x_
                yOut = y_
        
        x_ = x + 1
        y_ = y - 1
        if x_ <= xSize and y_ >= 0:
            g_ = data[x_,y_] - data[x,y]
            if g_ < gOut:
                gOut = g_
                xOut = x_
                yOut = y_                
        ##########
        x_ = x - 1
        y_ = y
        if x_ > 0:
            g_ = data[x_,y_] - data[x,y]
            if g_ < gOut:
                gOut = g_
                xOut = x_
                yOut = y_            
    
        x_ = x + 1
        y_ = y
        if x_ <= xSize:
            g_ = data[x_,y_] - data[x,y]
            if g_ < gOut:
                gOut = g_
                xOut = x_
                yOut = y_
                      
        ##########
        x_ = x - 1
        y_ = y + 1
        if x_ > 0 and y_ <= ySize:
            g_ = data[x_,y_] - data[x,y]
            if g_ < gOut:
                gOut = g_
                xOut = x_
                yOut = y_        
        x_ = x
        y_ = y + 1
        if y_ <= ySize:
            g_ = data[x_,y_] - data[x,y]
            if g_ < gOut:
                gOut = g_
                xOut = x_
                yOut = y_    
        x_ = x + 1
        y_ = y + 1
        if x_ <= xSize and y_ <= ySize:
            g_ = data[x_,y_] - data[x,y]
            if g_ < gOut:
                gOut = g_
                xOut = x_
                yOut = y_

        return gOut, xOut, yOut

    #-----------------------------------------------------------------
    #
    #-----------------------------------------------------------------
    def getFWHM(self, data, peakIdx):
        width = 0.0
        peakHeghtHalf = data[peakIdx]/2
        borderIndex = 0.0
        for i in range(peakIdx + 1, len(data)):
            if data[i] < peakHeghtHalf:
                d1 = data[i-1]
                d2 = data[i]
                borderIndex = i-1 + 1/(1 + (d1-peakHeghtHalf)/(peakHeghtHalf-d2))
                print(borderIndex, d1, d2)
                break
        width = (borderIndex - peakIdx)*2

        return width
