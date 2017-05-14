# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '_qtdesigner\qdesignFDTables.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(348, 768)
        Form.setMinimumSize(QtCore.QSize(280, 460))
        Form.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.distributionValuesGroup = QtWidgets.QGroupBox(Form)
        self.distributionValuesGroup.setMinimumSize(QtCore.QSize(250, 250))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.distributionValuesGroup.setFont(font)
        self.distributionValuesGroup.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.distributionValuesGroup.setObjectName("distributionValuesGroup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.distributionValuesGroup)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableWidgetDistrValues = XParameterTableWidget(self.distributionValuesGroup)
        self.tableWidgetDistrValues.setStyleSheet("selection-color: rgb(93, 87, 107);\n"
"selection-background-color: rgb(139, 218, 249);\n"
"background-color: rgb(252, 252, 252);\n"
"border-color: rgb(93, 87, 107);\n"
"alternate-background-color: rgb(255, 250, 227);\n"
"font: 75 14pt \"Arial\";")
        self.tableWidgetDistrValues.setObjectName("tableWidgetDistrValues")
        self.tableWidgetDistrValues.setColumnCount(0)
        self.tableWidgetDistrValues.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidgetDistrValues, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.distributionValuesGroup, 2, 0, 1, 1)
        self.distributionDefBox = QtWidgets.QGroupBox(Form)
        self.distributionDefBox.setMinimumSize(QtCore.QSize(250, 210))
        self.distributionDefBox.setMaximumSize(QtCore.QSize(16777215, 210))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.distributionDefBox.setFont(font)
        self.distributionDefBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.distributionDefBox.setObjectName("distributionDefBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.distributionDefBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.comboBoxDist = QtWidgets.QComboBox(self.distributionDefBox)
        self.comboBoxDist.setStyleSheet("selection-color: rgb(93, 87, 107);\n"
"selection-background-color: rgb(139, 218, 249);\n"
"background-color: rgb(252, 252, 252);\n"
"border-color: rgb(93, 87, 107);\n"
"alternate-background-color: rgb(255, 250, 227);\n"
"font: 75 14pt \"Arial\";")
        self.comboBoxDist.setCurrentText("")
        self.comboBoxDist.setObjectName("comboBoxDist")
        self.gridLayout_3.addWidget(self.comboBoxDist, 0, 0, 1, 1)
        self.tableWidgetDistrInputs = XParameterTableWidget(self.distributionDefBox)
        self.tableWidgetDistrInputs.setStyleSheet("selection-color: rgb(93, 87, 107);\n"
"selection-background-color: rgb(139, 218, 249);\n"
"background-color: rgb(252, 252, 252);\n"
"border-color: rgb(93, 87, 107);\n"
"alternate-background-color: rgb(255, 250, 227);\n"
"font: 75 14pt \"Arial\";")
        self.tableWidgetDistrInputs.setObjectName("tableWidgetDistrInputs")
        self.tableWidgetDistrInputs.setColumnCount(0)
        self.tableWidgetDistrInputs.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableWidgetDistrInputs, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.distributionDefBox, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.distributionValuesGroup.setTitle(_translate("Form", "Distribution Values"))
        self.distributionDefBox.setTitle(_translate("Form", "Distribution Definition"))

from pyqt5x.XTableWidget import XParameterTableWidget
import qdesignResource_rc
