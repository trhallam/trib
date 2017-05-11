"""XChartProbit

This file contains functions which help build probit style charts using QtCharts

"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtChart import (QChart, QValueAxis,
        QScatterSeries, 
        QLineSeries)

from XChartTools import XLineSeries, XScatterSeries
        
from itertools import zip_longest
from scipy.stats import norm
from numpy import arange, insert, log10, array, append

class XChartProbit(QChart):
    def __init__(self, parent=None):
        super(QChart, self).__init__(parent)

        # Axis Setup
        self.axisX = QValueAxis()
        self.axisY = QValueAxis()
        
        self.setAxesMinMax(-3,3,0.01,3)
        
        self.axisX.setMinorGridLineVisible(False)
        self.axisX.setGridLineVisible(False)
        self.axisY.setMinorGridLineVisible(False)
        self.axisY.setGridLineVisible(False)
        
        self.setGridColor(110,110,110)
        
        self._drawVerticalGridLines()
        self._drawHorizontalGridLine()
        
        #method needed for axes change to redraw grid lines
        
    def axesMinMax(self):
        return [self.axisX.min(), self.axisX.max(), self.axisY.min(), self.axisX.max()]
        
    def setGridColor(self,r,g,b):
        self.gridcolor = QColor(r,g,b)
    
    def setAxes(self,series):
        self.setAxisX(self.axisX, series); self.setAxisY(self.axisY, series)
    
    def setAxesMinMax(self,x1,x2,y1,y2):
        self.axisX.setMin(x1); self.axisX.setMax(x2)
        self.axisY.setMin(y1); self.axisY.setMax(y2)
        
    def _drawVerticalGridLines(self):
        vgridx = arange(0.05, 1.0, 0.05)
        vgridx = insert(vgridx, 0, [0.01, 0.02]); vgridx = insert(vgridx, len(vgridx), [0.98, 0.99])
        vgridy = [self.axisY.min(), self.axisY.max()]
        self.vgridseries = []
        for val in vgridx:
            line = 'P'+'%02d'%round(100.0*(1.0-val))
            tdict = {'X':[norm.ppf(val)]*2, line:vgridy}
            self.vgridseries = self.vgridseries + XLineSeries(tdict, xkey = 'X', openGL=True)
        for i,line in enumerate(self.vgridseries):
            pen = line.pen()
            pen.setColor(self.gridcolor); pen.setWidthF(0.4), line.setPen(pen)
            self.addSeries(line)
            self.setAxes(line)
            self.legend().markers(line)[0].setVisible(False)

    def _drawHorizontalGridLine(self):
        hgridx = [norm.ppf(0.01)-1, norm.ppf(0.99)+1]
        hgridy = self._logrange(self.axisY.min(), self.axisY.max(), base=10)
        self.hgridseries = []
        for val in hgridy:
            line = '%d'%val
            tdict = {'X':hgridx, line:[log10(val)]*2}
            self.hgridseries = self.hgridseries + XLineSeries(tdict, xkey = 'X', openGL=True)
        for i, line in enumerate(self.hgridseries):
            pen = line.pen()
            pen.setColor(self.gridcolor); pen.setWidthF(0.4), line.setPen(pen)
            self.addSeries(line)
            self.setAxes(line)
            self.legend().markers(line)[0].setVisible(False)
            
    def _removeHorizontalGridLine(self):
        for ser in self.hgridseries:
            self.removeSeries(ser)
            
    def _removeVerticalGridLine(self):
        for ser in self.vgridseries:
            self.removeSeries(ser)
            
    def _logrange(self, min, max, base=10):
        if min <= 0:
            min += max/(base**10)
        y = 1; bpow = base
        if min < base:
            while min < bpow:
                y -= 1; bpow = pow(base,y)
        else:
            while min > bpow:
                y += 1; bpow = pow(base,y)
        out = array([])
        while bpow < max*base:
            y += 1; bpown = pow(base,y)
            out = append(out, arange(bpow,bpown,bpow))
            bpow = bpown
        bpown= pow(base,y+1)
        out = append(out, arange(bpow,bpown,bpow))
        bpow = bpown; bpown= pow(base,y+2)
        out = append(out, arange(bpow,bpown,bpow))
        
        
        #print(out)
        return out
        
def main():
    import sys
    from PyQt5.QtChart import QChart, QChartView, QLogValueAxis, QValueAxis
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPainter
    from PyQt5.QtWidgets import QApplication, QMainWindow    
    
    from scipy.stats import norm, lognorm, percentileofscore
    from numpy import log10, random
    
    app = QApplication(sys.argv)

    rand = random.lognormal(size=50,mean=6,sigma=1.5)
    randn = random.normal(size=50,loc=4,scale=5)
    srand = rand.copy()
    srandn = randn.copy()
    srand.sort()    
    srandn.sort()
    data = dict();
    datan = dict();
    data["X"] = norm.ppf([percentileofscore(srand,srand[i])/100 for i in range(0,50)])
    datan["X"] = norm.ppf([percentileofscore(srandn,srandn[i])/100 for i in range(0,50)])    
    data["Rand"] = log10(srand)
    datan["Rand"] = log10(srandn)

    ymin = min(data['Rand'].min(),datan['Rand'].min())
    ymax = max(data['Rand'].max(),datan['Rand'].max())
    print(ymin,ymax)
    
    series=XScatterSeries(data, xkey="X", openGL=True)
    seriesn=XScatterSeries(datan, xkey="X", openGL=True)
    
    chart = XChartProbit()
    chart.setAxesMinMax(-3,3,0,3)

    for i,set in enumerate(series):
        chart.addSeries(series[i])
        chart.setAxes(series[i])
    for i,set in enumerate(series):
        chart.addSeries(seriesn[i])
        chart.setAxes(seriesn[i])

        
    chart.axisY.setRange(ymin,ymax)
    #print(chart.axesMinMax())
        
    chart.setTitle("Simple Scatter example")
    chart.setAnimationOptions(QChart.SeriesAnimations)
    
    #chart._removeHorizontalGridLine()
    
    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignBottom)

    chartView = QChartView(chart)
    chartView.setRenderHint(QPainter.Antialiasing)

    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(800, 600)
    window.show()

    chart._logrange(0.2,100)
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()