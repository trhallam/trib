"""XChartTools

This file contains functions which help build charts using QtCharts

"""

from PyQt5.QtChart import QScatterSeries, QXYSeries, QValueAxis
from PyQt5.QtChart import QChart, QChartView
from PyQt5.QtCore import QObject, QPointF, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QColor, QPen
from itertools import zip_longest
import random
import numpy as np

from XChartMarkers import xtypemarker
from XGraphColourPack import gaColours

class XScatterSeries(QScatterSeries):

    onActionUpdated = pyqtSignal()
    hovered = pyqtSignal(QPointF, bool, str)

    def __init__(self, parent=None, marker=None, tooltips=False, temp=False):#, parent = None):
        super(QScatterSeries, self).__init__(parent)
        self.setUseOpenGL(True)
        
        #self.hovered.connect(self.onHoverHighlight)
        self.setName('Help')
        self._temp = temp

        #setup better marker defaults
        self._markersize = 15
        self.setMarkerSize(self._markersize)
        self.setMarkerShape(1)
        self.setBorderColor(QColor(0,0,0,0))
        xtypemarker(self, fillalpha=100)
            
    def addXY(self,X, Y):
        '''
        the first dict in the key_order will be used as the x-axis
        '''
        self.X = X; self.Y = Y
        for i, (itemx, itemy) in enumerate(zip_longest(X,Y)):
            self.append(itemx, itemy)
            
    def _find_nearest(self, vx, vy):
        idx = np.sqrt(np.power(self.X-vx,2) + np.power(self.Y-vy,2)).argmin()
        #idx = (np.abs(array-value)).argmin()
        return QPointF(self.X[idx], self.Y[idx])


class XScatterSet(QObject):

    onActionUpdated = pyqtSignal(int, int, int, int)
    hovered = pyqtSignal(QPointF, bool, str)

    def __init__(self, tooltips=False, useOpenGL=False, parent=None):
        super(XScatterSet, self).__init__(parent)
        self._openGL = useOpenGL
        self._scatterset = []
        
        self._basecolour = gaColours.blue
        self._hlcolour = gaColours.zinnia
        self._size = 15
        
        
    def setChart(self, chart):
        self._chart = chart
    
    def chart(self):
        return self._chart

    def addXY(self,X, Y):
        for i, (itemx, itemy) in enumerate(zip_longest(X,Y)):
            series = QScatterSeries()#XScatterSeries(marker=self._marker)
            if self._openGL:
                series.setUseOpenGL(True)
            series.append(itemx, itemy)
            
            xtypemarker(series, fill=self._basecolour, width=3, size=self._size)
            self._scatterset.append(series)
            self._chart.addSeries(series)
            self.chart().legend().markers(series)[0].setVisible(False)
            series.hovered.connect(self.onHovered)
           

    def setAxisX(self, axis):
        for ser in self._scatterset:
            self.chart().setAxisX(axis, ser)
            
    def setAxisY(self, axis):
        for ser in self._scatterset:
            self.chart().setAxisY(axis, ser)
            
    def _find_nearest(self, vx, vy):
        idx = np.sqrt(np.power(self.X-vx,2) + np.power(self.Y-vy,2)).argmin()
        #idx = (np.abs(array-value)).argmin()
        return QPointF(self.X[idx], self.Y[idx])
            
    @pyqtSlot(QPointF, bool)        
    def onHovered(self, point, state):
        sender = self.sender()
        if state:
            xtypemarker(sender, size=self._size*1.3, width=3, fill=self._hlcolour)
        else:
            xtypemarker(sender, size=self._size, width=3, fill=self._basecolour)
        sender.pointsReplaced.emit()

        

class XChart(QChart):
    
    onActionUpdated = pyqtSignal()
    
    def __init__(self, parent=None):
        super(QChart, self).__init__(parent)
        
        self.setAnimationOptions(QChart.SeriesAnimations)

        self.axisX = QValueAxis()
        self.axisY = QValueAxis()

        self.axisX.setTickCount(10)
        self.axisY.setTickCount(10)
        
        self.axisX.setMin(0); self.axisX.setMax(1)
        self.axisY.setMin(0); self.axisY.setMax(1)
        
        #Temporay Test Data
        x = np.random.rand(100)
        y = np.random.rand(100)
        #self.series = XScatterSeries(tooltips = True)
        #self.series.addXY(x,y)
        #self.addSeries(self.series)
        #self.setAxisX(self.axisX, self.series); self.setAxisY(self.axisY, self.series)
        
        self.serset = XScatterSet(useOpenGL=False) # many options not supported with openGl
        self.serset.setChart(self)
        self.serset.addXY(x,y)
        self.serset.setAxisX(self.axisX); self.serset.setAxisY(self.axisY)
        
        self.setToolTip('Hello')
        #Tooltip series

class XChartView(QChartView):
    def __init__(self, parent=None):
        super(QChartView, self).__init__(parent)
        
    def update(self):
        super(QChartView, self).update()
        print('Updating')

def main():
    import sys
    from PyQt5.QtChart import QChart, QChartView
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPainter
    from PyQt5.QtWidgets import QApplication, QMainWindow
    
    import numpy as np

    app = QApplication(sys.argv)
    chart = XChart()
    #chart.addSeries(series)

 
    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignBottom)

    chartView = XChartView(chart)
    #chart.serset.onActionUpdated.connect(chartView.repaint)
    
    chartView.setMouseTracking(True)

    chartView.setRenderHint(QPainter.Antialiasing)
    
    
    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
