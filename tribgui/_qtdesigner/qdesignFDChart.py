# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '_qtdesigner\qdesignFDChart.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(471, 72)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonSettings = QtWidgets.QPushButton(Form)
        self.pushButtonSettings.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButtonSettings.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/charticons/icons/Settings_48px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonSettings.setIcon(icon)
        self.pushButtonSettings.setIconSize(QtCore.QSize(32, 32))
        self.pushButtonSettings.setFlat(True)
        self.pushButtonSettings.setObjectName("pushButtonSettings")
        self.horizontalLayout.addWidget(self.pushButtonSettings)
        self.pushButtonExpand = QtWidgets.QPushButton(Form)
        self.pushButtonExpand.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButtonExpand.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/charticons/icons/Expand_48px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonExpand.setIcon(icon1)
        self.pushButtonExpand.setIconSize(QtCore.QSize(30, 30))
        self.pushButtonExpand.setFlat(True)
        self.pushButtonExpand.setObjectName("pushButtonExpand")
        self.horizontalLayout.addWidget(self.pushButtonExpand)
        self.pushButtonZoom = QtWidgets.QPushButton(Form)
        self.pushButtonZoom.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButtonZoom.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/charticons/icons/Zoom In_48px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonZoom.setIcon(icon2)
        self.pushButtonZoom.setIconSize(QtCore.QSize(30, 30))
        self.pushButtonZoom.setFlat(True)
        self.pushButtonZoom.setObjectName("pushButtonZoom")
        self.horizontalLayout.addWidget(self.pushButtonZoom)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonExportPNG = QtWidgets.QPushButton(Form)
        self.pushButtonExportPNG.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButtonExportPNG.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/charticons/icons/PNG_48px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonExportPNG.setIcon(icon3)
        self.pushButtonExportPNG.setIconSize(QtCore.QSize(30, 30))
        self.pushButtonExportPNG.setFlat(True)
        self.pushButtonExportPNG.setObjectName("pushButtonExportPNG")
        self.horizontalLayout.addWidget(self.pushButtonExportPNG)
        self.pushButtonExportCSV = QtWidgets.QPushButton(Form)
        self.pushButtonExportCSV.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButtonExportCSV.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/charticons/icons/CSV_48px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonExportCSV.setIcon(icon4)
        self.pushButtonExportCSV.setIconSize(QtCore.QSize(30, 30))
        self.pushButtonExportCSV.setFlat(True)
        self.pushButtonExportCSV.setObjectName("pushButtonExportCSV")
        self.horizontalLayout.addWidget(self.pushButtonExportCSV)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

import qdesignResource_rc
