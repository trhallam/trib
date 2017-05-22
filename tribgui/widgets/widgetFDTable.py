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

        # input table checking
        self.inval = dict(); icount = 1; fpsanity = []; rowflags = []; fprows = []
        for i, val in enumerate(self.fixedInputData['Input']):  # loop through values in input
            if val != '':  # make sure cell not empty
                try:
                    if val in distr._distrinputs(self.activeDistr):  # known values like mu, std
                        self.inval[val] = float(self.fixedInputData['Value'][i])
                        rowflags.append(1)  # append known value flag
                    else: #unknown value check for decimal input to set f* p* values
                        pc = float(val); fv = float(self.fixedInputData['Value'][i])
                        if 0.0 < pc < 1.0:
                            self.inval['f%d'%icount] = fv
                            self.inval['p%d'%icount] = 1-pc
                            icount+=1
                            fpsanity.append([1 - pc, fv]); fprows.append(i)
                            rowflags.append(2)  # append fp type row flag (requires group sanity check)

                        else:  # append bad row flag
                            rowflags.append(9)
                except:  #TODO write some code that changes the colour of the cells to reflect bad inputs
                    rowflags.append(9)  # append bad row flag

        # sanity check for fp values
        fpsanity = np.array(fpsanity)
        try:
            fpsanity = fpsanity[fpsanity[:, 1].argsort()]
            if not strictly_increasing(fpsanity[:, 0]):
                for row in fprows:
                    rowflags[row] = 9
        except:
            pass
        self.tableWidgetDistrInputs.colourTableByRow(rowflags,tablecolourflagstyle())

        # calculate kstats for input values and send to chart
        # mu and std as input
        cond1 = all([input in self.inval.keys() for input in distr._distrinputs(self.activeDistr)])
        # mu and p1 f1 as input
        cond2 = all([input in self.inval.keys() for input in ['mu', 'f1', 'p1']])
        # p1 f1 p2 f2 as input
        cond3 = all([input in self.inval.keys() for input in ['f1', 'p1', 'f2', 'p2']])
        if cond1: # check for simple keys
            self.kstats = dict()
            for key in distr._distrinputs(self.activeDistr):
                self.kstats[key] = self.inval[key] # add simple keys to kstats
        elif cond2:
            self.kstats = distr.invdistr(self.activeDistr, **self.inval) # use 2 point method to fix distribution
        elif cond3:
            self.inval['mu'] = None
            self.kstats = distr.invdistr(self.activeDistr, **self.inval)  # use 2 point method to fix distribution
        else:
            self.kstats = None

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