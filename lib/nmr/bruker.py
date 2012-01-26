#!/usr/bin/python
# -*- coding: utf-8 -*-
#  lib/nmr/bruker.py
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

import os
import struct
import math

import scipy
import scipy.fftpack
import numpy


import lib
import __init__ as nmr
import nmr_prototype
import peaks
import integrals

# Variablen, die man aus den Dateien suchen soll
# Im Format name : typ
searchAcqu = {
    'SFO1'    : numpy.float64,
    'SFO2'    : numpy.float64,
    'SFO3'    : numpy.float64,
    'SFO4'    : numpy.float64,
    'SFO5'    : numpy.float64,
    'SFO6'    : numpy.float64,
    'SFO7'    : numpy.float64,
    'SFO8'    : numpy.float64,
    'SW'      : numpy.float64, # Spektrumbreite (ppm)
    'SF'      : numpy.float64, # Im Prinzip sollte hier die Frequenz von 0ppm stehen.
    'SOLVENT' : str, # Das verwendete Lösemittel.
    'GB'      : numpy.float64, # GM-Faktor => Window-Funktion
    'LB'      : numpy.float64, # Linienverbreiterung (Hz) => Window-Funktion
    'TD'      : numpy.int32, # Acquirierte Punkte (r+i), also Zahl der gemessenen Datenpunkte
    'DECIM'   : numpy.int16, # DSP Dezimierungsfaktor
    'DSPFVS'  : numpy.int16, # DSP Version
    'GRPDLY'  : numpy.float64, #? DSP Gruppendelay
    'SI'      : numpy.int32, # Transformationsgrösse
    'BYTORDA' : numpy.int8, # Byteanordnung, 0 und 1
    'DTYPA'   : numpy.int8, # Zahlentyp, 0 = 32 Bit integer
    'AQ_mod'  : numpy.int8, # Aquirierungsmodus
    'DIGMOD'  : numpy.int8, # Filtertyp
    'NS'      : numpy.int64, # Anzahl der Scans
    'PULPROG' : str, # Name des Pulse-Programms
    'NUC1'    : str, # Beobachteter Kern
    'INSTRUM' : str, # Instrumentenname
    'WDW'     : numpy.int8, # Window function type
    'PH_mod'  : numpy.int8, # Phasing type: 0 = None, 1 = "Normal"
    'PHC0'    : numpy.float64, # Phase 0. Ordnung
    'PHC1'    : numpy.float64, # Phase 1. Ordnung
    'SSB'     : numpy.int64, # Sine bell shift
    'MC2'     : numpy.int64, # F1 Detektionsmodus (?)
    'EXP'     : str, # Name des Experiments
}

searchProc = {
    'SF'      : numpy.float64, # Im Prinzip sollte hier die Frequenz von 0ppm stehen.
    'FTSIZE'  : numpy.int32, # Beinhaltet offenbar ebenfalls die Zahl der Zahlen in fid - aber scheint zu stimmen.
    'SI'      : numpy.int32, # Transformationsgrösse, scheint auch in proc zu sein..
    'PHC0'    : numpy.float64, # Phase 0. Ordnung
    'PHC1'    : numpy.float64, # Phase 1. Ordnung
    'BYTORDP' : numpy.int8, # Byte-Ordnung der prozessierten Daten
    'DTYPP'   : numpy.int8, # Zahlentyp, 0 = 32 Bit integer
    'WDW'     : numpy.int8, # Window function type
    'SW_p'    : numpy.float64, # Spektrumbreite für proc
}

phases = {
    12 : {
        2 : 16560.0,
        3 : 13140.0,
        4 : 17280.0,
        6 : 18060.0,
        8 : 19170.0,
        12 : 25020.0,
        16 : 25785.0,
        24 : 25260.0,
        32 : 25965.0,
        48 : 25380.0,
        64 : 26055.0,
        96 : 25440.0,
        128 : 26100.0,
        192 : 25680.0,
        256 : 26010.0,
        384 : 25800.0,
        512 : 25965.0,
        768 : 25860.0,
        1024 : 25942.5,
        1536 : 25890.0,
        2048 : 25931.25,
    }    
}


# Information about the bruker files are taken from the reference material 
#   and fileutil.cs from SpinWorks.
#
#
# Thanks to the authors of this great program and for providing those files
#   which were a great help to understand those files.

class BrukerNMR_1D(nmr_prototype.NMR_1D):
    fid = None
    spectrum = None
    
    def getFidPath(self):
        return os.path.join(self.getPath(), "fid")
    
    def hasFid(self):
        path = self.getFidPath()
        if os.path.exists(path):
            return True
        else:
            return False
        
    def getFid(self):
        if self.fid == None:
            data = numpy.fromfile(self.getFidPath(), dtype=">i4")	
            data = data[...,::2] + data[...,1::2]*1.j
            
            # Normalize to 1
            a = data.real.max()
            i = abs(data.real.min())
            
            if a > i:
                data /= a
            else:
                data /= i
            
            self.fid = data
        
        return self.fid
        
    def getSpectrumPath(self, what = 1):
        if what == 1:
            return os.path.join(self.getPath(), "pdata", "1", "1r")
        elif what == 2:
            return os.path.join(self.getPath(), "pdata", "1", "1i")
        else:
            return (os.path.join(self.getPath(), "pdata", "1", "1r"), os.path.join(self.getPath(), "pdata", "1", "1i"))
            
    def hasSpectrum(self):
        path = self.getSpectrumPath(1)
        if os.path.exists(path):
            return True
        else:
            return False
            
    def getSpectrum(self):
        if self.spectrum == None:
            real = numpy.fromfile(self.getSpectrumPath(1), dtype=">i4")
            imag = numpy.fromfile(self.getSpectrumPath(2), dtype=">i4")
            
            data = real + imag*1j
            
            # Normalize to 1
            a = data.max()
            i = abs(data.min())
            
            if a > i:
                data /= a
            else:
                data /= i
                
            self.spectrum = data
    
        return self.spectrum
