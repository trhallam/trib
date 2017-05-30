"""XParameterTableWidget

This class builds it's own table model using an ordered dictionary 
 designed to be more functional and higher performance than 
 QTableWidget for a 2 column but many parameter table. 

Borrowed a lot here from itemmodels.py in OrangeData program.

"""

from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
from collections import OrderedDict, defaultdict

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


class XParameterModel(QtCore.QAbstractTableModel):

    @staticmethod
    def _RoleData(): # this is quite complicated and needs some more understanding
        return defaultdict(lambda: defaultdict(dict))

    def __init__(self, odict=None, parent=None, editable=False):
        super(QtCore.QAbstractTableModel, self).__init__(parent)
        self._hheaders = None
        self._editable = editable
        self._table = None
        self._roleData = None
        self._ndpoints = '%.5f'
        self.wrap(odict or [])

    def rowCount(self, parent=None):
        return 0 if parent.isValid() else len(self)

    def columnCount(self, parent=None):
        return 2

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return

        role_value = (self._roleData
                      .get(index.row(), {})
                      .get(index.column(), {})
                      .get(role))
        if role_value is not None:
            return role_value

        try:
            value = self[index.column()][index.row()]
        except IndexError:
            return
        if role == QtCore.Qt.EditRole:
            print(type(value))
            if type(value) is str:
                return value
            elif type(value) is float:
                return QtCore.QVariant(self._ndpoints%value)
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            if col == 0:
                return QtCore.QVariant("%s"%value)
            if col == 1:
                return QtCore.QVariant(self._ndpoints%float(value))
        return QtCore.QVariant()

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role == QtCore.Qt.DisplayRole:
            if Qt_Orientation == QtCore.Qt.Horizontal:
                return QtCore.QVariant("%s"%self._hheaders[p_int])
            if Qt_Orientation == QtCore.Qt.Vertical:
                return QtCore.QVariant()
        return QtCore.QVariant()

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            self[index.column()][index.row()] = value
            self.dataChanged.emit(index, index)
        else:
            print(dir(index.column()))
            self._roleData[index.column()][index.row()][role] = value
        return True

    def flags(self, index):
        flags = super().flags(index)
        if not self._editable or not index.isValid():
            return flags
        if isinstance(self._editable, OrderedDict):
            return flags | QtCore.Qt.ItemIsEditable if self._editable[index.column()] else flags
        return flags | QtCore.Qt.ItemIsEditable

    def __len__(self):
        return len(self._table[0])

    def __iter__(self):
        return iter(self._table)

    def __getitem__(self, item):
        return self._table[item]

    def wrap(self, odict):
        self.beginResetModel()
        self._table = list()
        self._hheaders = list(odict.keys())
        for key in odict.keys():
            self._table.append(odict[key])
        self._roleData = self._RoleData()
        self.endResetModel()

if __name__ == "__main__":
    import sys
    import string, random
    from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
    a = QApplication(sys.argv)
    w = QTableView()

    d = OrderedDict()
    d['Parameter']=list(string.ascii_lowercase)
    d['Value'] = [random.random() for char in d['Parameter']]
    m = XParameterModel(d, editable=True)
    print(m[0][10])
    w.setModel(m)

    w.show()
    a.exec_()