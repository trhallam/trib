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
        Form.resize(391, 662)
        Form.setMinimumSize(QtCore.QSize(280, 460))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.distributionDefBox = QtWidgets.QGroupBox(Form)
        self.distributionDefBox.setMinimumSize(QtCore.QSize(250, 180))
        self.distributionDefBox.setMaximumSize(QtCore.QSize(16777215, 180))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.distributionDefBox.setFont(font)
        self.distributionDefBox.setObjectName("distributionDefBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.distributionDefBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBoxDist = QtWidgets.QComboBox(self.distributionDefBox)
        self.comboBoxDist.setStyleSheet("selection-color: rgb(93, 87, 107);\n"
"selection-background-color: rgb(139, 218, 249);\n"
"background-color: rgb(252, 252, 252);\n"
"border-color: rgb(93, 87, 107);\n"
"alternate-background-color: rgb(255, 250, 227);\n"
"font: 75 14pt \"Arial\";")
        self.comboBoxDist.setCurrentText("")
        self.comboBoxDist.setObjectName("comboBoxDist")
        self.verticalLayout.addWidget(self.comboBoxDist)
        self.horizontalLayoutLabel = QtWidgets.QHBoxLayout()
        self.horizontalLayoutLabel.setContentsMargins(-1, 2, -1, 2)
        self.horizontalLayoutLabel.setObjectName("horizontalLayoutLabel")
        self.labelProb = QtWidgets.QLabel(self.distributionDefBox)
        self.labelProb.setMinimumSize(QtCore.QSize(110, 20))
        self.labelProb.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        self.labelProb.setFont(font)
        self.labelProb.setAlignment(QtCore.Qt.AlignCenter)
        self.labelProb.setObjectName("labelProb")
        self.horizontalLayoutLabel.addWidget(self.labelProb)
        self.labelValue = QtWidgets.QLabel(self.distributionDefBox)
        self.labelValue.setMinimumSize(QtCore.QSize(110, 20))
        self.labelValue.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        self.labelValue.setFont(font)
        self.labelValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelValue.setObjectName("labelValue")
        self.horizontalLayoutLabel.addWidget(self.labelValue)
        self.verticalLayout.addLayout(self.horizontalLayoutLabel)
        self.horizontalLayout1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout1.setObjectName("horizontalLayout1")
        self.lineEditProb1 = QtWidgets.QLineEdit(self.distributionDefBox)
        self.lineEditProb1.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEditProb1.setStyleSheet("selection-color: rgb(93, 87, 107);\n"
"selection-background-color: rgb(139, 218, 249);\n"
"background-color: rgb(252, 252, 252);\n"
"border-color: rgb(93, 87, 107);\n"
"alternate-background-color: rgb(255, 250, 227);\n"
"font: 75 14pt \"Arial\";")
        self.lineEditProb1.setMaxLength(5)
        self.lineEditProb1.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditProb1.setClearButtonEnabled(False)
        self.lineEditProb1.setObjectName("lineEditProb1")
        self.horizontalLayout1.addWidget(self.lineEditProb1)
        self.labeldots1 = QtWidgets.QLabel(self.distributionDefBox)
        self.labeldots1.setMinimumSize(QtCore.QSize(10, 45))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        self.labeldots1.setFont(font)
        self.labeldots1.setAlignment(QtCore.Qt.AlignCenter)
        self.labeldots1.setObjectName("labeldots1")
        self.horizontalLayout1.addWidget(self.labeldots1)
        self.lineEditValue1 = QtWidgets.QLineEdit(self.distributionDefBox)
        self.lineEditValue1.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEditValue1.setStyleSheet("selection-color: rgb(139, 218, 249);\n"
"background-color: rgb(252, 252, 252);\n"
"border-color: rgb(93, 87, 107);\n"
"alternate-background-color: rgb(255, 250, 227);\n"
"font: 75 14pt \"Arial\";")
        self.lineEditValue1.setMaxLength(10)
        self.lineEditValue1.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditValue1.setPlaceholderText("")
        self.lineEditValue1.setClearButtonEnabled(False)
        self.lineEditValue1.setObjectName("lineEditValue1")
        self.horizontalLayout1.addWidget(self.lineEditValue1)
        self.verticalLayout.addLayout(self.horizontalLayout1)
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        self.lineEditProb2 = QtWidgets.QLineEdit(self.distributionDefBox)
        self.lineEditProb2.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEditProb2.setStyleSheet("selection-color: rgb(139, 218, 249);\n"
"background-color: rgb(252, 252, 252);\n"
"border-color: rgb(93, 87, 107);\n"
"alternate-background-color: rgb(255, 250, 227);\n"
"font: 75 14pt \"Arial\";")
        self.lineEditProb2.setMaxLength(5)
        self.lineEditProb2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditProb2.setClearButtonEnabled(False)
        self.lineEditProb2.setObjectName("lineEditProb2")
        self.horizontalLayout2.addWidget(self.lineEditProb2)
        self.labeldots2 = QtWidgets.QLabel(self.distributionDefBox)
        self.labeldots2.setMinimumSize(QtCore.QSize(10, 45))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        self.labeldots2.setFont(font)
        self.labeldots2.setAlignment(QtCore.Qt.AlignCenter)
        self.labeldots2.setObjectName("labeldots2")
        self.horizontalLayout2.addWidget(self.labeldots2)
        self.lineEditValue2 = QtWidgets.QLineEdit(self.distributionDefBox)
        self.lineEditValue2.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEditValue2.setStyleSheet("selection-color: rgb(139, 218, 249);\n"
"background-color: rgb(252, 252, 252);\n"
"border-color: rgb(93, 87, 107);\n"
"alternate-background-color: rgb(255, 250, 227);\n"
"font: 75 14pt \"Arial\";")
        self.lineEditValue2.setMaxLength(10)
        self.lineEditValue2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditValue2.setPlaceholderText("")
        self.lineEditValue2.setClearButtonEnabled(False)
        self.lineEditValue2.setObjectName("lineEditValue2")
        self.horizontalLayout2.addWidget(self.lineEditValue2)
        self.verticalLayout.addLayout(self.horizontalLayout2)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.distributionDefBox, 0, 0, 1, 1)
        self.distributionValuesGroup = QtWidgets.QGroupBox(Form)
        self.distributionValuesGroup.setMinimumSize(QtCore.QSize(250, 250))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.distributionValuesGroup.setFont(font)
        self.distributionValuesGroup.setStyleSheet("")
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
        self.gridLayout_2.addWidget(self.tableWidgetDistrValues, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.distributionValuesGroup, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.distributionDefBox.setTitle(_translate("Form", "Distribution Definition"))
        self.labelProb.setText(_translate("Form", "Probability"))
        self.labelValue.setText(_translate("Form", "Value"))
        self.lineEditProb1.setToolTip(_translate("Form", "Enter probability between 0 and 100"))
        self.lineEditProb1.setText(_translate("Form", "0.9"))
        self.lineEditProb1.setPlaceholderText(_translate("Form", "90"))
        self.labeldots1.setText(_translate("Form", ":"))
        self.lineEditValue1.setToolTip(_translate("Form", "Enter probability associated value"))
        self.lineEditValue1.setText(_translate("Form", "11.667"))
        self.lineEditProb2.setToolTip(_translate("Form", "Enter probability between 0 and 100"))
        self.lineEditProb2.setText(_translate("Form", "0.1"))
        self.lineEditProb2.setPlaceholderText(_translate("Form", "10"))
        self.labeldots2.setText(_translate("Form", ":"))
        self.lineEditValue2.setToolTip(_translate("Form", "Enter probability associated value"))
        self.lineEditValue2.setText(_translate("Form", "20.55"))
        self.distributionValuesGroup.setTitle(_translate("Form", "Distribution Values"))

from pyqt5x.XTableWidget import XParameterTableWidget
import qdesignResource_rc
