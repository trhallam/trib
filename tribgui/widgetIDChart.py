"""widgetIDChart

This module contains classes for the modification of the idchart widget 
Classes inherit from layouts designed in qt designer. 
make.py must be run in the tribgui module folder to update the gui interface.

"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtChart import QChart, QChartView, QValueAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import pyqtSlot, Qt
from tufpy.stats import distr

import numpy as np
from scipy import stats

from tribgui._qtdesigner import qdesignFDChart
from pyqt5x.XChartTools import XLineSeries, XDictSet

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


class widgetIDChart(QtWidgets.QWidget, qdesignFDChart.Ui_Form):
    def __init__(self, parent=None):
        super(widgetIDChart, self).__init__(parent)
        self.setupUi(self)

        # Default Settings
        self.nbins = 10
        
        # Extra Menu Items
        # Distribution Type Selection
        self.comboBoxDistr = QtWidgets.QComboBox(self)
        self.comboBoxDistr.setMinimumSize(QtCore.QSize(100, 30))
        
        self.knowndistr = distr._distrnames()
        self.comboBoxDistr.addItems(['None'] + [self.knowndistr[key] for key in self.knowndistr])
        self.comboBoxDistr.setObjectName("comboBoxDistr")
        self.horizontalLayout.insertWidget(3,self.comboBoxDistr)
        self.comboBoxDistr.currentTextChanged.connect(self.onComboBoxDistrChanged)
        self.activeDist = str(self.distrfromname(self.comboBoxDistr.currentText()))

        # Spinbox Label
        self.spinBoxLab = QtWidgets.QLabel(self)
        self.spinBoxLab.setText('N Hist Bins: ')
        self.horizontalLayout.insertWidget(4, self.spinBoxLab)
        
        # Histogram N columns quick select spin box
        self.spinBoxDistr = QtWidgets.QSpinBox(self)
        self.spinBoxDistr.setMinimumSize(QtCore.QSize(50,30))
        self.spinBoxDistr.setRange(2,100); self.spinBoxDistr.setSingleStep(1); self.spinBoxDistr.setValue(self.nbins)
        self.spinBoxDistr.setObjectName("spinBoxDistr")
        self.horizontalLayout.insertWidget(5,self.spinBoxDistr)
        self.spinBoxDistr.valueChanged.connect(self.onSpinBoxChanged)
        
        # SetUp for Chart to Display Distribution curves and inputs.
        self.chart = QChart()
        self.chart.legend().setVisible(False)

        # SetUp Visible Chart Axes
        self.chart.axisX = QValueAxis(); self.chart.axisY = QValueAxis()
        self.chart.axisX.setTickCount(10); self.chart.axisY.setTickCount(2)
        self.chart.axisX.setTitleText("Value")
        self.chart.axisY.setTitleText("Probability")
        
        # HistogramAxis
        self.chart.axisHist = QValueAxis()
        self.chart.addAxis(self.chart.axisHist, Qt.AlignRight)
        self.chart.axisHist.setTickCount(10)
        self.chart.axisHist.setTitleText("Count")
        self.chart.axisBins = QValueAxis()
        self.chart.addAxis(self.chart.axisBins, Qt.AlignBottom)
        self.chart.axisBins.setVisible(False)

        # Add Chart to Chartview and Chartview to Widget
        self.chartview = QChartView(self.chart)
        self.verticalLayout.addWidget(self.chartview)
        self.chartview.setRenderHint(QPainter.Antialiasing)

    def axesMinMax(self):
        # returns a length 4 list of the axes min and max values [x1,x2,y1,y2]
        return [self.chart.axisX.min(), self.chart.axisX.max(), self.chart.axisY.min(), self.chart.axisY.max()]

    def setAxes(self, series):
        # assigns a series to the chart default axes
        self.chart.setAxisX(self.chart.axisX, series)
        self.chart.setAxisY(self.chart.axisY, series)

    def setAxesMinMax(self, x1, x2, y1, y2):
        # sets the min max values in X and Y
        self.chart.axisX.setMin(x1); self.chart.axisX.setMax(x2)
        self.chart.axisY.setMin(y1); self.chart.axisY.setMax(y2)

    def setTitle(self,title):
        self.chart.setTitle(title)
        
    def setRawData(self, datar):
        self.datar = datar
        self.ndata = len(self.datar)   

    def addDistrLine(self, n, kstats):
        self.kstats = kstats
        data = distr.distrpdf(self.activeDist, n, **kstats)
        xmin = min(data['X']); xmax = max(data['X'])
        ymin = min(data['Y']); ymax = max(data['Y'])
        xscal = 0.1*(xmax-xmin); yscal = 0.1*(ymax-0)
        self.chart.axisY.setRange(0, ymax+yscal)
        self.lineDist = XLineSeries(data, xkey='X')[0]
        
    def addHistLine(self):
        # fits a distribution to the histogram and draws a line
        self.kstats = distr.distrfit(self.activeDist,self.datar)#hist[0])
        self.addDistrLine(100,self.kstats)
        
    def addHistogram(self, nbins):
# accepts a data array datar and int nbins to calculate a histogram
        self.nbins = nbins
        self.spinBoxDistr.setValue(nbins)
        try:
            self.hist = np.histogram(self.datar, bins=nbins)
        except:
            pass
            # create a function which displays a msg in the middle of the chart by raising a data error of sorts
        self.histseries = XDictSet({'Hist':self.hist[0]})
            
    def updateChart(self):
        self.chart.removeAllSeries()
        hmin = self.hist[1][0]; hmax = self.hist[1][-1]; cmax = max(self.hist[0])+1
        binwidth = self.hist[1][1]-self.hist[1][0]; binscale = 1/binwidth
        
        if self.activeDist == 'None':
            self.chart.axisY.setVisible(False)
            self.chart.axisX.setMin(hmin)
            self.chart.axisX.setMax(hmax)
        else:
            self.chart.axisY.setVisible(True)

        try:  # Add histogram bars
            self.chart.axisBins.setRange(-1, self.nbins)
            self.chart.axisHist.setRange(0, cmax)
            self.chart.addSeries(self.histseries)
            self.histseries.setBarWidth(1)
            self.histseries.setColor()
            self.chart.setAxisX(self.chart.axisBins, self.histseries)
            self.chart.setAxisY(self.chart.axisHist, self.histseries)
        except NameError:
            pass

        if self.activeDist != 'None':
            try:  # Add distribution line
                self.addHistLine()
                self.chart.addSeries(self.lineDist)
                self.setAxes(self.lineDist)
                self.chart.axisX.setRange(hmin-binwidth, hmax+binwidth)
               
            except AttributeError:
                pass
             

    @pyqtSlot(int)
    def onSpinBoxChanged(self,n):
        self.nbins = n
        self.addHistogram(self.nbins)
        self.updateChart()

    def distrfromname(self,search):
        for key, name in self.knowndistr.items():
            if name == search:
                return key
        
    @pyqtSlot(str)
    def onComboBoxDistrChanged(self, name):
        self.activeDist = str(self.distrfromname(name))
        self.addHistogram(self.nbins)
        self.updateChart()

def main():
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    IDchart = widgetIDChart()
    #IDchart.addDistrLine('lognorm', 100, kstats)
    IDchart.setRawData(dummy_data_4testing)
    IDchart.addHistogram(20)
    #IDchart.addHistLine()
    IDchart.updateChart()
    
    distr.distrfit('lognorm',dummy_data_4testing)
    window = QMainWindow()
    window.setCentralWidget(IDchart)
    window.resize(800, 600)
    
    
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()