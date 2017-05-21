"""widgetFDChart

This module contains classes for the modification of the fdchart widget 
Classes inherit from layouts designed in qt designer. 
make.py must be run in the tribgui module folder to update the gui interface.

"""

from PyQt5 import QtWidgets
from PyQt5.QtChart import QChart, QChartView, QValueAxis
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from tufpy.stats import distr

from tribgui._qtdesigner import qdesignFDChart
from tribgui.stylesheet import tribchartmenustyle
from pyqt5x.XChartTools import XLineSeries

class widgetFDChart(QtWidgets.QWidget, qdesignFDChart.Ui_Form):
    def __init__(self, parent=None):
        super(widgetFDChart, self).__init__(parent)
        self.setupUi(self)
        tribchartmenustyle(self)
         # SetUp for Chart to Display Distribution curves and inputs.
        self.chart = QChart()
        self.chart.legend().setVisible(False)

        self.chart.axisX = QValueAxis(); self.chart.axisY = QValueAxis()
        self.chart.axisX.setTickCount(10); self.chart.axisY.setTickCount(10)
        self.chart.axisX.setTitleText("Value")
        self.chart.axisY.setTitleText("Probability")

        self.chartview = QChartView(self.chart)
        self.verticalLayout.addWidget(self.chartview)
#        self.setAxesMinMax(-3,3,0.01,1.5)
        self.chartview.setRenderHint(QPainter.Antialiasing)
        # self.legend().setVisible(True)
        # self.setAnimationOptions(QChart.SeriesAnimations)
        # self.legend().setAlignment(Qt.AlignBottom)

        # Connect Buttons
        self.pushButtonExportPNG.pressed.connect(self._onActionSavePNG)

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

    def addDistrLine(self, type, n, kstats):
        data = distr.distrpdf(type, n, **kstats)
        xmin = min(data['X']); xmax = max(data['X'])
        ymin = min(data['Y']); ymax = max(data['Y'])
        self.lineDist = XLineSeries(data, xkey='X')[0]
        self.chart.addSeries(self.lineDist)
        self.setAxes(self.lineDist)
        xscal = 0.1*(xmax-xmin); yscal = 0.1*(ymax-ymin)
        self.setAxesMinMax(xmin-xscal, xmax+xscal, ymin, ymax+yscal)

    def updateChart(self, tabledata):
        self.activeDist = tabledata[0]
        self.kstats = tabledata[1]
        self.chart.removeAllSeries()
        self.addDistrLine(self.activeDist, 100, self.kstats)

    @pyqtSlot(str)
    def paintChart(self,filename):
        #pixmap = QPixmap()
        pixmap = self.chartview.grab()
        pixmap.save(filename)

    def _onActionSavePNG(self):
        pngfile = QtWidgets.QFileDialog.getSaveFileName(self,
                caption = 'Export PNG As', directory = '~', filter='*.png')
        #try:
        self.paintChart(pngfile[0])
        #except:
        #   pass

def main():
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    kstats = {'mu':2, 'std':1.5, 'shp':0.5}

    FDchart = widgetFDChart()
    FDchart.addDistrLine('lognorm', 100, kstats)

    window = QMainWindow()
    window.setCentralWidget(FDchart)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()