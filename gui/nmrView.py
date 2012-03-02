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

import math

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
        "axis_items" : None,
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
        x0 = 0
        y0 = 1.0 / (-2) * (data[0].real)
        path = QtGui.QPainterPath(self.fid_items["plot"].point(x0, y0))
        
        # Add points to the polygon
        for i in numpy.arange(1, data.shape[-1]):
            x = 1.0 / data.shape[-1] * i
            y = 1.0 / (-2) * (data[i].real)
            # y-points may vary from -height....+height and are in item-coordinates of PlotItem
            # This ensures a zoom where y = 0 always stays on the same position. No more bouncing
            # plots! Still have to invert + and -.
            path.lineTo(self.fid_items["plot"].point(x, y))

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
        self.spc_items["axis"] = SpcAxisItem(
            self.x(0), self.y(0 - self.x1_axis_padding_top), self.getXWidth(), self.getYHeight(),
            self.o_main.getNMR().getSpectrumHighestPPMValue(),
            self.o_main.getNMR().getSpectrumLowestPPMValue()
        )
        
        self.spc_scene.addItem(self.spc_items["axis"])
    
    def drawSpcPlot(self):
        self.spc_items["plot"] = SpcPlotItem(self.x(0), self.y(0), self.getXWidth(), self.getYHeight())
        self.spc_scene.addItem(self.spc_items["plot"])
        
        data = self.o_main.getNMR().getSpectrum()
        
        # Create a polygon with n items
        x0 = 0
        y0 = 1.0 / (-2) * (data[0].real)
        path = QtGui.QPainterPath(self.spc_items["plot"].point(x0, y0))
        
        # Add points to the polygon
        for i in numpy.arange(1, data.shape[-1]):
            x = 1.0 / data.shape[-1] * i
            y = 1.0 / (-2) * (data[i].real)
            # y-points may vary from -height....+height and are in item-coordinates of PlotItem
            # This ensures a zoom where y = 0 always stays on the same position. No more bouncing
            # plots! Still have to invert + and -.
            path.lineTo(self.spc_items["plot"].point(x, y))
        
      
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
            self.spc_items["axis"].relocateAxis()
                   
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
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.translate(0, y)
        self.setRect(x, -h, w, h*2)
        
    def point(self, x, y):
        """ Maps x 0...1 to 0..w and y -1..1 to -h..h"""
        return QtCore.QPointF(round(self.w * x, 2), round(self.h*2 * y, 2))
        
class AxisItem(QtGui.QGraphicsRectItem):
    x = 0
    y = 0
    w = 0
    h = 0
    
    childs = []
    childs_dict = {}
    
    def __init__(self, x, y, w, h):
        super(AxisItem, self).__init__(x, y, w, h)
        
        self.childs = []
        self.childs_dict = {}
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.translate(0, y)
        self.setRect(x, -h, w, h*2)
        
        self.drawAxis()
        
    def paint(self, a, b, c):
        pass
        
    def point(self, x, y):
        """ Maps x 0...1 to 0..w and y -1..1 to -h..h"""
        #return QtCore.QPointF(round(self.w * x, 2), round(self.h*2 * y, 2))
        return QtCore.QPointF(self.toX(x), self.toY(y))
        
    def toX(self, x):
        return round(self.w * x, 2)
        
    def toY(self, y):
        return round(self.h*2 * y, 2)
        
    def drawAxis(self):
        axis = QtGui.QGraphicsLineItem(QtCore.QLineF(self.point(0, 0), self.point(1, 0)))
        axis.setParentItem(self)
        
    def relocateAxis(self):        
        for child in self.childs:
            child.relocate()
            
    def addChild(self, identifier, child):
        if isinstance(child, AxisSubItem):
            self.childs.append(child)
            self.childs_dict[identifier] = child
        else:
            raise ValueError("child has to be an object of the class gui.AxisSubItem")
            
    def removeChild(self, identifier):
        child = self.childs_dict[identifier]
        self.scene().removeItem(child)
        self.childs.remove(child)
        del self.childs_dict[identifier]
        
class SpcAxisItem(AxisItem):
    ppmmax = 20
    ppmmin = 0
    
    axiscaptionelements = []
    mode = None
    
    def __init__(self, x, y, w, h, ppmmax, ppmmin):
        # Has to set first some variables, since parent.__init__ calls directly drawAxis which needs them.
        self.ppmmax = ppmmax
        self.ppmmin = ppmmin
        
        super(SpcAxisItem, self).__init__(x, y, w, h)
        
    def drawAxis(self):
        super(SpcAxisItem, self).drawAxis()
        self.addChild("unit", AxisTextItem("ppm", self, 1, y = 20, align = AlignRight))
        
        self.createAxisCaption()
        
    def ppm2x(self, ppm):
        m = 1.0/(self.ppmmin - self.ppmmax)
        q = self.ppmmax/(self.ppmmax - self.ppmmin)
        return m*ppm + q
        
    def clearAxisCaption(self):
        for child in self.axiscaptionelements:
            self.removeChild(child)
        
        # Empty it.
        self.axiscaptionelements = []
            
    def createAxisCaption(self):
        if self.mode == None:
            self.mode = self.getNumberOfNumbers()
            
        specwidth = self.ppmmax - self.ppmmin
        
        # Search an appropriate start point - zero?
        if self.ppmmin < 0 and self.ppmmax > 0:
            start = 0
        else:
            start = round(round(specwidth) / 2, 0)
            
        rangeUpwards = numpy.arange(start, self.ppmmax + 1, self.mode).tolist()
        rangeUpwards.sort()
        rangeDownwards = numpy.arange(start, self.ppmmin - 1, -1*self.mode).tolist()
        rangeDownwards.sort()
        if len(rangeDownwards) > 0:
            rangeDownwards.pop() # Remove start
        rangeDownwards.extend(rangeUpwards)
        
        if self.mode % 1 == 0:
            rangeDownwards = map(int, rangeDownwards)
        
        specLeftPPMMark = math.ceil(self.ppmmax) if self.ppmmax < 0 else math.floor(self.ppmmax)
        specRightPPMMark = math.ceil(self.ppmmin) if self.ppmmin < 0 else math.floor(self.ppmmin)
        
        # Done the preparation - create the actual items.
        for i in rangeDownwards:
            idf = "caption_%s" % (i, )
            idt = "captiontick_%s" % (i, )
            loc = self.ppm2x(i)
            
            iLess = i - self.mode
            
            # Do not paint if the location is < 0 or > 1
            if loc >= 0 and loc <= 1:
                # Draw the figure!
                self.addChild(idf, AxisTextItem(str(i), self, loc, AlignCenter))
                self.axiscaptionelements.append(idf)
                
                # Draw the "line"
                self.addChild(idt, AxisTickItem(self, loc, TickBig))
                self.axiscaptionelements.append(idt)
                
            # Draw Subticks
            if self.mode >= 1.0:
                submode = self.mode / 10.0
            elif self.mode >= 0.5:
                submode = self.mode / 5.0
            else:
                submode = 1
            
            if submode < 1:
                start = i
                
                subrangeUpwards = numpy.arange(start, self.ppmmax + 1, submode).tolist()
                subrangeUpwards.sort()
                subrangeDownwards = numpy.arange(start, self.ppmmin - 1, -1*submode).tolist()
                subrangeDownwards.sort()
                if len(subrangeDownwards) > 0:
                    subrangeDownwards.pop() # Remove start
                subrangeDownwards.extend(subrangeUpwards)
                
                for j in subrangeDownwards:
                    subidt = "%s_subtick_%s" % (idf, j, )
                    subloc = self.ppm2x(j)
                    
                    if subloc >= 0 and subloc <= 1 and subloc != loc:
                        self.addChild(subidt, AxisTickItem(self, subloc, TickSmall))
                        self.axiscaptionelements.append(subidt)
        
    def relocateAxis(self):
        mode = self.getNumberOfNumbers()
        
        if mode != self.mode:
            self.mode = mode
            # Delete all numbers
            self.clearAxisCaption()
            
            # Add Axis-Numbers!
            self.createAxisCaption()
        
        # Call parent's
        super(SpcAxisItem, self).relocateAxis()
        
    def getNumberOfNumbers(self):
        # Until I find something more flexible, I'll have to deal with this.
        # Maybe I have to discriminate between nuclei... Still not sure.
        # 50 is just an replaceable figure..
        foobar = 50
        approximation = round(self.mapRectToScene(self.boundingRect()).width()/foobar)
        if approximation < 4.5:
            approximation = 4
        elif approximation < 7.5:
            approximation = 5
        elif approximation < 12.5:
            approximation = 10
        elif approximation < 27.5:
            approximation = 20
        #elif approximation < 80:
        else:
            approximation = 40
        #elif approximation < 180:
        #    approximation = 100
        #else:
        #    approximation = 200
            
        width = self.ppmmax - self.ppmmin
        steps = round(width / approximation * 2, 0) / 2
        
        # Make sure there are no "0" steps
        if steps <= 0.1:
            steps = 0.1
            
        return steps
    

        
AlignLeft = 1
AlignRight = 2
AlignCenter = 3

TickSmall = 1
TickBig = 2

class AxisSubItem(object):
    pass
        
class AxisTextItem(AxisSubItem, QtGui.QGraphicsTextItem):
    item = None
    align = None
    parent = None
    x = 1
    y = 0
    
    anchor = None
    
    def __init__(self, text, parent, x = 1, align = AlignLeft, y = 0):
        super(AxisTextItem, self).__init__(text, parent)
        self.align = align
        self.parent = parent
        self.x = x
        self.y = y
        
        self.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations)
        
        self.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Normal, False))
        self.setTextWidth(self.boundingRect().width())
        
        # Block-Format
        blockformat = QtGui.QTextBlockFormat()
        
        if self.align == AlignRight:
            blockformat.setAlignment(QtCore.Qt.AlignRight)
        elif self.align == AlignCenter:
            blockformat.setAlignment(QtCore.Qt.AlignCenter)
        else:
            blockformat.setAlignment(QtCore.Qt.AlignLeft)
        
        # Cursor
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        cursor.mergeBlockFormat(blockformat)
        cursor.clearSelection()
        
        # Set cursor
        self.setTextCursor(cursor)
        
        self.locate()
        
    def locate(self):
        self.relocate(False)
        
    def relocate(self, relocate = True):
        """ Relocate this item on the axis to allow a smooth zoom."""
        x = self.parent.toX(self.x)
        
        if self.align == AlignRight:
            x = x - self.mapRectFromScene(self.boundingRect()).width()
        elif self.align == AlignCenter:
            x = x - self.mapRectFromScene(self.boundingRect()).width()/2.0
        else:
            x = x
        
        self.setPos(QtCore.QPointF(x, self.y))
        
class AxisTickItem(AxisSubItem, QtGui.QGraphicsLineItem):
    item = None
    align = None
    parent = None
    x = 1
    y = 0
    
    def __init__(self, parent, x = 1, type = TickSmall):
        super(AxisTickItem, self).__init__(parent)
        self.type = type
        self.parent = parent
        self.x = x
        
        self.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations)
        
        # set Line:
        if type == TickSmall:
            self.setLine(0, 0, 0, 3)
        else:
            self.setLine(0, 0, 0, 5)
            
        self.locate()
            
    def locate(self):
        self.relocate(False)
        
    def relocate(self, relocate = True):
        """ Relocate this item on the axis to allow a smooth zoom."""
        x = self.parent.toX(self.x)
        
        self.setPos(QtCore.QPointF(x, self.y))
        
            
class NMRScene(QtGui.QGraphicsScene):
    pass
    
# Debug
def printTransformation(o):
    print "\t%s, %s, %s" % (o.m11(), o.m12(), o.m13())
    print "\t%s, %s, %s" % (o.m21(), o.m22(), o.m23())
    print "\t%s, %s, %s" % (o.m31(), o.m32(), o.m33())
    
