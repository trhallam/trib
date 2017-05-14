"""XChartProbit

This file contains functions which help build probit style charts using QtCharts

"""

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtChart import (QChart, QValueAxis, QChartView)

from XChartTools import XLineSeries, XScatterSeries
        
from itertools import zip_longest
from scipy.stats import norm, linregress, lognorm, percentileofscore
from numpy import arange, insert, log10, array, append, power


class XChartProbit(QChart):
    def __init__(self, parent=None):
        super(QChart, self).__init__(parent)

        # Axis Setup
        self.axisX = QValueAxis()
        self.axisY = QValueAxis()
        
        self.setAxesMinMax(-3,3,0.01,1.5)
        self.axisX.setLabelsVisible(False)
        self.axisY.setLabelsVisible(False)
        self.axisX.setTickCount(2)
        self.axisY.setTickCount(1)
        self.axisX.setTitleText("Series Fractional Probability")
        self.axisY.setTitleText("Value")
        self.setTitle("Log Probit Plot")
        
        self.axisX.setMinorGridLineVisible(False)
        self.axisX.setGridLineVisible(False)
        self.axisY.setMinorGridLineVisible(False)
        self.axisY.setGridLineVisible(False)
        
        #define the default grid colour to grey
        self.setGridColor(110,110,110)
        
        #draw the grid
        self._drawVerticalGridLines()
        self._drawHorizontalGridLine()
        
        self.plotAreaChanged.connect(self.onPlotSizeChanged)
        #method needed for axes change to redraw grid lines
        
    def addLinearReg(self,x,y):
        #adds a linear regression line for a data set x,y
        slope, intercept, r_value, p_value, std_err = linregress(x,y)
        xmin = norm.ppf(0.01); xmax = norm.ppf(0.99)
        ymin = slope*xmin+intercept; ymax = slope*xmax+intercept
        data = dict()
        data['X'] = [xmin,xmax]; data['LinearReg'] = [ymin,ymax]
        lines = XLineSeries(data, xkey='X',openGL=True)
        
        self.addSeries(lines[0])
        self.setAxes(lines[0])
        
    def axesMinMax(self):
        # returns a length 4 list of the axes min and max values [x1,x2,y1,y2]
        return [self.axisX.min(), self.axisX.max(), self.axisY.min(), self.axisY.max()]
        
    def setGridColor(self,r,g,b):
        # sets the colour of the background grid
        self.gridcolor = QColor(r,g,b)
    
    def setAxes(self,series):
        # assigns a series to the chart default axes
        self.setAxisX(self.axisX, series); self.setAxisY(self.axisY, series)
    
    def setAxesMinMax(self,x1,x2,y1,y2):
        # sets the min max values in X and Y 
        self.axisX.setMin(x1); self.axisX.setMax(x2)
        self.axisY.setMin(y1); self.axisY.setMax(y2)
        
    def _drawHorizontalLabels(self):
        xmin = self.axisX.min(); xmax = self.axisX.max()
        axisScale = 1/ (xmax - xmin) # scaler for plotted axis (reduces to 0-1.0)
        # calculate probit values to scale from grid lines insert min and max values to scale correctly
        vlabx = norm.ppf(self.vgridx); vlabx = insert(vlabx, 0, xmin); vlabx = insert(vlabx, len(vlabx), xmax)
        vlabx = (vlabx-xmin)*axisScale #scale the probit value to ratios of the Xaxis length
        paw = self.plotArea().width(); pah = self.plotArea().height() #find the plot width and height
        # find plot bottom left corner X and Y
        pblx = self.plotArea().bottomLeft().x(); pbly = self.plotArea().bottomLeft().y() 
        # offset from axix by 10 pixels -> may need to automate this offset in future
        pbly_lab = pbly+10
        # calculate the position on the chart in x plane with which to place each label.
        pblx = [pblx+int(paw*x) for x in vlabx[1:-1]]
        try:
            self.hlabels
        except AttributeError:
            self.hlabels=[]    
            for i,labx in enumerate(pblx): #run through labels and create and position them
                # label text based on P scale
                ltext = 'P'+'%02d'%round(100.0*(1.0-self.vgridx[i]))
                self.hlabels.append(self.scene().addText(ltext))            
        
        for i,labx in enumerate(pblx): #run through labels and create and position them
            # label text based on P scale
            self.hlabels[i].setPos(labx-0.5*self.hlabels[i].boundingRect().width(),pbly) #centre on tick marks
            
    def _drawVerticalLabels(self):
        ymin = self.axisY.min(); ymax = self.axisY.max()
        axisScale = 1/ (ymax - ymin) # scaler for plotted axis (reduces to 0-1.0)
        # calculate base10 values to scale from grid lines insert min and max values to scale correctly
        vlaby = log10(self.hgridy); vlaby = insert(vlaby, 0, ymin); vlaby = insert(vlaby, len(vlaby), ymax)
        vlaby = (vlaby-ymin)*axisScale #scale the probit value to ratios of the Xaxis length
        paw = self.plotArea().width(); pah = self.plotArea().height() #find the plot width and height
        # find plot bottom left corner X and Y
        pblx = self.plotArea().bottomLeft().x(); pbly = self.plotArea().bottomLeft().y() 
        # offset from axix by 10 pixels -> may need to automate this offset in future
        pblx_lab = pblx-10
        # calculate the position on the chart in y plane with which to place each label.
        pbly = [pbly-int(pah*y) for y in vlaby[1:-1]]
        try:
            self.vlabels
        except AttributeError:
            self.vlabels=[]    
            for i,labx in enumerate(pbly): #run through labels and create and position them
                # label text based on P scale
                ltext = str(self.hgridy[i]);
                self.vlabels.append(self.scene().addText(ltext))            
        
        for i,laby in enumerate(pbly): #run through labels and create and position them
            # label text based on P scale
            self.vlabels[i].setPos(pblx-self.hlabels[i].boundingRect().width()-10,
                                    laby-0.5*self.hlabels[i].boundingRect().height()) #centre on tick marks        
        
    def _drawVerticalGridLines(self):
        self.vgridx = arange(0.05, 1.0, 0.05)
        self.vgridx = insert(self.vgridx, 0, [0.01, 0.02]); 
        self.vgridx = insert(self.vgridx, len(self.vgridx), [0.98, 0.99])
        vgridy = [self.axisY.min(), self.axisY.max()]
        self.vgridseries = []
        for val in self.vgridx:
            line = 'P'+'%02d'%round(100.0*(1.0-val))
            tdict = {'X':[norm.ppf(val)]*2, line:vgridy}
            self.vgridseries = self.vgridseries + XLineSeries(tdict, xkey = 'X', openGL=True)
        for i,line in enumerate(self.vgridseries):
            pen = line.pen()
            pen.setColor(self.gridcolor); pen.setWidthF(0.4), line.setPen(pen)
            line.setPointLabelsVisible(True)
            self.addSeries(line)
            self.setAxes(line)
            self.legend().markers(line)[0].setVisible(False)

    def _drawHorizontalGridLine(self):
        hgridx = [norm.ppf(0.01)-1, norm.ppf(0.99)+1]
        self.hgridy = self._logrange(10**self.axisY.min(), 10**self.axisY.max(), base=10)
        self.hgridseries = []
        for val in self.hgridy:
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
        while bpow < max:
            y += 1; bpown = pow(base,y)
            out = append(out, arange(bpow,bpown,bpow))
            bpow = bpown
        i=0; j=0
        for ind,val in enumerate(out):
            if val <= min:
                i=ind
            if val <= max:
                j=ind
        return out[i:j+1]
        
    @pyqtSlot()
    def onPlotSizeChanged(self):
        #reset position of labels
        self._drawHorizontalLabels()
        self._drawVerticalLabels()

        
class XChartViewProbit(QChartView):
    """
    Widget to Hangle the setup and input output related to a Probit Style Chart
    
    Has functionality for Log-Probit at the moment. Will extent to Normal Probit Soon.
    """

    def __init__(self, parent=None):
        super(QChartView, self,).__init__(parent)
        self.style = 'Log10'

        self.chart = XChartProbit()   
        self.setChart(self.chart)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)        
        
        self.data = {}
        
        
    def addSeries(self,arr,name):
        #takes a list/array arr
        nsamp = len(arr)
        y = array(arr).copy(); y.sort()
        # add data to temport dictionary
        tdict = dict(); 
        if self.style == 'Log10':
            tdict['X'] = norm.ppf([percentileofscore(y,y[i])/100.00001 for i in range(0,nsamp)])
            tdict[name] = log10(y)
            
        self.data[name] = tdict
        series = XScatterSeries(tdict, xkey='X', openGL=True)
        self.chart.addSeries(series[0])
        self.chart.setAxes(series[0])
        
    def addLinearReg(self,series_name):
        self.chart.addLinearReg(self.data[series_name]['X'],self.data[series_name][series_name])

        
def main():
    import sys
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPainter
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from numpy import random
    
    app = QApplication(sys.argv)

    rand = random.lognormal(size=50,mean=2,sigma=0.1); randn = random.normal(size=50,loc=10,scale=5)
    rand = rand.clip(min=1.1); randn = randn.clip(min=1.1)

    chartView = XChartViewProbit()    
    chartView.addSeries(rand,"Log-Normal Rand")
    chartView.addSeries(randn,"Normal Rand")
    
    #chartView.chart.addLinearReg()
    
    chartView.setRenderHint(QPainter.Antialiasing)
    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(800, 600)
    window.show()
    
    chartView.addLinearReg("Log-Normal Rand")
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()