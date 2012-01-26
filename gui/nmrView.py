#!/usr/bin/python
# -*- coding: utf-8 -*-
#  gui/nmrView.py
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

import numpy
import scipy

from PyQt4 import QtCore, QtGui, QtOpenGL

# View modes
NMRView1DFid = 1
NMRView1DSpectrum = 2

NMRViewX1AxisPaddingTop = 10
NMRViewX1AxisPaddingBottom = 50

class NMRView(QtGui.QGraphicsView):
    o_main_window = None
    o_main = None
    
    fid_scene = None
    spc_scene = None

    # Items
    fid_items = {
        "axis" : None,
        "plot" : None,
        "plot_real" : None,
    }
    
    spc_items = {
        "axis" : None,
        "plot" : None,
    }
    
    fid_is_drawn = False
    spc_is_drawn = False
    
    fid_resize_group = None
    spc_resize_group = None
    
    show_mode = None
    
    canvas_width = None
    canvas_height = None
    
    scene_corner = 0.0
    
    x1_axis_padding_top = NMRViewX1AxisPaddingTop
    x1_axis_padding_bottom = NMRViewX1AxisPaddingBottom
    
    # Tmp
    drag = False
    dragpos = None
    
    def __init__(self, centralwidget):
        super(NMRView, self).__init__(centralwidget)
        
        self.o_main_window = centralwidget.parentWidget()
        self.o_main = self.o_main_window.getApplicationObject()
        
        self.initScenes()
        
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor('white')))
        
        widget = QtOpenGL.QGLWidget()
        widget.setAutoFillBackground(True)
        widget.qglClearColor(QtGui.QColor('white'))
        self.setViewport(widget)
        # Empty Scene
        self.setScene(NMRScene())
        
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        
    def initScenes(self):
        self.fid_scene = NMRScene()
        self.spc_scene = NMRScene()
        
    def clearScenes(self):
        self.fid_scene = NMRView.fid_scene
        self.fid_is_drawn = NMRView.fid_is_drawn
        self.fid_items = NMRView.fid_items
        self.fid_resize_group = NMRView.fid_resize_group
        
        self.spc_scene = NMRView.spc_scene
        self.spc_is_drawn = NMRView.spc_is_drawn
        self.spc_items = NMRView.spc_items
        self.spc_resize_group = NMRView.spc_resize_group
        
        self.initScenes()
        
    def show(self, mode = NMRView1DFid):
        self.show_mode = mode
        
        if mode == NMRView1DFid:
            if self.fid_is_drawn == False:
                self.drawFid()
            self.setScene(self.fid_scene)
        elif mode == NMRView1DSpectrum:
            if self.spc_is_drawn == False:
                self.drawSpc()
            self.setScene(self.spc_scene)
            
        self.setSceneRect(0.0, -self.canvas_height, self.canvas_width, self.canvas_height)
        
    def clear(self):
        self.clearScenes()
    
    def switchShowMode(self, mode):
        if self.show_mode != mode:
            self.show(mode)
    
    def drawFid(self):
        self.drawFidAxis()
        self.drawFidPlot()
        
        # Group items together
        self.fid_resize_group = self.fid_scene.createItemGroup([
            self.fid_items["axis"], 
            self.fid_items["plot"],
        ])
        
        self.fid_is_drawn = True
        
    def drawFidAxis(self):
        # A FID
        self.fid_items["axis"] = self.fid_scene.addLine(
            self.x(0), self.y(0 - self.x1_axis_padding_top), 
            self.x(0, True), self.y(0 - self.x1_axis_padding_top)
        )
        
    def drawFidPlot(self):
        self.fid_items["plot"] = FidPlotItem(self.x(0), self.y(0), self.getXWidth(), self.getYHeight())
        self.fid_scene.addItem(self.fid_items["plot"])
        
        data = self.o_main.getNMR().getFid()
        
        # Create a polygon with n items
        #polygon = QtGui.QPolygonF(data.shape[-1])
        x0 = 0
        y0 = 1.0 / (-2) * (data[0].real)
        #path = QtGui.QPainterPath(QtCore.QPointF(x0, y0))
        path = QtGui.QPainterPath(self.fid_items["plot"].point(x0, y0))
        
        # Add points to the polygon
        for i in numpy.arange(1, data.shape[-1]):
            x = 1.0 / data.shape[-1] * i
            y = 1.0 / (-2) * (data[i].real)
            # y-points may vary from -height....+height and are in item-coordinates of PlotItem
            # This ensures a zoom where y = 0 always stays on the same position. No more bouncing
            # plots! Still have to invert + and -.
            #polygon[i] = QtCore.QPointF(x, y)
            #path.lineTo(QtCore.QPointF(x, y))
            path.lineTo(self.fid_items["plot"].point(x, y))
            
            
        #print polygon.first()
        #print polygon.last()
            
        #self.fid_items["plot_real"] = self.fid_scene.addPolygon(polygon)
        self.fid_items["plot_real"] = self.fid_scene.addPath(path)
        self.fid_items["plot_real"].setParentItem(self.fid_items["plot"])
            
    def drawSpc(self):
        self.drawSpcAxis()
        self.drawSpcPlot()
        
        # Group items together
        self.spc_resize_group = self.spc_scene.createItemGroup([
            self.spc_items["axis"], 
            self.spc_items["plot"],
        ])
        
        self.spc_is_drawn = True
        
    def drawSpcAxis(self):
        self.spc_items["axis"] = self.spc_scene.addLine(
            self.x(0), self.y(0 - self.x1_axis_padding_top), 
            self.x(0, True), self.y(0 - self.x1_axis_padding_top)
        )
        pass
    
    def drawSpcPlot(self):
        self.spc_items["plot"] = SpcPlotItem(self.x(0), self.y(0), self.getXWidth(), self.getYHeight())
        self.spc_scene.addItem(self.spc_items["plot"])
        
        data = self.o_main.getNMR().getSpectrum()
        
        # Create a polygon with n items
        #polygon = QtGui.QPolygonF(data.shape[-1])
        x0 = 0
        y0 = 1.0 / (-2) * (data[0].real)
        path = QtGui.QPainterPath(self.spc_items["plot"].point(x0, y0))
        
        # Add points to the polygon
        for i in numpy.arange(1, data.shape[-1]):
            #x = float(self.getXWidth()) / data.shape[-1] * i
            #y = float(self.getYHeight()) / (-2) * (data[i].real)
            x = 1.0 / data.shape[-1] * i
            y = 1.0 / (-2) * (data[i].real)
            # y-points may vary from -height....+height and are in item-coordinates of PlotItem
            # This ensures a zoom where y = 0 always stays on the same position. No more bouncing
            # plots! Still have to invert + and -.
            #polygon[i] = QtCore.QPointF(x, y)
            #path.lineTo(QtCore.QPointF(x, y))
            path.lineTo(self.spc_items["plot"].point(x, y))
        
        # Draw to the bottom - and back.
        #path.lineTo(QtCore.QPointF(1, 0))
        #path.lineTo(QtCore.QPointF(0, 0))
            
        self.spc_items["plot_real"] = self.spc_scene.addPath(path)
        self.spc_items["plot_real"].setParentItem(self.spc_items["plot"])
    
    
    # Transform-Qt-to-plot-coordinations (x: →, y: ↑ instead of x: →, y: ↓)
    def x(self, x, reverse = False):
        """ Transform x """
        if reverse == False:
            return x
        else:
            return self.canvas_width - x
        
    def y(self, y, reverse = False):
        """ Transform y """
        if reverse == False:
            return (y + self.getYBottomOffset()) * -1
        else:
            return (self.canvas_height - self.getYTopOffset() - y) * -1
            
    def getXWidth(self):
        return self.canvas_width - self.XLeftOffset() - self.XRightOffset()
        
    def XLeftOffset(self):
        return 0
        
    def XRightOffset(self):
        return 0
        
    def getYHeight(self):
        return self.canvas_height - self.x1_axis_padding_bottom - self.x1_axis_padding_top
            
    def getYBottomOffset(self):
        return self.x1_axis_padding_bottom + self.x1_axis_padding_top
        
    def getYTopOffset(self):
        return 0
            
            
    # Events....
    def resizeEvent(self, resizeEvent):
        size = resizeEvent.size()
        
        new_width = size.width()
        new_height = size.height()
        
        if self.canvas_width == None:
            self.canvas_width = new_width
            
        if self.canvas_height == None:
            self.canvas_height = new_height
        
        if new_width > self.canvas_width:
            x_t = float(new_width) / self.canvas_width
            self.canvas_width = new_width
        else:
            x_t = 1.0
            
        y_t = float(new_height) / self.canvas_height
        self.canvas_height = new_height
        
        transform = QtGui.QTransform()
        transform = QtGui.QTransform.scale(transform, x_t, y_t)
        
        # Apply!
        if self.fid_resize_group != None:
            self.fid_resize_group.setTransform(transform, True)
            
        if self.spc_resize_group != None:
            self.spc_resize_group.setTransform(transform, True)
                   
        # (0,0) to the left bottom corner
        self.setSceneRect(self.scene_corner, -self.canvas_height, new_width, new_height)
        
    def mousePressEvent(self, event):
        mousebuttons = event.buttons()
        
        if mousebuttons & QtCore.Qt.LeftButton:
            event.accept()
            self.drag = True
            self.dragpos = (event.x(), event.y())
        else:
            event.ignore()
        
    def mouseMoveEvent(self, event):
        if self.drag == True:
            event.accept()
            moveto = self.scene_corner - (self.dragpos[0] - event.x())
            
            if moveto > (0 - self.canvas_width/2) and moveto < (self.canvas_width*0.5):
                self.setSceneRect(self.scene_corner - (self.dragpos[0] - event.x()), -self.canvas_height, self.canvas_width, self.canvas_height)
        else:
            event.ignore()
            
    def mouseReleaseEvent(self, event):
        if self.drag == True:
            event.accept()
            moveto = self.scene_corner - (self.dragpos[0] - event.x())
            
            if moveto <= (0 - self.canvas_width/2):
                self.scene_corner = (0 - self.canvas_width/2)
            elif moveto >= (self.canvas_width*0.5):      
                self.scene_corner = (self.canvas_width*0.5)
            else:
                self.scene_corner = self.scene_corner - (self.dragpos[0] - event.x())
            
            self.setSceneRect(self.scene_corner, -self.canvas_height, self.canvas_width, self.canvas_height)
            
            self.drag = False
            self.dragpos = None
        else:
            event.ignore()
            
    def wheelEvent(self, event):
        # Zomg!
        
        # Make steps a number between -1 and 1.
        steps = event.delta() / 8.0 / 360.0
        
        # Make bigger
        if steps > 0:
            zoom_factor = 1.0 + steps
        elif steps < 0:
            zoom_factor = 1.0 / (1.0 + abs(steps))
        else:
            zoom_factor = 1.0
            
        minus = steps/abs(steps)
            
        #transform = QtGui.QTransform()
        #transformA = QtGui.QTransform.scale(transform, 1.0, zoom_factor)
        
        if self.show_mode == NMRView1DFid:
            self.fid_items["plot"].scale(1, zoom_factor)
        elif self.show_mode == NMRView1DSpectrum:
            self.spc_items["plot"].scale(1, zoom_factor)
                     
class PlotItem(QtGui.QGraphicsRectItem):
    def paint(self, a, b, c):
        pass
        
class FidPlotItem(PlotItem):
    x = 0
    y = 0
    w = 0
    h = 0
    
    def __init__(self, x, my, w, h):
        """y is the "middle"""
        super(FidPlotItem, self).__init__()
        
        self.x = x
        self.y = my
        self.w = w
        self.h = h
        
        self.translate(0, my - h/2 - 0.5)
        self.setRect(x, -h/2.0, w, h)
        
    def point(self, x, y):
        """ Maps x 0...1 to 0..w and y -1..1 to -h..h"""
        return QtCore.QPointF(round(self.w * x, 2), round(self.h * y, 2))
        
class SpcPlotItem(PlotItem):
    x = 0
    y = 0
    w = 0
    h = 0
    
    def __init__(self, x, y, w, h):
        super(SpcPlotItem, self).__init__()
        
        print "Create Box at Position %s,%s " % (x, y)
        print "Translate position %s,%s to %s,%s" % (x, y, x+0, -h)
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.translate(0, y)
        self.setRect(x, -h, w, h*2)
        
    def point(self, x, y):
        """ Maps x 0...1 to 0..w and y -1..1 to -h..h"""
        return QtCore.QPointF(round(self.w * x, 2), round(self.h*2 * y, 2))

            
class NMRScene(QtGui.QGraphicsScene):
    pass
    
