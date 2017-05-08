'''
test_XTableWidget.py

Antony Hallam
2017-04-29


test functions for XTableWidget.py
'''


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QAbstractScrollArea
from pyqt5x.XTableWidget import XParameterTableWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = XParameterTableWidget()

    w.setSize(4,4)

    w.getHorizontalHeader()
    print(w.headeritems)

    header = ['C1', 'C2', 'C3', 'C4']
    w.setHorizontalHeaderLabels(header)

    data = dict()
    for item in header:
        data[item] = [1,2,3,4,8]

    print(data)
    w.setdata(data)

    w.getHorizontalHeader()
    print(w.headeritems)

    #w.resetColumnWidth()
    w.stretchtable()

    w.getColumnWidth()
    w.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
    w.setColumnWidth(2, 28)

    w.resize(850, 450)
    w.move(300, 300)
    w.setWindowTitle('Simple')

    x=w.returndata()
    print(x)

    w.show()

    sys.exit(app.exec_())