"""XTableWidget

This class extends the pyqt5 QTableWidget

"""

from PyQt5 import QtWidgets
from PyQt5.Qt import pyqtSignal, pyqtSlot


class XComboBoxDict(QtWidgets.QComboBox):
    """
    Provides a class of Combo Box which displays nice text but returns simple coding names.
    """

    currentKeyChanged = pyqtSignal(str)
    currentValueChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(XComboBoxDict, self).__init__(parent)
        self.dictMap = dict()
        self.currentTextChanged.connect(self._onCurrentValueChanged)

    def addItem(self, indict):
        for key in indict:
            self.dictMap[key] = indict[key]
            super(XComboBoxDict, self).addItem(indict[key])

    def addItems(self, indict):
        self.addItem(indict)

    def currentKey(self):
        val = self.currentText()
        return self._keyfromname(val)

    def _keyfromname(self,search):
        for key, name in self.dictMap.items():
            if name == search:
                return key

    @pyqtSlot(str)
    def _onCurrentValueChanged(self, val):
        self.currentKeyChanged.emit(self._keyfromname(val))
        self.currentValueChanged.emit(val)

def main():
    import sys
    from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QLineEdit, QLabel

    class GridWidget(QWidget):
        def __init__(self):
            super().__init__()
            self.setMinimumWidth(300)
            self.initUI()

        def initUI(self):
            grid = QGridLayout()
            self.setLayout(grid)
            self.cbox = XComboBoxDict()

            grid.addWidget(self.cbox, 1, 1, 1, 2)

            labKeys = QLabel(); labKeys.setText('Keys:')
            editKeys = QLineEdit();
            grid.addWidget(labKeys, 2, 1, 1, 1)
            grid.addWidget(editKeys, 2, 2, 1, 1)
            labValues = QLabel(); labValues.setText('Values:')
            editValues = QLineEdit();
            grid.addWidget(labValues, 3, 1, 1, 1)
            grid.addWidget(editValues, 3, 2, 1, 1)

            self.cbox.currentKeyChanged.connect(editKeys.setText)
            self.cbox.currentValueChanged.connect(editValues.setText)
            self.move(400, 400)
            self.setWindowTitle(' Test QComboBoxDict')
            self.show()

    app = QApplication(sys.argv)
    ex = GridWidget()
    ex.cbox.addItem({'A': 'a'})
    ex.cbox.addItems({'B':'b', 'C':'c'})
    print(ex.cbox.currentKey())
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()