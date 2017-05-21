"""widgetIDTable

This module contains classes for the modification of the idtables widget 

"""

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal
try:
    from pyqt5x import XParameterTableWidget
except ImportError:
    from .. import env
    from pyqt5x import XParameterTableWidget

from tribgui.stylesheet import tribtablestyle
from numpy import random

'''
Class to caputre the setup of the data input table.
'''

dummy_data_4testing = list(random.lognormal(size=150,sigma=0.6))
dummy_data_names = list()
 
for i, dp in enumerate(dummy_data_4testing):
    dummy_data_names.append('ID_%02d'%i)

class widgetIDTable(QtWidgets.QWidget):

    # signals to communicate with other widgets through main window
    actionInputUpdated = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(widgetIDTable, self).__init__(parent)
        self.activeDistr = 'norm'
        
        self.setObjectName("Input Table")


        #self.resize(348, 768)
        # Sizing
        self.setMinimumSize(QtCore.QSize(300, 200))
        # self.setMaximumSize(QtCore.QSize(300, 5000))
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)
        self.gridLayout = QtWidgets.QGridLayout()
        self.setLayout(self.gridLayout)

        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tableWidgetInputValues = XParameterTableWidget()
        self.tableWidgetInputValues.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                                    QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addWidget(self.tableWidgetInputValues)
        tribtablestyle(self.tableWidgetInputValues)

        # Populate Input Distr Table

        self.inputHeaders = ['Point ID', 'Value']
        self.inputData = {}
        rand = random.lognormal(size=100, mean=10, sigma=0.6)
        self.inputData[self.inputHeaders[0]]=dummy_data_names
        self.inputData[self.inputHeaders[1]]=dummy_data_4testing
        self.currentInput = self.inputData
        self.tableColRatio = 0.5
        self.tableWidgetInputValues.setdata(self.currentInput)

        # monitors for changes to output table
        self.tableWidgetInputValues.itemChanged.connect(self.onTableEdited)

        # monitors resizing of window
        # self.tableWidgetDistrValues.resizeEvent(self.onTableResize)

        #self.tableWidgetDistrInput.setCurrentCell(0, 0)

    def _checkInputRow(self, row):

        self.tableWidgetInputValues.setCurrentCell(row, 1)
        var = self.tableWidgetInputValues.currentItem().text()

        try: #check for numerical value
            float(var)
            # return all data send to histogram
        except ValueError:
            self.tableWidgetInputValues.currentItem().setBackground(QtGui.QColor(255, 154, 145))
            self._setRowColour(self.tableWidgetInputValues, row, QtGui.QColor(255, 154, 145))
            var = None
            
        if row == self.tableWidgetInputValues.rowCount() - 1:
            self.tableWidgetInputValues.addrow()

        self.tableWidgetInputValues.setCurrentCell(row, 1)
        if var != None:
            self._setRowColour(self.tableWidgetInputValues, row, QtGui.QColor(255, 255, 255))

    def _setRowColour(self, table, row, colour):
        # QTableWidget, int, QColor
        nclm = table.columnCount()
        for ind in range(0, nclm):
            table.setCurrentCell(row, ind)
            table.currentItem().setBackground(colour)

    def _cleandata(self):
        cleandata = dict()
        values = list(); ids = list()
        for i, val in enumerate(self.data['Value']):
            try:
                values.append(float(val)); ids.append(self.data['Point ID'][i])
            except ValueError:
                continue
        cleandata['Value']=values; cleandata['Point ID']=ids
        return cleandata

    # special pyqt slots
    @pyqtSlot()
    def onTableEdited(self):
        inrow = self.tableWidgetInputValues.currentRow()
        incol = self.tableWidgetInputValues.currentColumn()

        self.tableWidgetInputValues.itemChanged.disconnect()
        self._checkInputRow(inrow)
        self.tableWidgetInputValues.itemChanged.connect(self.onTableEdited)

        self.tableWidgetInputValues.setCurrentCell(inrow, incol)
        self.data=self.tableWidgetInputValues.returndata()
        self.tableWidgetInputValues.setCurrentCell(inrow, incol)
        self.actionInputUpdated.emit(self._cleandata())

    @pyqtSlot()
    def onDataRequest(self):
        inrow = self.tableWidgetInputValues.currentRow()
        incol = self.tableWidgetInputValues.currentColumn()

        self.data=self.tableWidgetInputValues.returndata()
        self.tableWidgetInputValues.setCurrentCell(inrow, incol)
        self.actionInputUpdated.emit(self._cleandata())

def main():
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)
    # chartView.chart.addLinearReg()
    idtable = widgetIDTable()
    window = QMainWindow()
    window.setCentralWidget(idtable)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()