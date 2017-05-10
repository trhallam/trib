"""widgetFDTable

This module contains classes for the modification of the fdtables widget 
Classes inherit from layouts designed in qt designer. 
make.py must be run in the tribgui module folder to update the gui interface.

"""

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

from tribgui._qtdesigner import qdesignFDTables

from tufpy.stats import distr
from scipy import stats, exp

'''
Class to caputre the setup of the main window.
'''


class widgetFDTable(QtWidgets.QWidget, qdesignFDTables.Ui_Form):
    def __init__(self, parent=None):
        super(widgetFDTable, self).__init__(parent)
        self.setupUi(self)

        # known distributions
        self.distrTypes = {'Normal': 'norm',
                           'Log-Normal': 'lognorm'}

        # Populate Distribution Combobox
        self.comboBoxDist.clear()
        self.comboBoxDist.addItems(list(self.distrTypes.keys()))
        self.activeDistr = self.comboBoxDist.currentText()
        self.comboBoxDist.currentIndexChanged.connect(self.onChangeDistribution)

        # Populate Fixed Distr Tab Table

        self._getFixedDistrValues()
        self._calcFixedDistr()

        #self.tableWidgetDistrValues.setSize(10,2)
        self.fixedDistrHeaders = ['Variable', 'Value']
        self.fixedDistrData = {}
        self.fixedDistrData[self.fixedDistrHeaders[0]]=['0.9', '0.5', '0.1', 'mean', 'std', 'P10']
        self.fixedDistrData[self.fixedDistrHeaders[1]]=['']*len(self.fixedDistrData[self.fixedDistrHeaders[0]])
        self.basicOutputs = self.fixedDistrData
        self.tableColRatio = 0.5
        self.tableWidgetDistrValues.setdata(self.basicOutputs)
        self._calcFixedDistrTable()
        # self.tableWidgetDistrValues.stretchTable()

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

        # print(dir(self.lineEditProb1))
        # print(dir(self.lineEditProb1.textChanged))

        self.tableWidgetDistrValues.setCurrentCell(0, 0)

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

        if self.activeDistr == 'Normal':
            self.fixedDistrMu, self.fixedDistrStd = \
                distr.invNormPpf(f[0], p[0], f[1], p[1])
        elif self.activeDistr == 'Log-Normal':
            self.fixedDistrMu, self.fixedDistrStd, self.fixedDistrShp = \
                distr.invLogNormPpf(f[0], p[0], f[1], p[1])
        # print(self.fixedDistrMu, self.fixedDistrStd)

    def _calcFixedDistrRow(self, row):
        kstats = {'mu':self.fixedDistrMu, 'std':self.fixedDistrStd, '':'', None:None}
        if self.activeDistr == 'Normal':
            kstats['mean'], kstats['var'], kstats['skew'], kstats['kurtosis'] = \
                stats.norm.stats(loc=self.fixedDistrMu, scale=self.fixedDistrStd,moments='mvsk')
        elif self.activeDistr == 'Log-Normal':
            kstats['mean'], kstats['var'], kstats['skew'], kstats['kurtosis'] = \
                stats.lognorm.stats(self.fixedDistrShp, scale=exp(self.fixedDistrMu), moments='mvsk') #check inputs
            kstats['shp'] = self.fixedDistrShp
        else:
            kstats['mean'], kstats['var'], kstats['skew'], kstats['kurtosis'] = ['#N/A']*4

        self.tableWidgetDistrValues.setCurrentCell(row, 0)
        var = self.tableWidgetDistrValues.currentItem().text()

        if var in kstats:
            val = kstats[var]

        else:
            try:
                pc = float(var)
                if 0.0 < pc < 1.0:
                    if self.activeDistr == 'Normal':
                        val = stats.norm.ppf(1 - pc, loc=self.fixedDistrMu, scale=self.fixedDistrStd)
                    elif self.activeDistr == 'Log-Normal':
                        val = stats.lognorm.ppf(1 - pc, self.fixedDistrShp, scale=exp(self.fixedDistrMu))
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
        self.activeDistr=self.comboBoxDist.currentText()
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

