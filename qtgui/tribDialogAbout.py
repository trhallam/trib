# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '_qtdesigner\tribDialogAbout.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialogAbout(object):
    def setupUi(self, dialogAbout):
        dialogAbout.setObjectName("dialogAbout")
        dialogAbout.resize(364, 260)
        self.pushButton = QtWidgets.QPushButton(dialogAbout)
        self.pushButton.setGeometry(QtCore.QRect(110, 230, 150, 23))
        self.pushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.layoutWidget = QtWidgets.QWidget(dialogAbout)
        self.layoutWidget.setGeometry(QtCore.QRect(1, 7, 361, 211))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTitle = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.labelTitle.setFont(font)
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle.setObjectName("labelTitle")
        self.verticalLayout.addWidget(self.labelTitle)
        self.labelDisc = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.labelDisc.setFont(font)
        self.labelDisc.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDisc.setObjectName("labelDisc")
        self.verticalLayout.addWidget(self.labelDisc)
        self.labelAuthor = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.labelAuthor.setFont(font)
        self.labelAuthor.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAuthor.setObjectName("labelAuthor")
        self.verticalLayout.addWidget(self.labelAuthor)
        self.labelYear = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.labelYear.setFont(font)
        self.labelYear.setAlignment(QtCore.Qt.AlignCenter)
        self.labelYear.setObjectName("labelYear")
        self.verticalLayout.addWidget(self.labelYear)
        spacerItem = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout.setStretch(0, 3)

        self.retranslateUi(dialogAbout)
        self.pushButton.released.connect(dialogAbout.close)
        QtCore.QMetaObject.connectSlotsByName(dialogAbout)

    def retranslateUi(self, dialogAbout):
        _translate = QtCore.QCoreApplication.translate
        dialogAbout.setWindowTitle(_translate("dialogAbout", "Trib- About"))
        self.pushButton.setText(_translate("dialogAbout", "OK"))
        self.labelTitle.setText(_translate("dialogAbout", "trib"))
        self.labelDisc.setText(_translate("dialogAbout", "A program to help calculate distribution statistics"))
        self.labelAuthor.setText(_translate("dialogAbout", "Created by: Tony Hallam"))
        self.labelYear.setText(_translate("dialogAbout", "2017"))

