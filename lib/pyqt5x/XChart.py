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

class XScatterSeries(QScatterSeries):

    onActionUpdated = pyqtSignal()
    hovered = pyqtSignal(QPointF, bool, str)

    def __init__(self, parent=None, tooltips=False, temp=False):#, parent = None):
        super(QScatterSeries, self).__init__(parent)
        self.setUseOpenGL(True)
        
        #self.hovered.connect(self.onHoverHighlight)
        self.setMarkerSize(15)
        self.setName('Help')
        self._temp = temp
        
        
        #conncet to overloaded slots
        if tooltips:
            super(QScatterSeries,self).hovered.connect(self.onHovered)

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
            
    @pyqtSlot(QPointF, bool)        
    def onHovered(self, point, state):
        print('l')
        point = self._find_nearest(point.x(),point.y())
        if not self._temp:
            
            self.hovered.emit(point, state, self.name())
        else:
            print('h')
            #if not state:
            self.hovered.emit(point, state, self.name())
        '''
        if state:
            self.setColor(QColor(50,30,210))
            self.append(0,0)
            self.remove(0,0)
        else:
            self.setColor(QColor(120,244,210))
            self.append(0,0)
            self.remove(0,0)
        '''   
        
        #self.markerColorChanged.emit()
        #self.onActionUpdated.emit()


class XScatterSet(QObject):

    onActionUpdated = pyqtSignal(int, int, int, int)
    hovered = pyqtSignal(QPointF, bool, str)

    def __init__(self, tooltips=False, useOpenGL=False, parent=None):
        super(XScatterSet, self).__init__(parent)
        self._openGL = useOpenGL
        #self.hovered.connect(self.onHoverHighlight)
        self._scatterset = []
        self._basecolour = QColor(153,217,234)
        self._basebordercolour = QColor(73,152,173)
        self._basecolour.setAlpha(10)
        self._basepen = QPen()
        self._basepen.setColor(self._basebordercolour)
        self._basepen.setWidth(100)
        print(self._basepen.isSolid())
        
        #self.setName('Help')
 
#        #conncet to overloaded slots - implement for each scatter series
#        if tooltips:
#            super(QScatterSeries,self).hovered.connect(self.onHovered)

    def setChart(self, chart):
        self._chart = chart
    
    def chart(self):
        return self._chart

    def addXY(self,X, Y):
        for i, (itemx, itemy) in enumerate(zip_longest(X,Y)):
            series = QScatterSeries()
            if self._openGL:
                series.setUseOpenGL(True)
            series.append(itemx, itemy)
            self._scatterset.append(series)
            self._chart.addSeries(series)
            self.chart().legend().markers(series)[0].setVisible(False)
            series.hovered.connect(self.onHovered)
            series.setColor(self._basecolour)
            series.setPen(self._basepen)
            #series.setBorderColor(self._basebordercolour)
            

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
            size = 25
            color = QColor(221,145,145,150)
        else:
            size = 15
            color = self._basecolour
            
        sender.setMarkerSize(size)
        sender.setColor(color)
        sender.setPen(self._basepen)
        sender.pointsReplaced.emit()#colorChanged.emit(color)

        

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
        x = np.random.rand(1000)
        y = np.random.rand(1000)
        #self.series = XScatterSeries(tooltips = True)
        #self.series.addXY(x,y)
        #self.addSeries(self.series)
        #self.setAxisX(self.axisX, self.series); self.setAxisY(self.axisY, self.series)
        
        self.serset = XScatterSet(useOpenGL=True)
        self.serset.setChart(self)
        self.serset.addXY(x,y)
        self.serset.setAxisX(self.axisX); self.serset.setAxisY(self.axisY)
        
        
        #Tooltip series
        self.hlser = XScatterSeries(temp=True)
        #self.hlser.append(0,0); 
        self.addSeries(self.hlser)
        #self.hlser.remove(0,0)
        self.legend().markers(self.hlser)[0].setVisible(False)
        self.hlser.setColor(QColor(50,30,210))
        self.hlser.setMarkerSize(20)
        self.setAxisX(self.axisX, self.hlser); self.setAxisY(self.axisY, self.hlser)
        
        #self.series.hovered.connect(self.onHoverHighlight)
        
        #self.serset.onActionUpdated.connect(self.update)
       
    @pyqtSlot(QPointF, bool, str)
    def onHoverHighlight(self, point, state, name):
        print(state,name)
        if state:
            self.series.hovered.disconnect(self.onHoverHighlight)
            self.hlser.hovered.connect(self.onHoverHighlight)
            self.hlser.append(point)
            #self.series.remove(point)
        else:
            self.hlser.hovered.disconnect(self.onHoverHighlight)
            self.hlser.remove(point)
            self.series.hovered.connect(self.onHoverHighlight)
            #self.series.append(point)

    @pyqtSlot()
    def onUpdate(self):
        '''
        rect = self.boundingRect()
        self.visibleChanged.emit()
        
        self.scene().update(0,0,1000,1000)
        self.plotAreaChanged.emit(rect)
        self.enabledChanged.emit()
        self.update(rect)
        print(self.isEnabled())
        print(self.isActive())
        '''

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
