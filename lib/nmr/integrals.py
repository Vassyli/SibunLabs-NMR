#!/usr/bin/python
# -*- coding: utf-8 -*-
#  lib/nmr/integrals.py
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

class Integral(object):
    i_n_from = 0
    i_n_to = 0
 
    f_area = None
    o_nmr = None
    
    def __init__(self, i_n_from, i_n_to, nmr = None):
        self.i_n_from = i_n_from
        self.i_n_to = i_n_to
        self.o_nmr = nmr
        
    def getStart(self):
        return self.i_n_from
        
    def getStartPPM(self):
        return self.o_nmr.i2ppm(self.i_n_from)
        
    def getStartHz(self):
        return self.o_nmr.i2Hz(self.i_n_from)
        
    def getEnd(self):
        return self.i_n_to
        
    def getEndPPM(self):
        return self.o_nmr.i2ppm(self.i_n_to)
        
    def getEndHz(self):
        return self.o_nmr.i2Hz(self.i_n_to)
        
    def getArea(self):
        return self.getAbsArea() / self.o_nmr.getIntegralReference()
        
    def getAbsArea(self):
        if self.f_area == None:
            a = self.o_nmr.getSlice(self.i_n_from, self.i_n_to)
            self.f_area = a.cumsum()[-1]
        
        return self.f_area
        
    
class IntegralList(object):
    a_integrallist = {}
    a_integral_starts = {}
    a_integral_ends = {}
    
    a_integrals = []
    
    i_current = 0
    
    o_nmr = None
    
    def __init__(self, nmr):
        self.a_integrallist = {}
        self.a_integrals = []
        self.i_current = 0
        self.o_nmr = nmr
        
    def addIntegral(self, i_n_from, i_n_to):
        if self.overlapsIntegrals(i_n_from, i_n_to):
            print "\tIntegral overlaps with existing integral"
        else:
            integral = Integral(i_n_from, i_n_to, nmr = self.o_nmr)            
            for n in range(i_n_from, i_n_to):
                self.a_integrallist[n] = integral
                
            self.a_integral_starts[i_n_from] = integral
            self.a_integral_ends[i_n_to] = integral
            
            self.a_integrals.append(i_n_from)
            
            # Set Integral = 1, if none was set before
            if self.o_nmr.hasIntegralReference() == False:
                self.o_nmr.setIntegralReference(integral.getAbsArea())
    
    def deleteIntegral(self, integral = None, start = None, end = None):
        if integral != None:
            i_n_from = integral.getStart()
            i_n_to = integral.getEnd()
        elif start != None:
            integral = self.a_integral_starts[start]
            i_n_from = integral.getStart()
            i_n_to = integral.getEnd()
        elif end != None:
            integral = self.a_integral_ends[end]
            i_n_from = integral.getStart()
            i_n_to = integral.getEnd()
            
        for n in range(i_n_from, i_n_to):
            del self.a_integrallist[n]
            
        del self.a_integral_starts[i_n_from]
        del self.a_integral_ends[i_n_to]
        
        self.a_integrals.remove(i_n_from)
        self.resort()
    
    def overlapsIntegrals(self, i_n_from, i_n_to):
        # Get intersection - if integral range intersects with existing integrals, 
        # it overlaps.
        intersec = [val for val in self.a_integrallist.keys() if val in range(i_n_from, i_n_to)]
        
        if len(intersec) == 0:
            return False
        else:
            return True
            
    def resort(self):
        self.a_integrals.sort(reverse=True)
    
    def __iter__(self):
        self.resort()
        self.i_current = 0
        return self

    def next(self):
        if self.i_current >= len(self.a_integrals):
            raise StopIteration
        else:
            self.i_current += 1
            return self.a_integral_starts[self.a_integrals[self.i_current-1]]
