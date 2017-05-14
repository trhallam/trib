"""tribMainWindow

This module contains classes for the creation the trib GUI main window. 
Classes inherrit from layouts designed in qt designer. 
make.py must be run in the tribgui module folder to update the gui interface.

"""

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

from tribgui._qtdesigner import qdesignMainWindow, qdesignDialogAbout
from widgetFDTable import widgetFDTable
from widgetFDChart import widgetFDChart

import webbrowser


'''
Class to capture the setup of the About Dialog.
'''


class aboutDialog(QtWidgets.QDialog, qdesignDialogAbout.Ui_dialogAbout):
    def __init__(self, parent=None):
        super(aboutDialog, self).__init__(parent)
        self.setupUi(self)

        self.pushButtonGitHub.clicked.connect(self.onIconClick)
        self.pushButtonLIn.clicked.connect(self.onIconClick)
        self.pushButtonIcon8.clicked.connect(self.onIconClick)

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


class mainApp(QtWidgets.QMainWindow, qdesignMainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainApp, self).__init__(parent)
        self.setupUi(self)

        # Connect Menu Actions to Other Windows
        self.actionAbout.triggered.connect(self._onActionAbout)
        self.aboutDialog = aboutDialog(self)

        self.w1 = widgetFDTable()
        self.verticalLayoutFD.addWidget(self.w1)


        self.c1 = widgetFDChart()
        self.gridLayoutFDChart.addWidget(self.c1)


        self.w1.actionDistrUpdated.connect(self.c1.updateChart)

        #chart displays on start
        self.w1._calcFixedDistr()


    def _onActionAbout(self):
        self.aboutDialog.show()


