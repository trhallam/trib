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
        MainWindow.setStyleSheet("selection-color: rgb(139, 218, 249);\n"
"background-color: rgb(230, 230, 230);\n"
"border-color: rgb(93, 87, 107);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("selection-color: rgb(139, 218, 249);\n"
"background-color: rgb(230, 230, 230);\n"
"border-color: rgb(93, 87, 107);")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("selection-color: rgb(139, 218, 249);\n"
"background-color: rgb(230, 230, 230);\n"
"border-color: rgb(93, 87, 107);")
        self.tabWidget.setObjectName("tabWidget")
        self.tabFixedDist = QtWidgets.QWidget()
        self.tabFixedDist.setAutoFillBackground(False)
        self.tabFixedDist.setStyleSheet("selection-color: rgb(139, 218, 249);\n"
"background-color: rgb(230, 230, 230);\n"
"border-color: rgb(93, 87, 107);")
        self.tabFixedDist.setObjectName("tabFixedDist")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabFixedDist)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter = QtWidgets.QSplitter(self.tabFixedDist)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 6, 6, 6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayoutFD = QtWidgets.QVBoxLayout()
        self.verticalLayoutFD.setObjectName("verticalLayoutFD")
        self.horizontalLayout.addLayout(self.verticalLayoutFD)
        self.lineSplitterFixedDistr = QtWidgets.QFrame(self.layoutWidget)
        self.lineSplitterFixedDistr.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineSplitterFixedDistr.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineSplitterFixedDistr.setObjectName("lineSplitterFixedDistr")
        self.horizontalLayout.addWidget(self.lineSplitterFixedDistr)
        self.gridLayoutFDChart = QtWidgets.QGridLayout()
        self.gridLayoutFDChart.setObjectName("gridLayoutFDChart")
        self.horizontalLayout.addLayout(self.gridLayoutFDChart)
        self.gridLayout_2.addWidget(self.splitter, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tabFixedDist, "")
        self.tabSetDist = QtWidgets.QWidget()
        self.tabSetDist.setStyleSheet("selection-color: rgb(139, 218, 249);\n"
"background-color: rgb(230, 230, 230);\n"
"border-color: rgb(93, 87, 107);")
        self.tabSetDist.setObjectName("tabSetDist")
        self.tabWidget.addTab(self.tabSetDist, "")
        self.tabProbit = QtWidgets.QWidget()
        self.tabProbit.setStyleSheet("selection-color: rgb(139, 218, 249);\n"
"background-color: rgb(230, 230, 230);\n"
"border-color: rgb(93, 87, 107);")
        self.tabProbit.setObjectName("tabProbit")
        self.tabWidget.addTab(self.tabProbit, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 941, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
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
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionHelp)
        self.menuEdit.addAction(self.actionSettings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.actionExit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Trib"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFixedDist), _translate("MainWindow", "Fixed Distribution"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSetDist), _translate("MainWindow", "Set Distribution"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabProbit), _translate("MainWindow", "Probit Plot"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))

import qdesignResource_rc
