#!/usr/bin/python
# -*- coding: utf-8 -*-
#  lib/nmr/nmr_prototype.py
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
import math

import numpy
import xml.etree.ElementTree as ET

import lib
from lib.nmr import peaks, integrals

class NMR(object):
    # Constant
    s_storagefilename = "sibunlab"
    
    # Properties
    s_path = ""
    
    def __init__(self, path):
        self.s_path = path
        
    def getPath(self):
        return self.s_path
    
class NMR_1D(NMR):
   pass
   
