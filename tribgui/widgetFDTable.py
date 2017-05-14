"""widgetFDTable

This module contains classes for the modification of the fdtables widget 
Classes inherit from layouts designed in qt designer. 
make.py must be run in the tribgui module folder to update the gui interface.

"""

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from tribgui._qtdesigner import qdesignFDTables

from tufpy.stats import distr
from scipy import stats, exp

'''
Class to caputre the setup of the main window.
'''


class widgetFDTable(QtWidgets.QWidget, qdesignFDTables.Ui_Form):

    # signals to communicate with other widgets through main window
    actionDistrUpdated = pyqtSignal(list)

    def __init__(self, parent=None):
        super(widgetFDTable, self).__init__(parent)
        self.setupUi(self)

        # known distributions
        self.distrTypes = {'Normal': 'norm',
                           'Log-Normal': 'lognorm'}

        # Populate Distribution Combobox
        self.comboBoxDist.clear()
        self.comboBoxDist.addItems(list(self.distrTypes.keys()))
        self.activeDistr = self.distrTypes[self.comboBoxDist.currentText()]
        self.comboBoxDist.currentIndexChanged.connect(self.onChangeDistribution)

        # Populate Fixed Distr Tab Table

        self._getFixedDistrValues()
        self._calcFixedDistr()

        self.fixedDistrHeaders = ['Variable', 'Value']
        self.fixedDistrData = {}
        self.fixedDistrData[self.fixedDistrHeaders[0]]=['0.9', '0.5', '0.1', 'mean', 'std', 'P10']
        self.fixedDistrData[self.fixedDistrHeaders[1]]=['']*len(self.fixedDistrData[self.fixedDistrHeaders[0]])
        self.basicOutputs = self.fixedDistrData
        self.tableColRatio = 0.5
        self.tableWidgetDistrValues.setdata(self.basicOutputs)
        self._calcFixedDistrTable()

        # monitors for distribution input boxes
        self.comboBoxDist.currentIndexChanged.connect(self.onFixedDistrEdited)
        self.lineEditProb1.textChanged.connect(self.onFixedDistrEdited)
        self.lineEditProb2.textChanged.connect(self.onFixedDistrEdited)
        self.lineEditValue1.textChanged.connect(self.onFixedDistrEdited)
        self.lineEditValue2.textChanged.connect(self.onFixedDistrEdited)

        # monitors for changes to output table

        self.tableWidgetDistrValues.itemChanged.connect(self.onTableEdited) #moved to _calcDistrRow


        # monitors resizing of window
        # self.tableWidgetDistrValues.resizeEvent(self.onTableResize)

        self.tableWidgetDistrValues.setCurrentCell(0, 0)

    # functions for Fixed Distribution Tab

    def _getFixedDistrValues(self):
        self.fixedDistr = {}
        self.fixedDistr[self.lineEditProb1.text()] = self.lineEditValue1.text()
        self.fixedDistr[self.lineEditProb2.text()] = self.lineEditValue2.text()

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

    #pyqt redefinitions



    #   def _getTableWidgetDistrValuesData(self):
    #      horHeaders = self.tableWidgetDistrValues.takeHorizontalHeaderItem(1)
    #      print(horHeaders)

