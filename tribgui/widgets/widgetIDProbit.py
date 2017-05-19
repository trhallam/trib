"""widgetIDChart

This module contains classes for the modification of the idchart widget 
Classes inherit from layouts designed in qt designer. 
make.py must be run in the tribgui module folder to update the gui interface.

"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtChart import QChartView
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from tufpy.stats import distr

from scipy import stats

from tribgui._qtdesigner import qdesignFDChart
from tribgui.colourpack import tribColours

from pyqt5x import XChartProbit

s = 0.5
dummy_data_4testing = stats.lognorm.rvs(s, scale=0.2, size=100)
#dummy_data_4testing = stats.norm.rvs(loc=100, scale=10, size=200)

'''
dummy_data_4testing = [0.08, 0.18, 0.19, 0.22, 0.38, 0.39, 0.83, 0.91, 1.62, 1.92, 1.93, 2.58, 3.2,
 3.43, 3.86, 3.87, 3.94, 3.95, 4.02, 4.14, 4.15, 4.22, 4.43, 4.6, 4.68, 4.78, 5.14, 5.52, 5.66,
 5.74, 6.89, 8.08, 8.3, 8.61, 8.76, 8.86, 9.24, 9.27, 9.56, 10.54, 11.64, 11.66, 12.46, 13.26, 14.1,
 14.48, 15.68, 15.72, 16.81, 18, 18.32, 18.54, 19.28, 20.56, 22.08, 23.8, 24.86, 27.12, 27.51,
 28.56, 30.08, 31.51, 35.62, 36.01, 36.1, 39.02, 39.09, 39.58, 40.14, 40.98, 41.05, 41.54, 43.01,
 43.93, 44.2, 44.76, 57.14, 67.12, 71.68, 72.01, 74.02, 76.68, 76.89, 82.16, 82.6, 85.12, 85.78,
 90.24, 92.44, 93.62, 94.51, 96.32, 99.22, 246.75]
 '''
dummy_data_names = list()
 
for i, dp in enumerate(dummy_data_4testing):
    dummy_data_names.append('ID_%02d'%i)


class widgetIDProbit(QtWidgets.QWidget, qdesignFDChart.Ui_Form):

    actionRequestFromTable = pyqtSignal()

    def __init__(self, parent=None):
        super(widgetIDProbit, self).__init__(parent)
        self.setupUi(self)

        # Default Settings
        self.nbins = 10
        
        # Extra Menu Items
        # Distribution Type Selection
        self.comboBoxDistr = QtWidgets.QComboBox(self)
        self.comboBoxDistr.setMinimumSize(QtCore.QSize(100, 30))
        
        self.knowndistr = distr._distrnames()
        self.comboBoxDistr.addItems([self.knowndistr[key] for key in self.knowndistr])
        self.comboBoxDistr.setObjectName("comboBoxDistr")
        self.horizontalLayout.insertWidget(3,self.comboBoxDistr)
        self.comboBoxDistr.currentTextChanged.connect(self.onComboBoxDistrChanged)
        self.activeDist = str(self.distrfromname(self.comboBoxDistr.currentText()))

        self.chart = XChartProbit()

        # Add Chart to Chartview and Chartview to Widget
        self.chartview = QChartView(self.chart)
        self.verticalLayout.addWidget(self.chartview)
        self.chartview.setRenderHint(QPainter.Antialiasing)        
        
        self.onComboBoxDistrChanged(self.activeDist)

        
    def updateChart(self):
        pass
             
    def distrfromname(self,search):
        for key, name in self.knowndistr.items():
            if name == search:
                return key
        
    @pyqtSlot(str)
    def onComboBoxDistrChanged(self, name):
        '''
        self.activeDist = str(self.distrfromname(name))
        if self.activeDist == 'norm':
            self.chart.setActiveScale('linear')
        elif self.activeDist == 'lognorm':
            self.chart.setActiveScale('log10')
        self.chart.redrawChart()
        '''

        self.chart.setActiveProbit(self.activeDist)

    @pyqtSlot(dict)
    def receiveFromTable(self, datadict):
        self.onComboBoxDistrChanged(self.activeDist)
        self.chart.loadSeries(datadict['Value'],"Values")
        self.chart.redrawChart()

def main():
    import sys
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from numpy import random

    app = QApplication(sys.argv)

    rand = random.lognormal(size=50,mean=2,sigma=0.1); randn = random.normal(size=50,loc=10,scale=5)
    rand = rand.clip(min=1.1); randn = randn.clip(min=1.1)

    chartWid = widgetIDProbit()    
    chartWid.chart.loadSeries(rand,"Log-Normal Rand")
    chartWid.chart.loadSeries(randn,"Normal Rand")
    chartWid.chart.redrawChart()
    
    #chartView.chart.addLinearReg()
    
    window = QMainWindow()
    window.setCentralWidget(chartWid)
    window.resize(800, 600)
    
    
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()