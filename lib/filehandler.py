#!/usr/bin/python
# -*- coding: utf-8 -*-
#  lib/filehandler.py
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
import copy

import xml.etree.ElementTree as ET
from PyQt4 import QtCore, QtGui

import lib

def openWorkspaceFile(main, filename):
    """ Open a workspace file (*.7nw) and let the application know """
    filename = os.path.normcase(filename)
    filedir = os.path.dirname(filename)
    
    # Check if there is already an open workspace
    if main.getWorkspaceFile() != None:
        # Check if there even is an open nmr!
        if main.getNMR() != None:
            closeNMR(main)
        
        closeWorkspaceFile(main)
    
    if os.path.exists(filename):
        tree = ET.parse(filename)
        workspace = tree.getroot()
        
        # Get nmr basepath
        nmrpath = workspace.find("nmrpath")
        if nmrpath == None:
            # If empty: lets asume the basedir is the same where the file is.
            nmr_basepath = filedir
        else:
            nmr_basepath = nmrpath.text
            nmr_basepath = os.path.normcase(os.path.join(filedir, nmr_basepath))
    
    main.openWorkspace(filename, nmr_basepath)
    
def saveWorkspaceFile(main):
    filename = main.getWorkspaceFile()
    filedir = os.path.dirname(filename)
    
    nmr_basepath = os.path.relpath(main.getNMRBasepath(), filedir)
    
    root = ET.Element("workspace")
    
    # Save path-to-nmr-basedir
    nmrpath = ET.SubElement(root, "nmrpath")
    nmrpath.text = nmr_basepath
    
    ET.ElementTree(root).write(filename, encoding='UTF-8', xml_declaration=True)
    
def closeWorkspaceFile(main):
    saveWorkspaceFile(main)
    main.closeWorkspace()
    
def openNMR(main, nmr):
    old_nmr = main.getNMR()
    
    if old_nmr != None:
        closeNMR(main)
    
    if isinstance(nmr, NMRExperiment):
        nmr = copy.copy(nmr.getNMR())
    elif isinstance(nmr, lib.nmr.NMR):
        nmr = copy.copy(nmr)
    else:
        raise ValueError("nmr has to be a object of lib.filehandler.NMRExperiment or lib.nmr.NMR")
        
    main.openNMR(nmr)
    
def closeNMR(main):
    # Save procedure....
    # Nothing to do.
    
    main.closeNMR()

class NMRExperimentSet(object):
    s_path = ""
    l_experiments = []
    o_treewidget = None
    
    def __init__(self, path, treewidget = None):
        self.s_path = path
        self.l_experiments = []
        self.o_treewidget = treewidget
        
        self.getExperiments()
        
    def getPath(self):
        return self.s_path
        
    def countExperiments(self):
        return len(self.l_experiments)
        
    def addExperiment(self, expset):
        if isinstance(expset, NMRExperimentSubset):
            self.l_experiments.append(expset)
            
            if self.o_treewidget != None:
                self.o_treewidget.addTopLevelItem(expset)
        else:
            raise ValueError("expset has to be a valid object of NMRExperimentSubset")
        
    def getExperiments(self):
        """ Search the path of the experiment and get every single entry."""
        dir = os.listdir(self.getPath())
        
        for experiment in dir:
            try:
                exp = NMRExperimentSubset(self.s_path, experiment)
                self.addExperiment(exp)
            except NMRExperimentSubsetException:
                # Skip if it isn't an experiment - for now.
                # Later, this would be the place to recognize
                # single file experiments.
                continue
        
        if self.countExperiments() == 0:
            raise NMRExperimentSetException('No Experiments found.')
        
        
class NMRExperimentSubset(NMRExperimentSet, QtGui.QTreeWidgetItem):
    s_experiment = ""
    
    def __init__(self, path, experiment):
        self.s_experiment = experiment
        # UI - call Parent widget
        QtGui.QTreeWidgetItem.__init__(self, self.getRowName(), QtGui.QTreeWidgetItem.Type)
        
        NMRExperimentSet.__init__(self, path)
        
        if os.path.isdir(self.getPath()) == False:
            raise NMRExperimentSubsetException()
        
    def getPath(self):
        p = NMRExperimentSet.getPath(self)
        return os.path.join(p, self.getExperimentName())
        
    def getExperimentName(self):
        return self.s_experiment
        
    def getRowName(self):
        return [self.getExperimentName()]
        
    def addExperiment(self, exp):
        if isinstance(exp, NMRExperiment):
            self.l_experiments.append(exp)
            
            # UI - add Child-Row
            self.addChild(exp)
        else:
            raise ValueError("expset has to be a valid object of NMRExperimentSubset")
        
    def getExperiments(self):
        dir = os.listdir(self.getPath())
        
        for experiment in dir:
            try:
                exp = NMRExperiment(NMRExperimentSet.getPath(self), self.getExperimentName(), experiment)
                self.addExperiment(exp)
            except lib.nmr.NMRTypeNotSupported:
                continue
                
        if len(self.l_experiments) == 0:
            raise NMRExperimentSubsetException()
            
class NMRExperiment(QtGui.QTreeWidgetItem):
    s_path = ""
    s_experiment = ""
    s_expno = ""
    
    o_nmr = None
    
    def __init__(self, path, experiment, expno):
        self.s_path = path
        self.s_experiment = experiment
        self.s_expno = expno
        
        self.setNMR()
        
        # UI - call Parent widget
        QtGui.QTreeWidgetItem.__init__(self, self.getRowName(), QtGui.QTreeWidgetItem.Type)
        
    def getPath(self):
        return os.path.join(self.s_path, self.s_experiment, self.s_expno)
        
    def setNMR(self):
        self.o_nmr = lib.nmr.getNMR(self.getPath())
        
    def getNMR(self):
        return self.o_nmr
        
    def getExpNo(self):
        return self.s_expno
        
    def getRowName(self):
        return [self.getExpNo(), "", ""]
            
class NMRExperimentSetException(Exception):
    pass
    
class NMRExperimentSubsetException(NMRExperimentSetException):
    pass
    
