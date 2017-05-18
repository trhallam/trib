"""tribColours

This file contains the colour definitions for the trib application.

"""

from PyQt5 import QtGui


"""
Contains all the colour definitions necessary for items in Trib.
"""

colours = {'tribBlue' : '#8BDAF9',
           'tribCoral': '#FF7F7F',
           'tribSnow' : '#FAFAFA',
           'tribOlive': '#9ABCAB',
           'tribStone': '#5D576B'
          }

class ColourPack(object):
    def __init__(self):
        self._cdd = dict()
        
    def addColour(self, name, rgbhex):
        self._cdd[name] = rgbhex
        colour = QtGui.QColor()
        colour.setNamedColor(rgbhex)
        self.__setattr__(name, colour)
        
    def namedColours(self):
        return self._cdd.keys()

tribColours = ColourPack()
    
for col in colours:
    tribColours.addColour(col, colours[col])
   
def main():
    import sys
    from PyQt5.QtWidgets import (QApplication, QGridLayout, QWidget,
        QLabel)
    from PyQt5.QtGui import QPalette, QColor
    from PyQt5 import Qt


    class GridWidget(QWidget):
        
        def __init__(self):
            super().__init__()
            
            self.initUI()
            
        def initUI(self):
            grid = QGridLayout()
            self.setLayout(grid)
            labellist = []; colourlist = []; pallist = [];    
            for i, col in enumerate(tribColours.namedColours()):
                lab = QLabel(); lab.setText(col)
                labellist.append(lab)
                grid.addWidget(labellist[i],i,0)
                collab = QLabel(); colourlist.append(collab)
                lpal = QPalette(); pallist.append(lpal)
                colourlist[i].setAutoFillBackground(True)
                pallist[i].setColor(QPalette.Window, tribColours.__getattribute__(col)); 
                colourlist[i].setPalette(pallist[i]); #
                grid.addWidget(colourlist[i],i,1)
            self.move(600, 500)
            self.setWindowTitle('tribPalette')
            self.show()

    app = QApplication(sys.argv)
    ex = GridWidget()
    sys.exit(app.exec_())
    
    
if __name__ == "__main__":
    main()