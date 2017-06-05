"""XChartTools

This file contains functions which help build charts using QtCharts

"""

from PyQt5.QtChart import QScatterSeries, QXYSeries, QValueAxis
from PyQt5.QtChart import QChart, QChartView
from PyQt5.QtCore import QObject, QPointF, pyqtSlot, pyqtSignal, Qt, QRect
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsRectItem
from itertools import zip_longest
import random
import numpy as np

from XChartMarkers import xtypemarker, XToolTipLabel
from XGraphColourPack import gaColours

class XScatterSeries(QScatterSeries):

    onActionUpdated = pyqtSignal()

    def __init__(self, parent=None, marker=None, tooltips=False, temp=False):
        super(XScatterSeries, self).__init__(parent)
        
        self.setName('Help')
        self._tooltips=tooltips

        #setup better marker defaults
        self._markersize = 15
        self.setMarkerSize(self._markersize)
        self.setBorderColor(QColor(0,0,0,0))
        xtypemarker(self, fillalpha=100)
        
        self.hovered.connect(self.onHovered)
            
    def addXY(self,X, Y):
        '''
        the first dict in the key_order will be used as the x-axis
        '''
        self.X = X; self.Y = Y
        for i, (itemx, itemy) in enumerate(zip_longest(X,Y)):
            self.append(itemx, itemy)
            
    def _find_nearest(self, vx, vy):
        idx = np.sqrt(np.power(self.X-vx,2) + np.power(self.Y-vy,2)).argmin()
        return QPointF(self.X[idx], self.Y[idx])
        
    @pyqtSlot(QPointF, bool)
    def onHovered(self, point, state):
        if state:
            spoint = self.chart().mapToPosition(point)-QPointF(0,self._markersize/2)
            if self._tooltips:
                self.ttip = XToolTipLabel('Hello from:\n x: %.1f, y: %.1f'%(point.x(), point.y()), colour = self.color())
            
                self.ttip_proxy = self.chart().scene().addWidget(self.ttip)
                w = self.ttip.width(); h = self.ttip.height();
                self.ttip_proxy.setPos(spoint.x()-w/2.0,spoint.y()-h)
                self.ttip.updateGeometry()
        else:
            if self._tooltips:
                self.ttip_proxy.deleteLater()


class XScatterSet(QObject):

    onActionUpdated = pyqtSignal(int, int, int, int)
    hovered = pyqtSignal(QPointF, bool, str)

    def __init__(self, tooltips=False, parent=None):
        super(XScatterSet, self).__init__(parent)
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
            series = XScatterSeries(tooltips=True)
            series.append(itemx, itemy)
            #xtypemarker(series, fill=self._basecolour, width=3, size=self._size)
            xtypemarker(series, width=3, size=self._size)
            self._scatterset.append(series)
            self._chart.addSeries(series)
            self._chart.legend().markers(series)[0].setVisible(False)

    def setAxisX(self, axis):
        for ser in self._scatterset:
            self.chart().setAxisX(axis, ser)
            
    def setAxisY(self, axis):
        for ser in self._scatterset:
            self.chart().setAxisY(axis, ser)
            

class XChart(QChart):
    

    def __init__(self, parent=None):
        super(QChart, self).__init__(parent)
        
        self.setAnimationOptions(QChart.SeriesAnimations)

        self.axisX = QValueAxis()
        self.axisY = QValueAxis()

        self.axisX.setTickCount(10)
        self.axisY.setTickCount(10)
        
        self.axisX.setMin(0); self.axisX.setMax(1)
        self.axisY.setMin(0); self.axisY.setMax(1)
        
        series=[]
        #Temporay Test Data
        for i in range(0, 10):
            x = np.random.rand(10)
            y = np.random.rand(10)
        #self.series = XScatterSeries(tooltips = True)
        #self.series.addXY(x,y)
        #self.addSeries(self.series)
        #self.setAxisX(self.axisX, self.series); self.setAxisY(self.axisY, self.series)
        
            serset = XScatterSet() # many options not supported with openGl
            serset.setChart(self)
            serset.addXY(x,y)
            serset.setAxisX(self.axisX); serset.setAxisY(self.axisY)
            series.append(serset)
            
        #self.mousePressEvent.connect(self.zoomSelectionAction)
        
        
        

    def mousePressEvent(self, event):
        self._clickpos = event.buttonDownScenePos(Qt.LeftButton)
        self._clickval = self.mapToValue(self._clickpos)
        
    def mouseMoveEvent(self, event):
        self._clickpos = event.buttonDownScenePos(Qt.LeftButton)
        self._clickval = self.mapToValue(self._clickpos)
        dragpos = event.scenePos() 
        c1 = self._clickpos.x(); c2 = self._clickpos.y()
        d1 = dragpos.x(); d2 = dragpos.y()
        x1 = min(c1,d1); y1 = min(c2, d2)
        x2 = abs(c1-d1); y2 = abs(c2 - d2)
        try:
            self.selectbox.prepareGeometryChange()
            self.scene().removeItem(self.selectbox)
        except AttributeError:
            pass
        self.selectbox = self.scene().addRect(x1, y1, x2, y2, QPen(QColor(0,0,0,0)), QBrush(QColor(125,125,255,100)))
        
    def mouseReleaseEvent(self, event):
        try:
            self.selectbox.prepareGeometryChange()
            self.scene().removeItem(self.selectbox)
        except AttributeError:
            pass
        self._releasepos = event.lastScenePos()
        self._releaseval = self.mapToValue(self._releasepos)
        self.scene().update()
        print(self._clickval, self._releaseval)

        
    def keyReleaseEvent(self, event):
        
        print(dir(event))
        if event == Qt.Key_Z:
            print ('zoom')
        
    @pyqtSlot()
    def zoomSelectionAction(self):
        print('click')
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
    
    series = XScatterSeries()
    series.append(0.5,0.5)
    chart.addSeries(series)

 
    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignBottom)

    chartView = QChartView(chart)
    chartView.setFocusPolicy(Qt.StrongFocus)
    #chart.serset.onActionUpdated.connect(chartView.repaint)
    
    #chartView.setMouseTracking(True)

    chartView.setRenderHint(QPainter.Antialiasing)
    
    
    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
