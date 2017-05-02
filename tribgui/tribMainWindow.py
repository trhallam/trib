"""tribMainWindow

This module contains classes for the creation the trib GUI main window. 
Classes inherrit from layouts designed in qt designer. 
make.py must be run in the tribgui module folder to update the gui interface.

"""

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

from tribgui._qtdesigner import tribDesignMainWindow, tribDesignDialogAbout
from tribWidgetFDTable import tribWidgetFDTable

import webbrowser


'''
Class to capture the setup of the About Dialog.
'''


class tribAboutDialog(QtWidgets.QDialog, tribDesignDialogAbout.Ui_dialogAbout):
    def __init__(self, parent=None):
        super(tribAboutDialog, self).__init__(parent)
        self.setupUi(self)

        self.pushButtonGitHub.clicked.connect(self.onIconClick)
        self.pushButtonLIn.clicked.connect(self.onIconClick)

    @pyqtSlot()
    def onIconClick(self):
        sender=self.sender()
        tooltip = sender.toolTip()
        try:
            webbrowser.open_new_tab(tooltip[2+tooltip.find(':'):])
        except webbrowser.Error:
            pass

'''
Class to caputre the setup of the main window.
'''


class tribMainApp(QtWidgets.QMainWindow, tribDesignMainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(tribMainApp, self).__init__(parent)
        self.setupUi(self)

        # Connect Menu Actions to Other Windows
        self.actionAbout.triggered.connect(self._onActionAbout)
        self.aboutDialog = tribAboutDialog(self)

        self.w1 = tribWidgetFDTable()
        self.verticalLayoutFD.addWidget(self.w1)

    def _onActionAbout(self):
        self.aboutDialog.show()