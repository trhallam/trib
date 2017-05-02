"""tribWidgetFDTable

This module contains classes for the modification of the fdtables widget 
Classes inherit from layouts designed in qt designer. 
make.py must be run in the tribgui module folder to update the gui interface.

"""

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

from tribgui._qtdesigner import tribDesignFDTables

from tufpy.stats import distr
from scipy import stats

'''
Class to caputre the setup of the main window.
'''


class tribWidgetFDTable(QtWidgets.QWidget, tribDesignFDTables.Ui_Form):
    def __init__(self, parent=None):
        super(tribWidgetFDTable, self).__init__(parent)
        self.setupUi(self)

        # known distributions
        self.distrTypes = {'Normal': 'norm',
                           'Log-Normal': 'lognorm'}

        # Populate Distribution Combobox
        self.comboBoxDist.clear()
        self.comboBoxDist.addItems(list(self.distrTypes.keys()))
        self.activeDistr = self.comboBoxDist.currentText()

        # Populate Fixed Distr Tab Table

        self._getFixedDistrValues()
        self._calcFixedDistr()

        self.tableWidgetDistrValues.setColumnCount(2)
        self.basicOutputs = {
            'Variable': ['0.9', '0.5', '0.1', 'mean', 'std', 'P10'], \
            'Value': ['0', '0', '0', '0', '0', '-99']}
        self.tableColRatio = 0.5
        self._setTableWidgetDistrValuesData(self.basicOutputs)
        self._calcFixedDistrTable()

        # monitors for distribution input boxes

        self.lineEditProb1.textChanged.connect(self.onFixedDistrEdited)
        self.lineEditProb2.textChanged.connect(self.onFixedDistrEdited)
        self.lineEditValue1.textChanged.connect(self.onFixedDistrEdited)
        self.lineEditValue2.textChanged.connect(self.onFixedDistrEdited)

        # monitors for changes to output table

        self.tableWidgetDistrValues.itemChanged.connect(self.onTableEdited)

        # monitors resizing of window
        # self.tableWidgetDistrValues.resizeEvent(self.onTableResize)

        # print(dir(self.lineEditProb1))
        # print(dir(self.lineEditProb1.textChanged))

    # functions for Fixed Distribution Tab

    def _getFixedDistrValues(self):
        self.fixedDistr = {}
        self.fixedDistr[self.lineEditProb1.text()] = self.lineEditValue1.text()
        self.fixedDistr[self.lineEditProb2.text()] = self.lineEditValue2.text()

    def _calcFixedDistr(self):
        p = []; f = []
        for key in self.fixedDistr.keys():
            p.append(1 - float(key))
            f.append(float(self.fixedDistr[key]))
        self.fixedDistrMu, self.fixedDistrStd = \
            distr.invNormPpf(f[0], p[0], f[1], p[1])
        # print(self.fixedDistrMu, self.fixedDistrStd)

    def _calcFixedDistrRow(self, row):
        kstats = ['mean', 'std', 'median']
        val = ''
        self.tableWidgetDistrValues.setCurrentCell(row, 0)
        var = self.tableWidgetDistrValues.currentItem().text()
        if var in kstats:
            if var == 'mean':
                val = self.fixedDistrMu
            if var == 'std':
                val = self.fixedDistrStd
            if var == 'median':
                val = stats.norm.median(loc=self.fixedDistrMu, scale=self.fixedDistrStd)
        else:
            try:
                pc = float(var)
                if 0.0 < pc < 1.0:
                    val = stats.norm.ppf(1 - pc, loc=self.fixedDistrMu, scale=self.fixedDistrStd)
                else:
                    raise ValueError
            except ValueError:
                self.tableWidgetDistrValues.currentItem().setBackground(QtGui.QColor(255, 154, 145))
                self._setRowColour(self.tableWidgetDistrValues, row, QtGui.QColor(255, 154, 145))
                val = '#N/A'

        # print('_calcFixedDistrRow', row, var, val)
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

    def _setTableWidgetDistrValuesData(self, data):
        horHeaders = []
        self.tableWidgetDistrValues.setRowCount(len(data['Variable']) + 1)
        for n, key in enumerate(data.keys()):
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QtWidgets.QTableWidgetItem(item)
                self.tableWidgetDistrValues.setItem(m, n, newitem)

        # self._togColEditable(self.tableWidgetDistrValues, 1)
        self.tableWidgetDistrValues.setHorizontalHeaderLabels(horHeaders)

    # special pyqt slots

    @pyqtSlot()
    def onFixedDistrEdited(self):
        self._getFixedDistrValues()
        self._calcFixedDistr()
        self._calcFixedDistrTable()

    @pyqtSlot()
    def onTableEdited(self):
        inrow = self.tableWidgetDistrValues.currentRow()
        incol = self.tableWidgetDistrValues.currentColumn()
        self._calcFixedDistrRow(inrow)
        self.tableWidgetDistrValues.setCurrentCell(inrow, incol)

    #pyqt redefinitions

    def resizeEvent(self, resizeEvent):
        twidth = self.tableWidgetDistrValues.width()
        self.tableWidgetDistrValues.setColumnWidth(0, int((twidth-22)*self.tableColRatio))
        self.tableWidgetDistrValues.setColumnWidth(1, int((twidth-22)*(1-self.tableColRatio)))

    #   def _getTableWidgetDistrValuesData(self):
    #      horHeaders = self.tableWidgetDistrValues.takeHorizontalHeaderItem(1)
    #      print(horHeaders)

