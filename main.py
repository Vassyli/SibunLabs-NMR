#!/usr/bin/python
# -*- coding: utf-8 -*-
#  main.py
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

import sys
import os

from PyQt4 import QtCore, QtGui

import gui

class SibunlabNMR(QtGui.QApplication):
    s = None
    o_main_window = None

    # Contains the path to this file
    s_main_path = ""
    
    s_workspace_file = None
    s_nmr_path = None
    
    o_nmr = None

    def __init__(self, sysarg):
        if self.s == None:
            super(SibunlabNMR, self).__init__(sysarg)

            self.o_main_window = gui.mainWindow.MainWindow(self)
            self.s_main_path = os.path.join(os.curdir, os.path.dirname(sysarg[0]))
        else:
            raise Exception("Initialization of Application only possible once. Use Application.get() instead.")

    @classmethod
    def get(cls, sysarg):
        if cls.s == None:
            cls.s = SibunlabNMR(sysarg)

        return cls.s

    def run(self):
        # Run the main application
        self.o_main_window.show()
        
    def openWorkspace(self, workspacefile, nmrpath):
        self.s_workspace_file = workspacefile
        self.s_nmr_path = nmrpath
        
        self.o_main_window.loadWorkspace()
        
    def closeWorkspace(self):
        self.s_workspace_file = None
        self.s_nmr_path = None
        
        self.o_main_window.unloadWorkspace()
        
    def getWorkspaceFile(self):
        return self.s_workspace_file
        
    def getNMRPath(self):
        return os.path.join(self.s_nmr_path, 'nmr')
        
    def getNMRBasepath(self):
        return self.s_nmr_path
        
    def openNMR(self, nmr):
        self.o_nmr = nmr
        self.o_main_window.loadNMR()
        
    def closeNMR(self):
        self.o_nmr = None
        self.o_main_window.unloadNMR()
        
    def getNMR(self):
        return self.o_nmr



if __name__ == "__main__":
    app = SibunlabNMR.get(sys.argv)
    app.run()
    sys.exit(app.exec_())
