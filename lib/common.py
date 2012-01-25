#!/usr/bin/python
# -*- coding: utf-8 -*-
#  lib/common.py
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

import math

import numpy

def round_significant(x, n):
    """ Return x with n significant digits """
    digits = int(n - math.ceil(math.log10(abs(x))))
    return round(x, digits)

def is_numeric(text):
    if isinstance(text, str):
        ret = True
        
        if text != "":
            try:
                if text[-1] == '.':
                    fl = numpy.float(text[0:-1])
                else:
                    fl = numpy.float(text)
                    
                if round(fl, 2) == 0.00:
                    ret = False
                else:
                    ret = True
            except ValueError:
                ret = False
        else:
            ret = False
            
        return ret
    else:
        raise ValueError("is_numeric accepts only")
    return None
    
def phase(y, phc0 = 0.0, phc1 = 0.0, returno = numpy.complex):
    c = numpy.arange(y.shape[-1])/numpy.float(y.shape[-1])
    a = 0.017453293 * (phc0 + c * phc1)
    
    r = y.real * numpy.cos(a) + y.imag * numpy.sin(a)
    j = y.real * numpy.sin(a) - y.imag * numpy.cos(a)
    
    return r + (j*1.j)
    
    
