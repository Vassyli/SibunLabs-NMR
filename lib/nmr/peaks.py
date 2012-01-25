#!/usr/bin/python
# -*- coding: utf-8 -*-
#  lib/nmr/peaks.py
#  
#  Copyright 2012 Basilius Sauter <basilius.sauter@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from lib import common

class Peak(object):
    iN = None
    o_nmr = None
    
    def __init__(self, iN, nmr):
        self.iN = iN
        self.o_nmr = nmr
        
    def getN(self):
        return self.iN
        
    def getPPM(self, doRound = False, numOfNumbers = 5):
        if doRound:
            return common.round_significant(self.o_nmr.i2ppm(self.iN), numOfNumbers)
        else:
            return self.o_nmr.i2ppm(self.iN)
        
    def getHz(self, doRound = False, numOfNumbers = 5):
        if doRound:
            return common.round_significant(self.o_nmr.i2Hz(self.iN), numOfNumbers)
        else:
            return self.o_nmr.i2Hz(self.iN)
        
    
class PeakList(object):
    aPeaklist = {}
    aPeaks = []
    iCurrent = 0
    
    o_nmr = None
    
    def __init__(self, nmr):
        self.aPeaklist = {}
        self.aPeaks = []
        self.iCurrent = 0
        self.o_nmr = nmr
        
    def addPeak(self, iN):
        if self.hasPeak(iN):
            print "\tPeak already exists"
        else:
            self.aPeaklist[iN] = Peak(iN, nmr = self.o_nmr)
            self.aPeaks.append(iN)
            
    def deletePeak(self, peak = None, n = None):
        if peak != None:
            n = peak.getN()
        elif n != None and self.hasPeak(n):
            peak = self.aPeaklist[n]
            
        if self.hasPeak(n):
            del self.aPeaklist[n]
            
            self.aPeaks.remove(n)
            self.resort()
            
    def hasPeak(self, iN):
        if iN in self.aPeaklist:
            return True
        else:
            return False
            
    def resort(self):
        self.aPeaks.sort(reverse=True)
    
    def __iter__(self):
        self.resort()
        self.iCurrent = 0
        return self

    def next(self):
        if self.iCurrent >= len(self.aPeaks):
            raise StopIteration
        else:
            self.iCurrent += 1
            return self.aPeaklist[self.aPeaks[self.iCurrent-1]]
