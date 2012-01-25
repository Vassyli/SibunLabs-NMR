#!/usr/bin/python
# -*- coding: utf-8 -*-
#  lib/nmr/__init__.py
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

from bruker import *
from nmr_prototype import *

__all__ = [
    "bruker",
    "nmr_prototype",
    "peaks",
]

def isBruker(path):
    return True
    
def isBruker1DNMR(path):
    if os.path.exists(os.path.join(path, 'fid')):
        return True
    else:
        return False

def getNMR(path):
    if isBruker(path):
        if isBruker1DNMR(path):
            return BrukerNMR_1D(path)
        else:
            raise BrukerNMRTypeNotSupported()
    else:
        raise NMRTypeNotSupported()
        
            
# Exceptions
class NMRException(Exception):
    pass
    
class NMRTypeNotSupported(NMRException):
    pass
    
class BrukerNMRTypeNotSupported(NMRTypeNotSupported):
    pass
    
class NMRNoDataFoundException(NMRException):
    pass
    
class NMRFileNotFound(NMRException):
    pass

class NMRSpectrumNotFoundException(NMRFileNotFound):
    pass


#__all__ = ["gui", "lang", "db"]

