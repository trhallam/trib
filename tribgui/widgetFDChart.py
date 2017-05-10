"""widgetFDChart

This module contains classes for the modification of the fdchart widget 
Classes inherit from layouts designed in qt designer. 
make.py must be run in the tribgui module folder to update the gui interface.

"""

from PyQt5 import QtGui, QtWidgets, QtCore, QtChart
from PyQt5.QtCore import pyqtSlot, Qt

from tribgui._qtdesigner import qdesignFDChart


class widgetFDChart(QtWidgets.QWidget, qdesignFDChart.Ui_Form):
    def __init__(self, parent=None):
        super(widgetFDChart, self).__init__(parent)
        self.setupUi(self)


        # self.setTitle("Fixed Distribution - Normal")

        self.chart = QtChart.QChart()
        self.chartview = QtChart.QChartView(self.chart)
        self.verticalLayout.addWidget(self.chartview)

        # self.legend().setVisible(True)
        # self.setAnimationOptions(QChart.SeriesAnimations)
        # self.legend().setAlignment(Qt.AlignBottom)

def main():
    import sys
    from PyQt5.QtChart import QChartView
    from PyQt5.QtGui import QPainter
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from scipy import stats
    import numpy as np
    from pyqt5x.XChartTools import XLineSeries

    app = QApplication(sys.argv)


    mu=50; std=1.5
    data = np.linspace(stats.norm.ppf(0.01, loc=mu, scale=std),
                       stats.norm.ppf(0.99, loc=mu, scale=std), 1000)
    data = stats.norm.pdf(data, loc=50, scale=1.0)
    data = {'Normal': data}

    lineseries = XLineSeries(data)
    print(lineseries)

    chartView = widgetFDChart()

    chart = widgetFDChart()
    chart.addSeries(lineseries[0])
    chart.createDefaultAxes()
    chartView = QChartView(chart)
    chartView.setRenderHint(QPainter.Antialiasing)

    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()