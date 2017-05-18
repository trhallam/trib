"""tribMainWindow

This module contains classes for the creation the trib GUI main window. 
Classes inherrit from layouts designed in qt designer. 
make.py must be run in the tribgui module folder to update the gui interface.

"""

import json
from os.path import expanduser, join

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from tribgui.widgets import (widgetFDChart, widgetIDChart,
                            widgetIDTable, widgetFDTable)

from tribgui._qtdesigner import qdesignMainWindow, qdesignDialogAbout
from tribgui import widgets


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

        # global variables
        self.userhome = join(expanduser("~"),'Documents')

        # Connect Menu Actions to Other Windows
        # File
        self.actionNew.triggered.connect(self._onActionNew)
        self.actionOpen.triggered.connect(self._onActionOpen)
        self.actionOpen_Recent.triggered.connect(self._onActionOpenRecent)
        self.actionSave_Session.triggered.connect(self._onActionSaveSession)
        self.actionSave_Session_As.triggered.connect(self._onActionSaveSessionAs)

        # About
        self.actionAbout.triggered.connect(self._onActionAbout)
        self.aboutDialog = aboutDialog(self)

        # Fixed Distribution Tab
        # Fixed Distribution Tables
        self.wFDTable = widgetFDTable()
        self.verticalLayoutFD.addWidget(self.wFDTable)

        # Fixed Distribution Chart
        self.wFDChart = widgetFDChart()
        self.gridLayoutFDChart.addWidget(self.wFDChart)

        # Input Distribution Tab
        # Input Distribution Table
        self.wIDTable = widgetIDTable()

        self.verticalLayoutIDLeft.addWidget(self.wIDTable)

        # Histogram Widget
        self.wIDChart = widgetIDChart()
        self.gridLayoutHist.addWidget(self.wIDChart)

        # Connect Widgets
        self.wIDTable.actionInputUpdated.connect(self.wIDChart.receiveFromTable)
        #self.wIDTable.onTableEdited()
        #self.w1.actionDistrUpdated.connect(self.c1.updateChart)

        #chart displays on start
        #self.w1._calcFixedDistr()

    def saveSession(self, file):
        outputdict = dict()
        settingsdict = dict()

        outputdict['fdtableInput'] = self.wFDTable.fixedInputData
        outputdict['fdtableOutput'] = self.wFDTable.fixedDistrData

        with open(file, 'w') as fp:
            json.dump(outputdict, fp, sort_keys=True, indent=4)
            fp.close()

    def openSession(self, file):

        with open(file, 'r') as fp:
            inputdict = json.load(fp)
            fp.close

        self.wFDTable.fixedInputData = inputdict['fdtableInput']
        self.wFDTable.fixedDistrData = inputdict['fdtableOutput']

    def _onActionAbout(self):
        self.aboutDialog.show()

    def _onActionNew(self):
        pass


    def _onActionOpen(self):
        self.sessionfile = QtWidgets.QFileDialog.getOpenFileName(self,
                caption='Open File', directory = self.userhome, filter='*.json')
        try:
            self.openSession(self.sessionfile[0])
        except PermissionError:
            pass

    def _onActionOpenRecent(self):
        '''
        Will contian users X most recent sessions to Open
        '''
        pass

    def _onActionSaveSession(self):
        try:
            if self.openFileName: #check session file is already open
                pass #write something to save the session to the open file name
        except:
            self._onActionSaveSessionAs()

    def _onActionSaveSessionAs(self):
        self.sessionfile = QtWidgets.QFileDialog.getSaveFileName(self,
                caption = 'Save Session As', directory = self.userhome, filter='*.json')
        self.saveSession(*self.sessionfile[0])