#!/usr/bin/python
# -*- coding: utf-8 -*-
#  gui/mainWindow.py
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
import glob

from PyQt4 import QtCore, QtGui

import main_ui as Ui
import nmrView
import main
import lib

class MainWindow(QtGui.QMainWindow, Ui.Ui_MainWindow):
    main = None

    s_file_path = ""

    o_nmr_set = None
    
    ViewMode1DFid = 1
    ViewMode1DSpectrum = 2

    def __init__(self, m):
        super(MainWindow, self).__init__()
        self.main = m
        
        self.setupUi()
        
    def setupUi(self):
        super(MainWindow, self).setupUi(self)
        
        # Make sure that all controls are disabled
        self.disableWorkspace()
        self.disableSpectrum()
        
        # Icon-Changes
        self.actionNew_Workspace.setIcon(QtGui.QIcon.fromTheme("document-new", self.actionNew_Workspace.icon()))
        self.actionOpen_Workspace.setIcon(QtGui.QIcon.fromTheme("document-open", self.actionOpen_Workspace.icon()))
        self.actionSave_Workspace.setIcon(QtGui.QIcon.fromTheme("document-save", self.actionSave_Workspace.icon()))
        self.actionClose_Workspace.setIcon(QtGui.QIcon.fromTheme("window-close", self.actionClose_Workspace.icon()))
        self.actionQuit.setIcon(QtGui.QIcon.fromTheme("application-exit", self.actionQuit.icon()))
        self.actionClose_NMR.setIcon(QtGui.QIcon.fromTheme("window-close", self.actionClose_NMR.icon()))
        
    def getApplicationObject(self):
        return self.main

    def loadWorkspace(self):
        """ Load the workspace """
        path = self.main.getNMRPath()
        try:
            self.o_nmr_set = lib.filehandler.NMRExperimentSet(path, treewidget = self.experimentList)
            self.enableWorkspace()
        except lib.filehandler.NMRExperimentSetException:
            # No experiments - disable.
            self.disableWorkspace()
            
    def unloadWorkspace(self):
        self.o_nmr_set = []
        self.experimentList.clear()
        self.disableWorkspace()
        
    def loadNMR(self):
        self.enableSpectrum()        
        nmr = self.main.getNMR()
        
        # Prefer spectrum over fid
        if nmr.hasSpectrum() == True:
            self.loadNMR_Spectrum()
        elif nmr.hasFid() == True:
            self.loadNMR_Fid()
        else:
            # Nothing to do! ARGH!
            self.filehandler.closeNMR()
            
    def loadNMR_Spectrum(self):
        self.changeView_UntoggleAllAction()
        self.actionSwitchView_Spectrum.setChecked(True)
        
        self.spectrum.show(nmrView.NMRView1DSpectrum)
            
    def loadNMR_Fid(self):
        self.changeView_UntoggleAllAction()
        self.actionSwitchView_FID.setChecked(True)
        
        self.spectrum.show(nmrView.NMRView1DFid)
        
    def unloadNMR(self):
        self.spectrum.clear()
        self.disableSpectrum()
        
    def changeView(self, mode, checked):
        self.changeView_UntoggleAllAction()
        
        if mode == self.ViewMode1DFid:
            self.actionSwitchView_FID.setChecked(True)
            if checked == True:
                self.spectrum.switchShowMode(nmrView.NMRView1DFid)
        elif mode == self.ViewMode1DSpectrum:
            self.actionSwitchView_Spectrum.setChecked(True)
            if checked == True:
                self.spectrum.switchShowMode(nmrView.NMRView1DSpectrum)
            
    def changeView_UntoggleAllAction(self):
        self.actionSwitchView_FID.setChecked(False)
        self.actionSwitchView_Spectrum.setChecked(False)
        
        
    # Enabler/Disable
    def enableWorkspace(self, what = True):
        """ Enables the controls for the workspace """
        self.menuWorkspace.setEnabled(what)
        self.experimentDockWidget.setEnabled(what)
        self.actionSave_Workspace.setEnabled(what)
        self.actionClose_Workspace.setEnabled(what)
        
    def disableWorkspace(self):
        self.enableWorkspace(False)
        
    def enableSpectrum(self, what = True):
        self.menuSpectrum.setEnabled(what)
        self.actionPick_Peak.setEnabled(what)
        self.actionIntegrate.setEnabled(what)
        self.spectrum.setEnabled(what)
        
    def disableSpectrum(self):
        self.enableSpectrum(False)
            
    # Slots
    def onOpenWorkspace(self):
        dialog_title = QtGui.QApplication.translate("MainWindow", "Open SibunLabs NMR Workspace", None, QtGui.QApplication.UnicodeUTF8)
        homepath = os.path.expanduser("~")
        filefilter = QtGui.QApplication.translate("MainWindow", "SibunLabs NMR Workspace file (*.7nw)", None, QtGui.QApplication.UnicodeUTF8)
        
        filename = QtGui.QFileDialog.getOpenFileName(self, dialog_title, homepath, filefilter)
        
        if filename != "":
            filename = str(filename)
            lib.filehandler.openWorkspaceFile(self.main, filename)
            
    def onSaveWorkspace(self):
        lib.filehandler.saveWorkspaceFile(self.main)
        
    def onCloseWorkspace(self):
        lib.filehandler.closeWorkspaceFile(self.main)
    
    def onExperimentClicked(self, widgetitem, t):
        # Only react if Item is GuiExperiment
        if isinstance(widgetitem, lib.filehandler.NMRExperiment):
            lib.filehandler.openNMR(self.main, widgetitem)
        elif isinstance(widgetitem, lib.filehandler.NMRExperimentSubset):
            pass
        else:
            pass
            
    def onChangeViewToFid(self, checked):
        self.changeView(self.ViewMode1DFid, checked)
        
    def onChangeViewToSpectrum(self, checked):
        self.changeView(self.ViewMode1DSpectrum, checked)
