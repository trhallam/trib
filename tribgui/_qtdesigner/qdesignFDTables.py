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
        Form.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.distributionDefBox = QtWidgets.QGroupBox(self.splitter)
        self.distributionDefBox.setMinimumSize(QtCore.QSize(250, 210))
        self.distributionDefBox.setMaximumSize(QtCore.QSize(16777215, 210))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.distributionDefBox.setFont(font)
        self.distributionDefBox.setStyleSheet("")
        self.distributionDefBox.setObjectName("distributionDefBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.distributionDefBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.comboBoxDist = QtWidgets.QComboBox(self.distributionDefBox)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setKerning(False)
        self.comboBoxDist.setFont(font)
        self.comboBoxDist.setStyleSheet("")
        self.comboBoxDist.setCurrentText("")
        self.comboBoxDist.setObjectName("comboBoxDist")
        self.gridLayout_3.addWidget(self.comboBoxDist, 0, 0, 1, 1)
        self.tableWidgetDistrInputs = XParameterTableWidget(self.distributionDefBox)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tableWidgetDistrInputs.setFont(font)
        self.tableWidgetDistrInputs.setStyleSheet("")
        self.tableWidgetDistrInputs.setObjectName("tableWidgetDistrInputs")
        self.tableWidgetDistrInputs.setColumnCount(0)
        self.tableWidgetDistrInputs.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableWidgetDistrInputs, 1, 0, 1, 1)
        self.distributionValuesGroup = QtWidgets.QGroupBox(self.splitter)
        self.distributionValuesGroup.setMinimumSize(QtCore.QSize(250, 250))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.distributionValuesGroup.setFont(font)
        self.distributionValuesGroup.setStyleSheet("")
        self.distributionValuesGroup.setObjectName("distributionValuesGroup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.distributionValuesGroup)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableWidgetDistrValues = XParameterTableWidget(self.distributionValuesGroup)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tableWidgetDistrValues.setFont(font)
        self.tableWidgetDistrValues.setStyleSheet("")
        self.tableWidgetDistrValues.setObjectName("tableWidgetDistrValues")
        self.tableWidgetDistrValues.setColumnCount(0)
        self.tableWidgetDistrValues.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidgetDistrValues, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.distributionDefBox.setTitle(_translate("Form", "Distribution Definition"))
        self.distributionValuesGroup.setTitle(_translate("Form", "Distribution Values"))

from pyqt5x.XTableWidget import XParameterTableWidget
import qdesignResource_rc
