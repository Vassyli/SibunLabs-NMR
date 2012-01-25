# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/main.ui'
#
# Created: Mon Jan 23 17:59:03 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "SibunLabs NMR", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("res/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.spectrum = NMRView(self.centralwidget)
        self.spectrum.setEnabled(True)
        self.spectrum.setMouseTracking(True)
        self.spectrum.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.spectrum.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.spectrum.setRenderHints(QtGui.QPainter.TextAntialiasing)
        self.spectrum.setDragMode(QtGui.QGraphicsView.NoDrag)
        self.spectrum.setObjectName(_fromUtf8("spectrum"))
        self.horizontalLayout.addWidget(self.spectrum)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuSibunLabs_NMR = QtGui.QMenu(self.menubar)
        self.menuSibunLabs_NMR.setTitle(QtGui.QApplication.translate("MainWindow", "Application", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSibunLabs_NMR.setObjectName(_fromUtf8("menuSibunLabs_NMR"))
        self.menuWorkspace = QtGui.QMenu(self.menubar)
        self.menuWorkspace.setEnabled(True)
        self.menuWorkspace.setTitle(QtGui.QApplication.translate("MainWindow", "Workspace", None, QtGui.QApplication.UnicodeUTF8))
        self.menuWorkspace.setObjectName(_fromUtf8("menuWorkspace"))
        self.menuSpectrum = QtGui.QMenu(self.menubar)
        self.menuSpectrum.setEnabled(True)
        self.menuSpectrum.setTitle(QtGui.QApplication.translate("MainWindow", "NMR", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSpectrum.setObjectName(_fromUtf8("menuSpectrum"))
        self.menuView = QtGui.QMenu(self.menuSpectrum)
        self.menuView.setTitle(QtGui.QApplication.translate("MainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.menuHelp.setTearOffEnabled(False)
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setEnabled(False)
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.experimentDockWidget = QtGui.QDockWidget(MainWindow)
        self.experimentDockWidget.setEnabled(False)
        self.experimentDockWidget.setFloating(False)
        self.experimentDockWidget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.experimentDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.experimentDockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "List of experiments", None, QtGui.QApplication.UnicodeUTF8))
        self.experimentDockWidget.setObjectName(_fromUtf8("experimentDockWidget"))
        self.experimentDockWidgetContents = QtGui.QWidget()
        self.experimentDockWidgetContents.setObjectName(_fromUtf8("experimentDockWidgetContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.experimentDockWidgetContents)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.experimentList = QtGui.QTreeWidget(self.experimentDockWidgetContents)
        self.experimentList.setMinimumSize(QtCore.QSize(299, 0))
        self.experimentList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.experimentList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.experimentList.setUniformRowHeights(True)
        self.experimentList.setObjectName(_fromUtf8("experimentList"))
        self.experimentList.headerItem().setText(0, _fromUtf8("Name"))
        self.experimentList.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Nuclei", None, QtGui.QApplication.UnicodeUTF8))
        self.experimentList.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Solvent", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout_2.addWidget(self.experimentList)
        self.experimentDockWidget.setWidget(self.experimentDockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.experimentDockWidget)
        self.actionPick_Peak = QtGui.QAction(MainWindow)
        self.actionPick_Peak.setCheckable(True)
        self.actionPick_Peak.setEnabled(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("res/button-peakpick-big.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPick_Peak.setIcon(icon1)
        self.actionPick_Peak.setText(QtGui.QApplication.translate("MainWindow", "Pick Peak", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPick_Peak.setObjectName(_fromUtf8("actionPick_Peak"))
        self.actionOpen_Workspace = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/trolltech/styles/commonstyle/images/standardbutton-open-32.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen_Workspace.setIcon(icon2)
        self.actionOpen_Workspace.setText(QtGui.QApplication.translate("MainWindow", "Open Workspace", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Workspace.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Workspace.setObjectName(_fromUtf8("actionOpen_Workspace"))
        self.actionQuit = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/trolltech/styles/commonstyle/images/standardbutton-close-32.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon3)
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionIntegrate = QtGui.QAction(MainWindow)
        self.actionIntegrate.setCheckable(True)
        self.actionIntegrate.setEnabled(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("res/button-integrate-big.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionIntegrate.setIcon(icon4)
        self.actionIntegrate.setText(QtGui.QApplication.translate("MainWindow", "Integrate", None, QtGui.QApplication.UnicodeUTF8))
        self.actionIntegrate.setToolTip(QtGui.QApplication.translate("MainWindow", "Integrate from... to", None, QtGui.QApplication.UnicodeUTF8))
        self.actionIntegrate.setObjectName(_fromUtf8("actionIntegrate"))
        self.actionSave_Workspace = QtGui.QAction(MainWindow)
        self.actionSave_Workspace.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/trolltech/styles/commonstyle/images/standardbutton-save-32.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_Workspace.setIcon(icon5)
        self.actionSave_Workspace.setText(QtGui.QApplication.translate("MainWindow", "Save Workspace", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Workspace.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Workspace.setObjectName(_fromUtf8("actionSave_Workspace"))
        self.actionClose_Workspace = QtGui.QAction(MainWindow)
        self.actionClose_Workspace.setEnabled(False)
        self.actionClose_Workspace.setIcon(icon3)
        self.actionClose_Workspace.setText(QtGui.QApplication.translate("MainWindow", "Close Workspace", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose_Workspace.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+W", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose_Workspace.setObjectName(_fromUtf8("actionClose_Workspace"))
        self.actionNew_Workspace = QtGui.QAction(MainWindow)
        self.actionNew_Workspace.setText(QtGui.QApplication.translate("MainWindow", "New Workspace", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Workspace.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Workspace.setObjectName(_fromUtf8("actionNew_Workspace"))
        self.actionWindow_function = QtGui.QAction(MainWindow)
        self.actionWindow_function.setText(QtGui.QApplication.translate("MainWindow", "Window function", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWindow_function.setObjectName(_fromUtf8("actionWindow_function"))
        self.actionPhase = QtGui.QAction(MainWindow)
        self.actionPhase.setText(QtGui.QApplication.translate("MainWindow", "Phase", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPhase.setObjectName(_fromUtf8("actionPhase"))
        self.actionFFT = QtGui.QAction(MainWindow)
        self.actionFFT.setText(QtGui.QApplication.translate("MainWindow", "FFT from FID", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFFT.setObjectName(_fromUtf8("actionFFT"))
        self.actionLoad_spectrum = QtGui.QAction(MainWindow)
        self.actionLoad_spectrum.setText(QtGui.QApplication.translate("MainWindow", "Load spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_spectrum.setObjectName(_fromUtf8("actionLoad_spectrum"))
        self.actionHelp = QtGui.QAction(MainWindow)
        self.actionHelp.setText(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setObjectName(_fromUtf8("actionHelp"))
        self.actionAbout_SibunLabs_NMR = QtGui.QAction(MainWindow)
        self.actionAbout_SibunLabs_NMR.setText(QtGui.QApplication.translate("MainWindow", "About SibunLabs NMR", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_SibunLabs_NMR.setObjectName(_fromUtf8("actionAbout_SibunLabs_NMR"))
        self.actionFFT_from_spectrum = QtGui.QAction(MainWindow)
        self.actionFFT_from_spectrum.setEnabled(False)
        self.actionFFT_from_spectrum.setText(QtGui.QApplication.translate("MainWindow", "FFT⁻¹ from spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFFT_from_spectrum.setObjectName(_fromUtf8("actionFFT_from_spectrum"))
        self.actionSwitchView_FID = QtGui.QAction(MainWindow)
        self.actionSwitchView_FID.setCheckable(True)
        self.actionSwitchView_FID.setText(QtGui.QApplication.translate("MainWindow", "FID", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSwitchView_FID.setIconVisibleInMenu(True)
        self.actionSwitchView_FID.setObjectName(_fromUtf8("actionSwitchView_FID"))
        self.actionSwitchView_Spectrum = QtGui.QAction(MainWindow)
        self.actionSwitchView_Spectrum.setCheckable(True)
        self.actionSwitchView_Spectrum.setText(QtGui.QApplication.translate("MainWindow", "Spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSwitchView_Spectrum.setObjectName(_fromUtf8("actionSwitchView_Spectrum"))
        self.actionPaper_Settings = QtGui.QAction(MainWindow)
        self.actionPaper_Settings.setText(QtGui.QApplication.translate("MainWindow", "Print Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaper_Settings.setObjectName(_fromUtf8("actionPaper_Settings"))
        self.actionPrint_spectrum = QtGui.QAction(MainWindow)
        self.actionPrint_spectrum.setText(QtGui.QApplication.translate("MainWindow", "Print spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrint_spectrum.setObjectName(_fromUtf8("actionPrint_spectrum"))
        self.actionPrint_signals_only = QtGui.QAction(MainWindow)
        self.actionPrint_signals_only.setText(QtGui.QApplication.translate("MainWindow", "Print signals only", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrint_signals_only.setObjectName(_fromUtf8("actionPrint_signals_only"))
        self.actionClose_NMR = QtGui.QAction(MainWindow)
        self.actionClose_NMR.setIcon(icon3)
        self.actionClose_NMR.setText(QtGui.QApplication.translate("MainWindow", "Close NMR", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose_NMR.setObjectName(_fromUtf8("actionClose_NMR"))
        self.menuSibunLabs_NMR.addAction(self.actionNew_Workspace)
        self.menuSibunLabs_NMR.addAction(self.actionOpen_Workspace)
        self.menuSibunLabs_NMR.addSeparator()
        self.menuSibunLabs_NMR.addAction(self.actionSave_Workspace)
        self.menuSibunLabs_NMR.addSeparator()
        self.menuSibunLabs_NMR.addAction(self.actionClose_Workspace)
        self.menuSibunLabs_NMR.addAction(self.actionQuit)
        self.menuView.addAction(self.actionSwitchView_FID)
        self.menuView.addAction(self.actionSwitchView_Spectrum)
        self.menuSpectrum.addAction(self.menuView.menuAction())
        self.menuSpectrum.addSeparator()
        self.menuSpectrum.addAction(self.actionWindow_function)
        self.menuSpectrum.addAction(self.actionFFT_from_spectrum)
        self.menuSpectrum.addSeparator()
        self.menuSpectrum.addAction(self.actionLoad_spectrum)
        self.menuSpectrum.addAction(self.actionFFT)
        self.menuSpectrum.addAction(self.actionPhase)
        self.menuSpectrum.addSeparator()
        self.menuSpectrum.addAction(self.actionPaper_Settings)
        self.menuSpectrum.addAction(self.actionPrint_spectrum)
        self.menuSpectrum.addAction(self.actionPrint_signals_only)
        self.menuSpectrum.addSeparator()
        self.menuSpectrum.addAction(self.actionClose_NMR)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_SibunLabs_NMR)
        self.menubar.addAction(self.menuSibunLabs_NMR.menuAction())
        self.menubar.addAction(self.menuWorkspace.menuAction())
        self.menubar.addAction(self.menuSpectrum.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionPick_Peak)
        self.toolBar.addAction(self.actionIntegrate)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.close)
        QtCore.QObject.connect(self.experimentList, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QTreeWidgetItem*,int)")), MainWindow.onExperimentClicked)
        QtCore.QObject.connect(self.actionOpen_Workspace, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.onOpenWorkspace)
        QtCore.QObject.connect(self.actionClose_Workspace, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.onCloseWorkspace)
        QtCore.QObject.connect(self.actionSave_Workspace, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.onSaveWorkspace)
        QtCore.QObject.connect(self.actionSwitchView_FID, QtCore.SIGNAL(_fromUtf8("triggered(bool)")), MainWindow.onChangeViewToFid)
        QtCore.QObject.connect(self.actionSwitchView_Spectrum, QtCore.SIGNAL(_fromUtf8("triggered(bool)")), MainWindow.onChangeViewToSpectrum)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.experimentList.setSortingEnabled(True)

from nmrView import NMRView
