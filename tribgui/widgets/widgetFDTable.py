"""widgetFDTable

This module contains classes for the modification of the fdtables widget 
Classes inherit from layouts designed in qt designer. 
make.py must be run in the tribgui module folder to update the gui interface.

"""

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from tribgui._qtdesigner import qdesignFDTables
from tribgui.stylesheet import tribtablestyle
from tribgui.stylesheet import tablecolourflagstyle

from tufpy.stats import distr
from tufpy.utils import strictly_increasing

from scipy import stats
import numpy as np

'''
Class to caputre the setup of the main window.
'''


class widgetFDTable(QtWidgets.QWidget, qdesignFDTables.Ui_Form):

    # signals to communicate with other widgets through main window
    actionDistrUpdated = pyqtSignal(list)

    def __init__(self, parent=None):
        super(widgetFDTable, self).__init__(parent)
        self.setupUi(self)
        tribtablestyle(self)

        # Populate Distribution Combobox
        self.comboBoxDist.clear()
        self.comboBoxDist.addItems(distr._distrnames())
        self.activeDistr = self.comboBoxDist.currentKey()
        #        self.comboBoxDist.currentIndexChanged.connect(self.onChangeDistribution)

        # Populate Fixed Distr Input Table
        self.fixedInputData = {'Input': [''], 'Value': ['']}
        self.resetInputTable()

        # Populate Fixed Distr Tab Table

        self._getFixedDistrValues()

        #        self._calcFixedDistr()

        self.fixedDistrHeaders = ['Variable', 'Value']
        self.fixedDistrData = {}
        self.fixedDistrData[self.fixedDistrHeaders[0]]=['0.9', '0.5', '0.1', 'mean', 'std', 'P10']
        self.fixedDistrData[self.fixedDistrHeaders[1]]=['']*len(self.fixedDistrData[self.fixedDistrHeaders[0]])
        self.basicOutputs = self.fixedDistrData
        self.tableColRatio = 0.5
        self.tableWidgetDistrValues.setdata(self.basicOutputs)
        #        self._calcFixedDistrTable()

        # monitors for distribution input boxes
        self.comboBoxDist.currentIndexChanged.connect(self.onChangeDistribution)

        # monitors for changes to input table
        self.tableWidgetDistrInputs.itemChanged.connect(self.onInputEdited)

        # monitors for changes to output table

        self.tableWidgetDistrValues.itemChanged.connect(self.onTableEdited) #moved to _calcDistrRow


        # monitors resizing of window
        # self.tableWidgetDistrValues.resizeEvent(self.onTableResize)

        self.tableWidgetDistrValues.setCurrentCell(0, 0)

    # functions for Fixed Distribution Tab


    def _getFixedDistrValues(self):
        self.fixedInputData = self.tableWidgetDistrInputs.returndata()

    def resetInputTable(self):
        # reset the inputs required for the input table, necessary when type of distribution changes
        self.fixedInputData['Input'] = distr._distrinputs(self.activeDistr)
        self.fixedInputData['Value'] = len(self.fixedInputData['Input'])*[''] #TODO get this to work with saved info or info coming form another widget
        self.tableWidgetDistrInputs.setdata(self.fixedInputData)

    def _calcFixedDistr(self):
        self.fixedInputData = self.tableWidgetDistrInputs.returndata()
        # check for active distribution required stats
        self.kstats, rowflags = distr.invdistr2(self.activeDistr, self.fixedInputData, flags=True)
        self.tableWidgetDistrInputs.colourTableByRow(rowflags,tablecolourflagstyle())
        if self.kstats is not None: # if not failed update chart
            self.kstats = distr.distrstats(self.activeDistr, **self.kstats)  # calculate missing stats
            self.actionDistrUpdated.emit([self.activeDistr, self.kstats])

        self._calcFixedDistrTable()

    def _calcFixedDistrRow(self, row):

        self.tableWidgetDistrValues.setCurrentCell(row, 0)
        var = self.tableWidgetDistrValues.currentItem().text()
        rowflag = 1
        if var in self.kstats:
            val = self.kstats[var]
        else:
            try:
                pc = float(var)
                if 0.0 < pc < 1.0:
                    if self.activeDistr == 'norm':
                        val = stats.norm.ppf(1 - pc, loc=self.kstats['mu'], scale=self.kstats['std'])
                    elif self.activeDistr == 'lognorm':
                        val = stats.lognorm.ppf(1 - pc, self.kstats['shp'], scale=np.exp(self.kstats['mu']))
                    else:
                        raise ValueError
                else:
                    raise ValueError
            except ValueError:
                rowflag = 9
                val = '#N/A'

        # check if last row and add another if needed
        if row == self.tableWidgetDistrValues.rowCount() - 1:
            self.tableWidgetDistrValues.addrow()
        self.tableWidgetDistrValues.setCurrentCell(row, 1)
        self.tableWidgetDistrValues.currentItem().setText(str(val))
        self.tableWidgetDistrValues.setRowColour(row, tablecolourflagstyle()[rowflag])

    def _calcFixedDistrTable(self):

        self.tableWidgetDistrValues.itemChanged.disconnect()
        if self.kstats is not None:
            nrows = self.tableWidgetDistrValues.rowCount() - 1
            for row in range(0, nrows):
                self._calcFixedDistrRow(row)
        else:
            self.tableWidgetDistrValues.setBlankColumn(1)

        self.tableWidgetDistrValues.itemChanged.connect(self.onTableEdited)

    # special pyqt slots

    @pyqtSlot()
    def onInputEdited(self):
        self._calcFixedDistr()

    @pyqtSlot()
    def onChangeDistribution(self):
        self.activeDistr=self.comboBoxDist.currentKey()
        self.resetInputTable()
        self._calcFixedDistr()
        self._calcFixedDistrTable()

    @pyqtSlot()
    def onTableEdited(self):
        inrow = self.tableWidgetDistrValues.currentRow()
        incol = self.tableWidgetDistrValues.currentColumn()

        self.tableWidgetDistrValues.itemChanged.disconnect()
        self._calcFixedDistrRow(inrow)
        self.tableWidgetDistrValues.itemChanged.connect(self.onTableEdited)

        self.tableWidgetDistrValues.setCurrentCell(inrow, incol)

def main():
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)
    # chartView.chart.addLinearReg()
    fdtable = widgetFDTable()
    window = QMainWindow()
    window.setCentralWidget(fdtable)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()