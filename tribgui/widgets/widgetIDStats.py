"""widgetIDStats

Widget for stats pane of input distribution.

"""

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal

try:
    from pyqt5x import XParameterTableWidget
except ImportError:
    from .. import env
    from pyqt5x import XParameterTableWidget

from tufpy.stats import distr

'''
Class to caputre the setup of the data input table.
'''

dummy_data_4testing = [0.08, 0.18, 0.19, 0.22, 0.38, 0.39, 0.83, 0.91, 1.62, 1.92, 1.93, 2.58, 3.2,
 3.43, 3.86, 3.87, 3.94, 3.95, 4.02, 4.14, 4.15, 4.22, 4.43, 4.6, 4.68, 4.78, 5.14, 5.52, 5.66,
 5.74, 6.89, 8.08, 8.3, 8.61, 8.76, 8.86, 9.24, 9.27, 9.56, 10.54, 11.64, 11.66, 12.46, 13.26, 14.1,
 14.48, 15.68, 15.72, 16.81, 18, 18.32, 18.54, 19.28, 20.56, 22.08, 23.8, 24.86, 27.12, 27.51,
 28.56, 30.08, 31.51, 35.62, 36.01, 36.1, 39.02, 39.09, 39.58, 40.14, 40.98, 41.05, 41.54, 43.01,
 43.93, 44.2, 44.76, 57.14, 67.12, 71.68, 72.01, 74.02, 76.68, 76.89, 82.16, 82.6, 85.12, 85.78,
 90.24, 92.44, 93.62, 94.51, 96.32, 99.22, 246.75]
dummy_data_names = list()
 
for i, dp in enumerate(dummy_data_4testing):
    dummy_data_names.append('ID_%02d'%i)


class widgetIDStats(QtWidgets.QWidget):

    # signals to communicate with other widgets through main window
    actionInputUpdated = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(widgetIDStats, self).__init__(parent)
        self.activeDistr = 'norm'
        
        self.setObjectName("Stats Table")

        # Sizing
        self.setMinimumSize(QtCore.QSize(300, 200))
        # self.setMaximumSize(QtCore.QSize(300, 5000))
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)
        self.gridLayout = QtWidgets.QGridLayout()
        self.setLayout(self.gridLayout)

        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tableWidgetStats = XParameterTableWidget()
        self.tableWidgetStats.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                                    QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addWidget(self.tableWidgetStats)
        self._buildTable()
        self.tableWidgetStats.setdata(self.cstat)
        
        # Populate Input Distr Table

        self.tableColRatio = 0.5

        # monitors resizing of window
        # self.tableWidgetDistrValues.resizeEvent(self.onTableResize)

        #self.tableWidgetDistrInput.setCurrentCell(0, 0)

    def _buildTable(self):
        statorder = ['Number of Observations', 'Minimum', 'Maximum', 'Arithmetic Mean',  # 'Median',
                     'Variance', 'Skewness', 'Kurtosis', 'Fractile 90', 'Fractile 50',
                     'Fractile 10']
        keyorder = ['nsamp', 'min', 'max', 'mean', 'var', 'skew', 'kurt', 'F90', 'F50', 'F10']
        self.cstat = dict()
        self.cstat['Statistic'] = statorder
        results = []
        for key in keyorder:
            try:
                results.append(self.istat[key])
            except (AttributeError, KeyError):
                results.append('')
        self.cstat['Values'] = results


    def _calcstats(self, datar):
        self.istat = distr.distrdescribe(datar)
        self._buildTable()
        self.tableWidgetStats.setdata(self.cstat)

    @pyqtSlot(dict)
    def receiveFromTable(self, datadict):
        #self.setRawData(datadict['Value'])
        print(datadict)
        self._calcstats(datadict['Value'])
        #self.updateChart()

    # special pyqt slots
    @pyqtSlot()
    def onDataRequest(self):
        inrow = self.tableWidgetStats.currentRow()
        incol = self.tableWidgetStats.currentColumn()

        self.data=self.tableWidgetStats.returndata()
        self.tableWidgetStats.setCurrentCell(inrow, incol)
        self.actionInputUpdated.emit(self._cleandata())

def main():
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)
    # chartView.chart.addLinearReg()
    idtable = widgetIDStats()
    window = QMainWindow()
    window.setCentralWidget(idtable)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()