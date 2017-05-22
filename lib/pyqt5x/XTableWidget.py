"""XTableWidget

This class extends the pyqt5 QTableWidget

"""

from PyQt5 import QtWidgets


class XParameterTableWidget(QtWidgets.QTableWidget):

    def __init__(self, parent=None):
        super(QtWidgets.QTableWidget, self).__init__(parent)

        #Table Properties
        self.verticalHeader().setVisible(False)

    def addrow(self):
        n = self.rowCount()
        self.setRowCount(n+1)
        for col in range(0,self.columnCount()):
            self.setItem(n, col, QtWidgets.QTableWidgetItem(''))

    # not current working
    def addcol(self, name=None):
        n = self.columnCount()
        self.setColumnCount(n+1)
        self.getVerticalHeader()
        if name == None:
            i=1; name='Val'
            while name+'02%d'%i in self.headeritems:
                i += 1

    def getColumnWidth(self):
        twidth = self.width()
        self.widthratio = []
        for j in range(0, self.columnCount()):
            self.setCurrentCell(0,j)
            self.widthratio.append(self.currentColumn)

    def getHorizontalHeader(self):
        self.headeritems = []
        n = self.columnCount()
        for j in range(0, n):
            try:
                self.headeritems.append(self.horizontalHeaderItem(j).text())
            except AttributeError:
                self.headeritems.append(None)

    def resetColumnWidth(self):
        self.widthratio = 1.0/self.columnCount()

    def resizeEvent(self, resizeEvent):
        self.stretchtable()

    def returndata(self):
        nrows = self.rowCount(); ncols = self.columnCount()
        inrow = self.currentRow(); incol = self.currentColumn()
        data = dict()
        for j in range(0, ncols):
            temp = list()
            key = self.horizontalHeaderItem(j).text()
            for i in range(0,nrows):
                self.setCurrentCell(i, j)
                try:
                    temp.append(self.currentItem().text())
                except AttributeError:
                    temp.append('')
            data[key] = temp

        self.setCurrentCell(inrow, incol)
        return data

    def setdata(self, data, keyorder = None):
        if keyorder == None:
            keyorder = list(data.keys())
        #scan data
        max_i=0
        for j, key in enumerate(keyorder):
            max_i = max(max_i,len(data[key]))
        self.setSize(max_i+1, len(keyorder))
        for j, key in enumerate(keyorder):
            for i, item in enumerate(data[key]+['']):
                self.setItem(i, j, QtWidgets.QTableWidgetItem(str(item)))
        self.setHorizontalHeaderLabels(keyorder)

    def setBlankColumn(self, column):
        nrows = self.rowCount();
        inrow = self.currentRow(); incol = self.currentColumn()
        for i in range(0,nrows):
            self.setCurrentCell(i, column)
            self.currentItem()
            self.currentItem().setText('')
        self.setCurrentCell(inrow, incol)

    def setRowColour(self, row, colour):
        # QTableWidget, int, QColor
        nclm = self.columnCount()
        for ind in range(0, nclm):
            self.setCurrentCell(row, ind)
            self.currentItem().setBackground(colour)

    def colourTableByRow(self, rowflags, colourdict):
        #TODO could automatically extend rowflags to be white or a copy of rowflags for all rows
        inrow = self.currentRow(); incol = self.currentColumn()
        for i, row in enumerate(rowflags):
            self.setRowColour(i, colourdict[row])
        self.setCurrentCell(inrow, incol)

    def setSize(self, int_n, int_m):
        self.setColumnCount(int_m)
        self.setRowCount(int_n)

    def stretchtable(self):
        twidth = self.width()-30
        try:
            for j, pc in enumerate(self.widthratio):
                self.setColumnWidth(j, int((twidth)) * pc)
        except:
            self.resetColumnWidth()
            for j in range(0, self.columnCount()):
                self.setColumnWidth(j, twidth*self.widthratio)


