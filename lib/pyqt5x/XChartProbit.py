"""XChartProbit

This file contains functions which help build probit style charts using QtCharts

"""

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtChart import (QChart, QValueAxis, QChartView)


from pyqt5x.XChartTools import XLineSeries, XScatterSeries
from tufpy.stats import distr
        
from itertools import zip_longest
from scipy.stats import norm, linregress, lognorm, percentileofscore
from numpy import arange, insert, log10, array, append, power


class XChartProbit(QChart):
    def __init__(self, parent=None):
        super(QChart, self).__init__(parent)
        
        # Class Vars
        self.activeDistr ='lognorm'
        self.knowndistr = distr._distrnames()
        self.data = dict()

        # Axis Setup
        self.axisX = QValueAxis()
        self.axisY = QValueAxis()

        self.axisX.setLabelsVisible(False)
        self.axisX.setTickCount(2)
        self.axisX.setTitleText("Series Fractional Probability")
        self.axisY.setTitleText("Value")
        self.setAxesMinMax(-3,3,0.01,1.5)
        
        self.axisX.setMinorGridLineVisible(False)
        self.axisX.setGridLineVisible(False)
        
        # define the default grid colour to grey
        self.setGridColor(110,110,110)

        self.setActiveProbit(self.activeDistr)
        self.plotAreaChanged.connect(self.onPlotSizeChanged)
        # method needed for axes change to redraw grid lines
        
    def addLinearReg(self,seriesname):
        x = self.data[seriesname]['X'], y = self.data[seriesname][seriesname]
        # adds a linear regression line for a data set x,y
        slope, intercept, r_value, p_value, std_err = linregress(x,y)
        xmin = distr.distrppf(self.activeDistr, 0.01); xmax = distr.distrppf(self.activeDistr, 0.99)
        ymin = slope*xmin+intercept; ymax = slope*xmax+intercept
        data = dict()
        data['X'] = [xmin,xmax]; data['LinearReg'] = [ymin,ymax]
        lines = XLineSeries(data, xkey='X',openGL=True)
        
        self.addSeries(lines[0])
        self.setAxes(lines[0])

    def loadSeries(self, arr, name):
        # takes a list/array arr
        y = array(arr).copy(); y.sort()
        self.data[name] = y
        self.redrawChart()
        
    def plotSeries(self, name):
        nsamp = len(self.data[name])
        # add data to temport dictionary
        tdict = dict(); 
        if self.activeScale == 'log10':
            tdict[name] = log10(self.data[name])
        elif self.activeScale == 'linear':
            tdict[name] = self.data[name]
        tdict['X'] = distr.distrppf(self.activeProbit, [percentileofscore(self.data[name],self.data[name][i])/100.00001 for i in range(0,nsamp)])
        series  = XScatterSeries(tdict, xkey='X', openGL=True)
        self.addSeries(series[0])
        self.setAxes(series[0])
        
    def _replotData(self):
        for key in self.data.keys():
            self.pl
        
    def axesMinMax(self):
        # returns a length 4 list of the axes min and max values [x1,x2,y1,y2]
        return [self.axisX.min(), self.axisX.max(), self.axisY.min(), self.axisY.max()]
        
    def redrawChart(self):
        self.removeAllSeries()
        self._removeHorizontalGridLabels()
        self.resetAxes()
        self._drawVerticalGridLines()
        if self.activeScale == 'log10':
            self.axisY.setLabelsVisible(False)
            self.axisY.setTickCount(1)
            self.setTitle("Log Probit Plot")   
            self.axisY.setMinorGridLineVisible(False)
            self.axisY.setGridLineVisible(False)
            self._drawHorizontalGridLine()
            self._drawHorizontalLabels()
            self._drawHorizontalGridlLabels()
        elif self.activeScale == 'linear':
            self.axisY.setLabelsVisible(True)    
            self.axisY.setTickCount(10)
            self.setTitle("Probit Plot")               
            self.axisY.setMinorGridLineVisible(True)
            self.axisY.setGridLineVisible(True)
        
        for serkey in self.data.keys():
            self.plotSeries(serkey)
            
    def resetAxes(self):
        ymins = []; ymaxs = []
        for key in self.data.keys():
            ymins.append(min(self.data[key]))
            ymaxs.append(max(self.data[key]))
        try:
            ymin = min(ymins); ymax = max(ymaxs)
        except ValueError:
            ymin = 1.1; ymax = 2

        xmin = distr.distrppf(self.activeProbit, 0.001); xmax = distr.distrppf(self.activeProbit, 0.999)
        if self.activeScale == 'linear':
            yscal = 0.1 * (ymax - ymin)
            self.setAxesMinMax(xmin,xmax,ymin-yscal,ymax+yscal)
        elif self.activeScale == 'log10':
            yscal = 0.1 * (log10(ymax)-log10(ymin))
            self.setAxesMinMax(xmin,xmax,log10(ymin),log10(ymax))
            #self.setAxesMinMax(xmin,xmax,log10(ymin)-yscal,log10(ymax)+yscal*0.1)

    def setGridColor(self, r, g, b):
        # sets the colour of the background grid
        self.gridcolor = QColor(r,g,b)
    
    def setActiveProbit(self, type):
        if type in self.knowndistr:
            self.activeDistr = type
            if type == 'norm':
                self.activeProbit = 'norm'
                self.activeScale = 'linear'
            elif type == 'lognorm':
                self.activeProbit = 'norm'
                self.activeScale = 'log10'
        #self.redrawChart()
    
    def setActiveScale(self,newscale):
        self.activeScale = newscale
            
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
        vlabx = distr.distrppf(self.activeProbit, self.vgridx);
        vlabx = insert(vlabx, 0, xmin); vlabx = insert(vlabx, len(vlabx), xmax)
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
            self.hlabels[i].setPos(labx-0.5*self.hlabels[i].boundingRect().width(),pbly) #centre on tick marks
            
    def _drawVerticalGridLines(self):
        self.vgridx = arange(0.05, 1.0, 0.05)
        self.vgridx = insert(self.vgridx, 0, [0.01, 0.02]); 
        self.vgridx = insert(self.vgridx, len(self.vgridx), [0.98, 0.99])
        vgridy = [self.axisY.min(), self.axisY.max()]
        self.vgridseries = []
        for val in self.vgridx:
            line = 'P'+'%02d'%round(100.0*(1.0-val))
            tdict = {'X':[distr.distrppf(self.activeProbit,val)]*2, line:vgridy}
            self.vgridseries = self.vgridseries + XLineSeries(tdict, xkey = 'X', openGL=True)
        for i,line in enumerate(self.vgridseries):
            pen = line.pen()
            pen.setColor(self.gridcolor); pen.setWidthF(0.4), line.setPen(pen)
            line.setPointLabelsVisible(True)
            self.addSeries(line)
            self.setAxes(line)
            self.legend().markers(line)[0].setVisible(False)

    def _drawHorizontalGridLine(self):
        # calculate xmin and xmax points for lines to completely cross graph
        hgridx = [distr.distrppf(self.activeProbit, 0.0001)-1, distr.distrppf(self.activeProbit, 0.9999)+1]
        # calculate log scale for lines y values
        self.hgridy = self._logrange(10**self.axisY.min(), 10**self.axisY.max(), base=10)
        self.hgridseries = []
        # create a line series for each lines and add to list
        for val in self.hgridy:
            line = '%d'%val
            tdict = {'X':hgridx, line:[log10(val)]*2}
            self.hgridseries = self.hgridseries + XLineSeries(tdict, xkey = 'X', openGL=True)
        # add each of the series to the grid with special formatting
        for i, line in enumerate(self.hgridseries):
            pen = line.pen()
            pen.setColor(self.gridcolor); pen.setWidthF(0.4), line.setPen(pen)
            self.addSeries(line)
            self.setAxes(line)
            self.legend().markers(line)[0].setVisible(False)

    def _drawHorizontalGridlLabels(self):
        ymin = self.axisY.min(); ymax = self.axisY.max();
        axisScale = 1 / (ymax - ymin)  # scaler for plotted axis (reduces to 0-1.0)
        # calculate base10 values to scale from grid lines insert min and max values to scale correctly
        vlaby = log10(self.hgridy);
        vlaby = insert(vlaby, 0, ymin);
        vlaby = insert(vlaby, len(vlaby), ymax)
        vlaby = (vlaby - ymin) * axisScale  # scale the probit value to ratios of the Xaxis length
        paw = self.plotArea().width();
        pah = self.plotArea().height()  # find the plot width and height
        # find plot bottom left corner X and Y
        pblx = self.plotArea().bottomLeft().x();
        pbly = self.plotArea().bottomLeft().y()
        # offset from axix by 10 pixels -> may need to automate this offset in future
        pblx_lab = pblx - 10
        # calculate the position on the chart in y plane with which to place each label.
        pbly = [pbly - int(pah * y) for y in vlaby[1:-1]]
        self.vlabels = []
        for i, labx in enumerate(pbly):  # run through labels and create and position them
        # label text based on P scale
            ltext = str(self.hgridy[i]);
            self.vlabels.append(self.scene().addText(ltext))

        for i,laby in enumerate(pbly): #run through labels and create and position them
            # label text based on P scale
            self.vlabels[i].setPos(pblx-self.vlabels[i].boundingRect().width()-10,
                                   laby-0.5*self.vlabels[i].boundingRect().height()) #centre on tick marks

    def _removeHorizontalGridLine(self):
        for ser in self.hgridseries:
            self.removeSeries(ser)
            
    def _removeVerticalGridLine(self):
        for ser in self.vgridseries:
            self.removeSeries(ser)
            
    def _removeHorizontalGridLabels(self):
        try:
            for lab in self.vlabels:
                self.scene().removeItem(lab)
        except AttributeError:
            pass
            
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
        self.redrawChart()

        
def main():
    import sys
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPainter
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from numpy import random
    
    app = QApplication(sys.argv)

    rand = random.lognormal(size=100,mean=10,sigma=0.6)
    rand = rand.clip(min=1.1)

    chart = XChartProbit()
    chartView = QChartView(chart)

    chart.loadSeries(rand,"Log-Normal Rand")

    #chartView.chart.addLinearReg()
    
    chartView.setRenderHint(QPainter.Antialiasing)
    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(800, 600)
    window.show()
    
    #chartView.addLinearReg("Log-Normal Rand")
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()