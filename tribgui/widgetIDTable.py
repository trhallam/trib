"""widgetIDTable

This module contains classes for the modification of the idtables widget 

"""

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal
try:
	from pyqt5x import XTableWidget
except ImportError:
	from .. import env
	from pyqt5x import XTableWidget

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

class widgetIDTable(XTableWidget):

    # signals to communicate with other widgets through main window
    #actionDistrUpdated = pyqtSignal(list)

    def __init__(self, parent=None):
        super(widgetIDTable, self).__init__(parent)
        
        # Populate Input Distr Table

        self.fixedDistrHeaders = ['Point ID', 'Value']
        self.fixedDistrData = {}
        self.fixedDistrData[self.fixedDistrHeaders[0]]=dummy_data_names
        self.fixedDistrData[self.fixedDistrHeaders[1]]=dummy_data_4testing
        self.basicOutputs = self.fixedDistrData
        self.tableColRatio = 0.5
        self.tableWidgetDistrValues.setdata(self.basicOutputs)
#        self._calcFixedDistrTable()

        # monitors for distribution input boxes
#        self.comboBoxDist.currentIndexChanged.connect(self.onFixedDistrEdited)

        # monitors for changes to output table

#        self.tableWidgetDistrValues.itemChanged.connect(self.onTableEdited) #moved to _calcDistrRow


        # monitors resizing of window
        # self.tableWidgetDistrValues.resizeEvent(self.onTableResize)

        self.tableWidgetDistrValues.setCurrentCell(0, 0)

    # functions for Fixed Distribution Tab

'''
    def _getFixedDistrValues(self):
        self.fixedDistr = {}
#        self.fixedDistr[self.lineEditProb1.text()] = self.lineEditValue1.text()
#        self.fixedDistr[self.lineEditProb2.text()] = self.lineEditValue2.text()

    def _calcFixedDistr(self):
        fdistpoints = dict()
        for i, key in enumerate(self.fixedDistr.keys()):
            fdistpoints['p'+str(i)] = 1 - float(key)
            fdistpoints['f'+str(i)] = float(self.fixedDistr[key])

        self.kstats = distr.invdistr(self.activeDistr, **fdistpoints)
        self.kstats = distr.distrstats(self.activeDistr,**self.kstats)
        self.actionDistrUpdated.emit([self.activeDistr, self.kstats])

    def _calcFixedDistrRow(self, row):

        self.tableWidgetDistrValues.setCurrentCell(row, 0)
        var = self.tableWidgetDistrValues.currentItem().text()

        if var in self.kstats:
            val = self.kstats[var]

        else:
            try:
                pc = float(var)
                if 0.0 < pc < 1.0:
                    if self.activeDistr == 'norm':
                        val = stats.norm.ppf(1 - pc, loc=self.kstats['mu'], scale=self.kstats['std'])
                    elif self.activeDistr == 'lognorm':
                        val = stats.lognorm.ppf(1 - pc, self.kstats['shp'], scale=exp(self.kstats['mu']))
                    else:
                        raise ValueError
                else:
                    raise ValueError
            except ValueError:
                self.tableWidgetDistrValues.currentItem().setBackground(QtGui.QColor(255, 154, 145))
                self._setRowColour(self.tableWidgetDistrValues, row, QtGui.QColor(255, 154, 145))
                val = '#N/A'

        # print('_calcFixedDistrRow', row, var, val)
        # check if last row and add another if needed
        if row == self.tableWidgetDistrValues.rowCount() - 1:
            self.tableWidgetDistrValues.addrow()
            # self.tableWidgetDistrValues.setSelection()

        self.tableWidgetDistrValues.setCurrentCell(row, 1)
        self.tableWidgetDistrValues.currentItem().setText(str(val))
        if val != '#N/A':
            self._setRowColour(self.tableWidgetDistrValues, row, QtGui.QColor(255, 255, 255))

    def _calcFixedDistrTable(self):
        nrows = self.tableWidgetDistrValues.rowCount() - 1
        for row in range(0, nrows):
            self._calcFixedDistrRow(row)

    def _setRowColour(self, table, row, colour):
        # QTableWidget, int, QColor
        nclm = table.columnCount()
        for ind in range(0, nclm):
            table.setCurrentCell(row, ind)
            table.currentItem().setBackground(colour)

    def _togColEditable(self, table, clm):
        nrows = self.tableWidgetDistrValues.rowCount() - 1
        for row in range(0, nrows):
            table.setCurrentCell(row, clm)
            table.currentItem().setFlags(QtCore.Qt.ItemIsEditable)

    # special pyqt slots

    @pyqtSlot()
    def onChangeDistribution(self):
        self.activeDistr=self.distrTypes[self.comboBoxDist.currentText()]
        self.onFixedDistrEdited()

    @pyqtSlot()
    def onFixedDistrEdited(self):
        self._getFixedDistrValues()
        self._calcFixedDistr()

        self.tableWidgetDistrValues.itemChanged.disconnect()
        self._calcFixedDistrTable()
        self.tableWidgetDistrValues.itemChanged.connect(self.onTableEdited)

    @pyqtSlot()
    def onTableEdited(self):
        inrow = self.tableWidgetDistrValues.currentRow()
        incol = self.tableWidgetDistrValues.currentColumn()

        self.tableWidgetDistrValues.itemChanged.disconnect()
        self._calcFixedDistrRow(inrow)
        self.tableWidgetDistrValues.itemChanged.connect(self.onTableEdited)

        self.tableWidgetDistrValues.setCurrentCell(inrow, incol)
        data=self.tableWidgetDistrValues.returndata()

        self.tableWidgetDistrValues.setCurrentCell(inrow, incol)
'''

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