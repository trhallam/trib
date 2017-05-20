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

'''
Class to caputre the setup of the data input table.
'''

dummy_data_4testing = [0.08, 0.18, 0.19, 0.22, 0.38, 0.39, 0.83, 0.91, 1.62, 1.92, 1.93, 2.58, 3.2,
 3.43, 3.86, 3.87, 3.94, 3.95, 4.02, 4.14, 4.15, 4.22, 4.43, 4.6, 4.68, 4.78, 5.14, 5.52, 5.66,
 5.74, 6.89, 8.08, 8.3, 8.61, 8.76, 8.86, 9.24, 9.27, 9.56, 10.54, 11.64, 11.66, 12.46, 13.26, 14.1,
 14.48, 15.68, 15.72, 16.81, 18, 18.32, 18.54, 19.28, 20.56, 22.08, 23.8, 24.86, 27.12, 27.51,
 28.56, 30.08, 31.51, 35.62, 36.01, 36.1, 39.02, 39.09, 39.58, 40.14, 40.98, 41.05, 41.54, 43.01,
 43.93, 44.2, 44.76, 57.14, 67.12, 71.68, 72.01, 74.02, 76.68, 76.89, 82.16, 82.6, 85.12, 85.78,
 90.24, 92.44, 93.62, 94.51, 96.32, 99.22, 246.75]
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

        # Populate Input Distr Table

        self.inputHeaders = ['Point ID', 'Value']
        self.inputData = {}
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