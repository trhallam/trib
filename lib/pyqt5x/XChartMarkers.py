"""XChartMarkers

Definitions for a whole heap of chart markers.

"""

from PyQt5.QtChart import QScatterSeries, QXYSeries, QValueAxis
from PyQt5.QtChart import QChart, QChartView
from PyQt5.QtCore import QObject, QPointF, pyqtSlot, pyqtSignal, Qt
from PyQt5.QtGui import QColor, QPen, QBrush, QPainterPath, QImage, QPainter, QPixmap, QFont
from PyQt5 import QtWidgets, QtGui
from itertools import zip_longest
import random, copy
import numpy as np

from XGraphColourPack import gaColours


class XMarkerBase(QBrush):
    """
    Base class from which other markers are derived.
    """
    def __init__(self, parent=None):
        super(XMarkerBase, self).__init__()
        self._wrs = 500.0
        self._hrs = 500.0
        self._width = 500.0
        self._height = 500.0
        self._opacity = 1.0
        self._renderscaling = 100.0

        
        self._penWidth=1
        self._rotationAngle=0
        
        colourpicker = round(random.uniform(2,len(gaColours)-1))
        colourkey = list(gaColours.namedColours())[colourpicker]
        self.setColour(gaColours.colour(colourkey))

    def setColour(self, Qcolor, pen='darker'):
        self._colour = Qcolor
        if pen == 'darker':
            self._bcolour = self._colour.darker()
        elif pen == 'same':
            self._bcolour = self._colour
        elif pen is QColor:
            self._bcolour = pen
        else:
            self._bcolour = QColor(0,0,0,0)
       
    def setFillRule(self, rule):
        self._image.path.setFillRule(rule)
        self.update()

    def setPenWidth(self, width):
        if width is None:
            self._penWidth=0
        else:
            self._penWidth = 0.8*width*min(self._wrs, self._hrs)/10.0
        self.update()

    def setPenColor(self, color):
        self.penColor = color
        self.update()

    def setRotationAngle(self, degrees):
        self._rotationAngle = degrees
        self.update()        
        
    def setPath(self):
        return QPainterPath()

    def update(self):
        image = QImage(self._wrs, self._hrs, QImage.Format_ARGB32_Premultiplied)
        path = self.setPath()
        painter = QPainter(image)
        #painter.setOpacity(self._opacity)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(
                QPen(self._bcolour, self._penWidth, Qt.SolidLine, Qt.RoundCap,
                        Qt.RoundJoin))
        painter.setBrush(self._colour)
        painter.drawPath(path)
        painter.end()
        pixmap = QPixmap()
        pixmap.convertFromImage(image.smoothScaled(self._width, self._height))
        #self.setTextureImage(pixmap)     
        self.setTexture(pixmap)
        
    def setBrush(self, width, height, border=2, opacity=None, fill_opacity=None, border_opacity=None):
        if opacity is not None:
            self._opacity = opacity
        #TODO use fill_opacity kwargs
        self._width = width; self._height = height; 
        #Border is scale 10-100% of minradius
        self.setPenWidth(border)
        self.update()
        
        
class XMarkerCircle(XMarkerBase):
    """
    Circle Marker which has a boundary, some transparency.
    """
    def __init__(self, parent=None):
        super(XMarkerCircle, self).__init__(parent)
        self.update()
        
    def setPath(self):
        path = QPainterPath()
        path.moveTo(self._wrs*0.97,self._hrs/2)
        # artTo (startx, starty, width, height, arcdeg start, arcdeg end)
        path.arcTo(self._wrs*0.03,self._hrs*0.03, self._wrs*0.94, self._hrs*0.94, 0.0, 360.0)
        return path

        
class XMarkerPlus(XMarkerBase):
    """
    Plus Sign
    """
    def __init__(self, parent=None):
        super(XMarkerPlus, self).__init__(parent)
        self._thick = .15
        self.update()
        
    def setPath(self):
        path = QPainterPath()
        thickw = self._thick*self._wrs; thickh = self._thick*self._hrs
        pw1 = self._wrs*0.05; pw2 = self._wrs/2-thickw/2; pw3 = pw2+thickw; pw4 = self._wrs-pw1
        ph1 = self._hrs*0.05; ph2 = self._hrs/2-thickh/2; ph3 = ph2+thickh; ph4 = self._hrs-ph1
        sequence = [(pw2, ph1), (pw3,ph1), (pw3,ph2), (pw4,ph2), (pw4,ph3), (pw3,ph3),
                    (pw3,ph4), (pw2, ph4), (pw2,ph3), (pw1,ph3), (pw1,ph2), (pw2,ph2)]
        path.moveTo(pw2,ph1)
        for point in sequence:
            path.lineTo(*point)
        path.closeSubpath()
        return path

class XMarkerDash(XMarkerBase):
    """
    Dash Sign
    """
    def __init__(self, parent=None):
        super(XMarkerDash, self).__init__(parent)
        self._thick = .15
        self.update()
        
    def setPath(self):
        path = QPainterPath()
        thickh = self._thick*self._hrs
        path.addRect(self._wrs*0.05,self._hrs/2-thickh/2,self._wrs*0.9,thickh)
        return path

class XMarkerSquare(XMarkerBase):
    """
    Square Box
    """
    def __init__(self, parent=None):
        super(XMarkerSquare, self).__init__(parent)
        self.setPath()
        self.update()
        
    def setPath(self):
        path = QPainterPath()
        path.addRect(self._wrs*0.17,self._hrs*0.17,self._wrs*0.66,self._hrs*0.66)
        return path
        
class XMarkerDiamond(XMarkerBase):
    """
    Diamon Shaped box
    """
    def __init__(self, parent=None):
        super(XMarkerDiamond, self).__init__(parent)
        self._rotationAngle=45
        self.update()
        
    def setPath(self):
        path = QPainterPath()
        path.moveTo(self._wrs*0.5,self._hrs*0.1)
        path.lineTo(self._wrs*0.9,self._hrs*0.5)
        path.lineTo(self._wrs*0.5, self._hrs*0.9)
        path.lineTo(self._wrs*0.1, self._hrs*0.5)
        path.closeSubpath()
        return path

        
class XMarkerCross(XMarkerBase):
    """
    A cross
    """
    def __init__(self, parent=None):
        super(XMarkerCross, self).__init__(parent)
        self._thick = .15
        self.update()
        
    def setPath(self):
        path = QPainterPath()
        thickw = self._thick*self._wrs; thickh = self._thick*self._hrs
        pw1 = self._wrs*0.2; pw2 = pw1+thickw*0.851;  pw4 = self._wrs/2; pw7=self._wrs*0.8
        pw3 = pw4-0.851*thickw; pw5 = pw4+0.851*thickw; pw6 = pw7 - thickw*0.851
        ph1 = self._hrs*0.2; ph2 = ph1+thickh*0.851;  ph4 = self._hrs/2; ph7=self._hrs*0.8
        ph3 = ph4-0.851*thickh; ph5 = ph4+0.851*thickh; ph6 = ph7 - thickh*0.851
        sequence = [(pw2, ph1), (pw4,ph3), (pw6,ph1), (pw7,ph2), (pw5,ph4), (pw7,ph6),
                    (pw6,ph7), (pw4, ph5), (pw2,ph7), (pw1,ph6), (pw3,ph4), (pw1,ph2)]
        
        path.moveTo(pw1,ph2)
        for point in sequence:
            path.lineTo(*point)
        path.closeSubpath()
        return path

class XMarkerTriangle(XMarkerBase):
    """
    A Triangle
    """
    def __init__(self, parent=None):
        super(XMarkerTriangle, self).__init__(parent)
        self.update()
        
    def setPath(self):
        path = QPainterPath()
        path.moveTo(self._wrs*0.5,self._hrs*0.2)
        path.lineTo(self._wrs*0.8,self._hrs*0.8)
        path.lineTo(self._wrs*0.2,self._hrs*0.8)
        path.closeSubpath()
        return path


def xtypemarker(series, fill=True, fillalpha=60, border=True, borderalpha=255, size=10, width=2):
        colourpicker = round(random.uniform(2,len(gaColours)-1))  # random colour
        colourkey = list(gaColours.namedColours())[colourpicker]
        colour = gaColours.colour(colourkey)
        if border == 'darker':       # if border is darker
            bcolour = bcolour.darker()
        if fill == False:            # set the fill of the object
            fillalpha = 0
        elif isinstance(fill, QColor):
            colour = fill
        colour.setAlpha(fillalpha)     # set opacity of object
        if border:
            bcolour = copy.copy(colour)    # border colour
            bcolour.setAlpha(borderalpha)  # set opacity of border
        else:
            bcolour = QColor(0,0,0,0)
        # fix the width to be between 1-10 of half size
        pen = QPen(bcolour)            # set border pen
        width = width*0.5*size/10.0; pen.setWidth(width)
        # setup series
        series.setColor(colour)
        series.setPen(pen)
        series.setMarkerSize(size)
        series.borderColorChanged.emit(bcolour)
        series.colorChanged.emit(colour)
        series.markerSizeChanged.emit(size)
        
def xtooltippath(point):
    print(point)
    path = QPainterPath()
    width = 100; height = 50; pointer=5
    path.lineTo(width,0), path.lineTo(width,height)
    path.lineTo(width/2+pointer,height); path.lineTo(width/2,height+pointer)
    path.lineTo(width/2-pointer,height); path.lineTo(0,height); path.lineTo(0,0)
    path.closeSubpath()
    path.translate(point.x()-width/2,point.y()-height-pointer)

    return path

    
class XToolTipLabel(QtWidgets.QLabel):
    def __init__(self, text, colour=None, left=True):
        super(XToolTipLabel,self).__init__(text)
        self._text = text.split('\n')
        self._pointersize = 5
        self.setContentsMargins(10,10,15+self._pointersize,10)
        self.setFont(QFont("Helvetica [Cronyx]", 12))
        self.setStyleSheet("background-color: rgb(0,0,0,0);")
        self._fillColour = Qt.white
        self.pen = QPen(Qt.black)
        if colour is not None:
            colour.setAlpha(255)
            self.pen = QPen(colour)

    def paintEvent(self, e):
        super(XToolTipLabel,self).paintEvent(e)  
        p = QtGui.QPainter(self)
        p.setPen(self.pen)
        p.setBrush(self._fillColour)
        p.setRenderHint(QtGui.QPainter.Antialiasing,True)
        p.drawPath(self.boundarypath())
        for i,text in enumerate(self._text):
            z=len(self._text)-i
            p.drawText(QPointF(10, self.height()-z*14-z*3),text)
        
    def boundarypath(self):
        path = QtGui.QPainterPath()
        width = self.width(); height = self.height(); pointer=self._pointersize
        path.lineTo(width,0), path.lineTo(width,height-pointer)
        path.lineTo(width/2+pointer,height-pointer); path.lineTo(width/2,height)
        path.lineTo(width/2-pointer,height-pointer); path.lineTo(0,height-pointer); path.lineTo(0,0)
        path.closeSubpath()    
        return path
        
def main():
    import sys
    from PyQt5.QtChart import QChart, QChartView
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPainter
    from PyQt5.QtWidgets import QApplication, QMainWindow
    
    import numpy as np
    
    @pyqtSlot(QPointF, bool)
    def help(point, state):
        print('help')
    
    app = QApplication(sys.argv)
    
    size = 50; bdr = 2; opc = 0.3
    special = False
    
    markers = [XMarkerCircle(),
               XMarkerPlus(),
               XMarkerDash(),
               XMarkerSquare(),
               XMarkerDiamond(),
               XMarkerCross(),
               XMarkerTriangle()]
   
    # Chart Setup
    chart = QChart()
    chart.axisX = QValueAxis(); chart.axisY = QValueAxis()
    chart.axisX.setTickCount(11); chart.axisY.setTickCount(11)

    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignBottom)
    chartView = QChartView(chart)
    chartView.setRenderHint(QPainter.Antialiasing)
    
    class scatser(QScatterSeries):
        def __init__(self, parent=None):
            super(scatser, self).__init__(parent)
            self.hovered.connect(self.onHovered)
            self.pen = QPen(Qt.black)
            
        
        @pyqtSlot(QPointF, bool)
        def onHovered(self, point, state):
            if state:
                spoint = self.chart().mapToPosition(point)-QPointF(0,size/2)
                self.ttip = XToolTipLabel('Hello from:\n x: %.1f, y: %.1f'%(point.x(), point.y()), colour = self.color())
                
                self.ttip_proxy = chart.scene().addWidget(self.ttip)
                w = self.ttip.width(); h = self.ttip.height();
                self.ttip_proxy.setPos(spoint.x()-w/2.0,spoint.y()-h)
                self.ttip.updateGeometry()
            else:
                self.ttip_proxy.deleteLater()

    
    mcount = 0; nm = len(markers)
    pos = [0.1, 0.3, 0.5, 0.7, 0.9]
    for i in pos:
        for j in pos:
            if mcount == nm:
                mcount = 0
            #print(mcount)
            m = markers[mcount]
            m.setBrush(size, size, border=bdr, opacity=opc)
            ser = scatser()
            
            ser.append(i,j)
            
            if special:
                ser.setBorderColor(QColor(1,1,1,1))
                ser.setMarkerSize(size)
                #ser.setMarkerShape(1)
                ser.setBrush(m)   
                
            else:
                xtypemarker(ser,size=size,width=bdr,fillalpha=50)
            chart.addSeries(ser)
            chart.setAxisX(chart.axisX, ser)
            chart.setAxisY(chart.axisY, ser)
            mcount += 1
    
    
    
    
    chart.axisX.setMin(0); chart.axisY.setMin(0)
    chart.axisX.setMax(1); chart.axisY.setMax(1)
    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(800, 800)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
