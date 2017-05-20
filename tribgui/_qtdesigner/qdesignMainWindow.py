# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '_qtdesigner\qdesignMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(941, 642)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/CDFPlot.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolTipDuration(2)
        MainWindow.setStyleSheet("background-color: rgb(250, 250, 250);\n"
"selection-background-color: rgb(139, 218, 249);\n"
"border-color: rgb(93, 87, 107);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("selection-color: rgb(139, 218, 249);\n"
"background-color: rgb(250, 250, 250);\n"
"border-color: rgb(93, 87, 107);")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("selection-background-color: rgb(139, 218, 249);\n"
"selection-color: rgb(0,0,0);\n"
"background-color: rgb(250, 250, 250);\n"
"border-color: rgb(93, 87, 107);")
        self.tabWidget.setObjectName("tabWidget")
        self.tabFixedDist = QtWidgets.QWidget()
        self.tabFixedDist.setAutoFillBackground(False)
        self.tabFixedDist.setStyleSheet("selection-color: rgb(139, 218, 249);\n"
"background-color: rgb(250, 250, 250);\n"
"border-color: rgb(93, 87, 107);")
        self.tabFixedDist.setObjectName("tabFixedDist")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabFixedDist)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter = QtWidgets.QSplitter(self.tabFixedDist)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayoutFD = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayoutFD.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutFD.setObjectName("verticalLayoutFD")
        self.lineSplitterFixedDistr = QtWidgets.QFrame(self.splitter)
        self.lineSplitterFixedDistr.setMinimumSize(QtCore.QSize(20, 0))
        self.lineSplitterFixedDistr.setMaximumSize(QtCore.QSize(20, 16777215))
        self.lineSplitterFixedDistr.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineSplitterFixedDistr.setLineWidth(2)
        self.lineSplitterFixedDistr.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineSplitterFixedDistr.setObjectName("lineSplitterFixedDistr")
        self.widget1 = QtWidgets.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")
        self.gridLayoutFDChart = QtWidgets.QGridLayout(self.widget1)
        self.gridLayoutFDChart.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutFDChart.setObjectName("gridLayoutFDChart")
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabFixedDist, "")
        self.tabInputDist = QtWidgets.QWidget()
        self.tabInputDist.setMinimumSize(QtCore.QSize(20, 0))
        self.tabInputDist.setStyleSheet("selection-color: rgb(139, 218, 249);\n"
"background-color: rgb(250, 250, 250);\n"
"border-color: rgb(93, 87, 107);")
        self.tabInputDist.setObjectName("tabInputDist")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabInputDist)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter_2 = QtWidgets.QSplitter(self.tabInputDist)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setMinimumSize(QtCore.QSize(20, 0))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter_2)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayoutIDLeft = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayoutIDLeft.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutIDLeft.setObjectName("verticalLayoutIDLeft")
        self.lineSplitterSetDistr = QtWidgets.QFrame(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineSplitterSetDistr.sizePolicy().hasHeightForWidth())
        self.lineSplitterSetDistr.setSizePolicy(sizePolicy)
        self.lineSplitterSetDistr.setMinimumSize(QtCore.QSize(10, 0))
        self.lineSplitterSetDistr.setMaximumSize(QtCore.QSize(10, 10000000))
        self.lineSplitterSetDistr.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineSplitterSetDistr.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineSplitterSetDistr.setObjectName("lineSplitterSetDistr")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutIDRight = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutIDRight.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutIDRight.setObjectName("verticalLayoutIDRight")
        self.tabWidgetID = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.tabWidgetID.setMinimumSize(QtCore.QSize(600, 300))
        self.tabWidgetID.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidgetID.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidgetID.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidgetID.setObjectName("tabWidgetID")
        self.tabStats = QtWidgets.QWidget()
        self.tabStats.setObjectName("tabStats")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tabStats)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayoutStats = QtWidgets.QGridLayout()
        self.gridLayoutStats.setObjectName("gridLayoutStats")
        self.gridLayout_7.addLayout(self.gridLayoutStats, 0, 0, 1, 1)
        self.tabWidgetID.addTab(self.tabStats, "")
        self.tabHist = QtWidgets.QWidget()
        self.tabHist.setObjectName("tabHist")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tabHist)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayoutHist = QtWidgets.QGridLayout()
        self.gridLayoutHist.setObjectName("gridLayoutHist")
        self.gridLayout_4.addLayout(self.gridLayoutHist, 0, 0, 1, 1)
        self.tabWidgetID.addTab(self.tabHist, "")
        self.tabProbit = QtWidgets.QWidget()
        self.tabProbit.setObjectName("tabProbit")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tabProbit)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayoutProbit = QtWidgets.QGridLayout()
        self.gridLayoutProbit.setObjectName("gridLayoutProbit")
        self.gridLayout_6.addLayout(self.gridLayoutProbit, 0, 0, 1, 1)
        self.tabWidgetID.addTab(self.tabProbit, "")
        self.verticalLayoutIDRight.addWidget(self.tabWidgetID)
        self.gridLayout_3.addWidget(self.splitter_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabInputDist, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 941, 22))
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.menubar.setFont(font)
        self.menubar.setStyleSheet("font: 10pt \"HoloLens MDL2 Assets\";")
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        self.menuFile.setFont(font)
        self.menuFile.setStyleSheet("font: 9pt \"HoloLens MDL2 Assets\";")
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/menuicons/icons/Exit_64px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon1)
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        font.setPointSize(9)
        self.actionExit.setFont(font)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        font.setPointSize(9)
        self.actionAbout.setFont(font)
        self.actionAbout.setObjectName("actionAbout")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        font.setPointSize(9)
        self.actionHelp.setFont(font)
        self.actionHelp.setObjectName("actionHelp")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/menuicons/icons/Settings_64px_grey.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon2)
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.actionSettings.setFont(font)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSave_Session = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/menuicons/icons/Save_64px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_Session.setIcon(icon3)
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        font.setPointSize(9)
        self.actionSave_Session.setFont(font)
        self.actionSave_Session.setObjectName("actionSave_Session")
        self.actionSave_Session_As = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/menuicons/icons/Save as_64px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_Session_As.setIcon(icon4)
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        font.setPointSize(9)
        self.actionSave_Session_As.setFont(font)
        self.actionSave_Session_As.setObjectName("actionSave_Session_As")
        self.actionNew = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/menuicons/icons/Create New_64px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon5)
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        font.setPointSize(9)
        self.actionNew.setFont(font)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/menuicons/icons/Open Folder_64px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon6)
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        font.setPointSize(9)
        self.actionOpen.setFont(font)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen_Recent = QtWidgets.QAction(MainWindow)
        self.actionOpen_Recent.setIcon(icon6)
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        font.setPointSize(9)
        self.actionOpen_Recent.setFont(font)
        self.actionOpen_Recent.setObjectName("actionOpen_Recent")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionOpen_Recent)
        self.menuFile.addAction(self.actionSave_Session)
        self.menuFile.addAction(self.actionSave_Session_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionHelp)
        self.menuEdit.addAction(self.actionSettings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidgetID.setCurrentIndex(0)
        self.actionExit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Trib"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFixedDist), _translate("MainWindow", "Fixed Distribution"))
        self.tabWidgetID.setTabText(self.tabWidgetID.indexOf(self.tabStats), _translate("MainWindow", "Stats"))
        self.tabWidgetID.setTabText(self.tabWidgetID.indexOf(self.tabHist), _translate("MainWindow", "Histogram"))
        self.tabWidgetID.setTabText(self.tabWidgetID.indexOf(self.tabProbit), _translate("MainWindow", "Probit"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabInputDist), _translate("MainWindow", "Input Distribution"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionSave_Session.setText(_translate("MainWindow", "Save Session"))
        self.actionSave_Session_As.setText(_translate("MainWindow", "Save Session As"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen_Recent.setText(_translate("MainWindow", "Open Recent"))

import qdesignResource_rc
