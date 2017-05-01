"""tribWidgetFDTable

This module contains classes for the modification of the fdtables widget 
Classes inherit from layouts designed in qt designer. 
make.py must be run in the tribgui module folder to update the gui interface.

"""

from PyQt5 import QtGui, QtWidgets
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
        self._setTableWidgetDistrValuesData(self.basicOutputs)
        self._calcFixedDistrTable()

        # monitors for distribution input boxes

        self.lineEditProb1.textChanged.connect(self.onTextEdited)
        self.lineEditProb2.textChanged.connect(self.onTextEdited)
        self.lineEditValue1.textChanged.connect(self.onTextEdited)
        self.lineEditValue2.textChanged.connect(self.onTextEdited)

        # monitors for changes to output table

        self.tableWidgetDistrValues.itemChanged.connect(self.onTextEdited)

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

    def _calcFixedDistrTable(self):
        kstats = ['mean', 'std', 'median']
        rows = self.tableWidgetDistrValues.rowCount() - 1
        val = ''
        for row in range(0, rows):
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
                    if 0 < pc < 1:
                        val = stats.norm.ppf(1-pc, loc=self.fixedDistrMu, scale=self.fixedDistrStd)
                    else:
                        raise ValueError
                except ValueError:
                    # self.tableWidgetDistrValues.currentItem().setBackground() # investigate QBrush etc
                    val = ''

            # print('_calcFixedDistrTable', row, var, val)
            self.tableWidgetDistrValues.setCurrentCell(row, 1)
            self.tableWidgetDistrValues.currentItem().setText(str(val))

    # special pyqt slots

    @pyqtSlot()
    def onTextEdited(self):
        self._getFixedDistrValues()
        self._calcFixedDistr()
        self._calcFixedDistrTable()

    #   def _getTableWidgetDistrValuesData(self):
    #      horHeaders = self.tableWidgetDistrValues.takeHorizontalHeaderItem(1)
    #      print(horHeaders)

    def _setTableWidgetDistrValuesData(self, data):
        horHeaders = []
        self.tableWidgetDistrValues.setRowCount(len(data['Variable']) + 1)
        for n, key in enumerate(data.keys()):
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QtWidgets.QTableWidgetItem(item)
                self.tableWidgetDistrValues.setItem(m, n, newitem)
        self.tableWidgetDistrValues.setHorizontalHeaderLabels(horHeaders)