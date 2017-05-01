"""tribWidgetFDTable

This module contains classes for the modification of the fdtables widget 
Classes inherit from layouts designed in qt designer. 
make.py must be run in the tribgui module folder to update the gui interface.

"""

from PyQt5 import QtGui, QtWidgets

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

        print(self.fixedDistrMu, self.fixedDistrStd)

        self.tableWidgetDistrValues.setColumnCount(2)
        self.basicOutputs = {
            'Variable': ['90', '50', '10', 'mean', 'std'], \
            'Value': ['0', '0', '0', '0', '0']}
        self._setTableWidgetDistrValuesData(self.basicOutputs)
        self._calcFixedDistrTable()

    # functions for Fixed Distribution Tab

    def _getFixedDistrValues(self):
        self.fixedDistr = {}
        self.fixedDistr[self.lineEditProb1.text()] = self.lineEditValue1.text()
        self.fixedDistr[self.lineEditProb2.text()] = self.lineEditValue2.text()

    def _calcFixedDistr(self):
        p = [];
        f = []
        for key in self.fixedDistr.keys():
            p.append(1 - float(key))
            f.append(float(self.fixedDistr[key]))
        self.fixedDistrMu, self.fixedDistrStd = \
            distr.invNormPpf(f[0], p[0] / 100, f[1], p[1] / 100)

    def _calcFixedDistrTable(self):
        kstats = ['mean', 'std', 'median']
        rows = self.tableWidgetDistrValues.rowCount() - 1
        val = ''
        for row in range(0, rows + 1):
            var = self.tableWidgetDistrValues.itemAt(row, 0).text()
            print(row, var)
            if var in kstats:
                if var == 'mean':
                    val = self.fixedDistrMu
                if var == 'std':
                    val = self.fixedDistrStd
                if var == 'median':
                    val = stats.norm.median(loc=self.fixedDistrMu, scale=self.fixedDistrStd)
        self.tableWidgetDistrValues.itemAt(row, 0).setText(var)
        self.tableWidgetDistrValues.itemAt(row, 1).setText(str(val))

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