"""XGraphPalette

This file contains the colour definitions for the XCharting Tools.
Colours are by design as far from each other as possible.

kellycolours :: 
gacolours :: Green-Armytage, Paul, 2010, A Colour Alphabet and the Limits of Colour Coding

"""

"""
Contains all the colour definitions necessary for items in Trib.
"""

from PyQt5 import QtGui

kellycolours = {'white' : '#FFC9D7', 'black': '#131313', 'yellow' : '#FFB300', 'purple': '#803E75',
                'orange': '#FF6800', 'lightblue' : '#A6BDD7', 'red' : '#C10020', 'buff' : '#C2B280',
                'grey' : '#848482', 'green' : '#008856', 'purplishpink' : '#E68FAC', 'blue' : '#0067A5',
                'yellowishpink' : '#F99379', 'violet' : '#604E97', 'orangeyellow' : '#F6A600',
                'purplishred' : '#B32851', 'greenishyellow' : '#DCD300', 'reddishbrown' : '#7F180D',
                'yellowgreen' : '#8DB600', 'yellowishbrown' : '#654522', 'reddishorange' : '#F13A13',
                'olivegreen' : '#2B3D26'
                }

gacolours = {'white' : '#FFFFFF', 'black' : '#191919', 'yellow' : '#FFFF00',  'damson' : '#4C005C', 
             'zinnia' : '#FF5005', 'sky' : '#5EF1F2', 'red' : '#FF0010', 'xanthin' : '#FFFF80',
             'iron' : '#808080', 'green' : '#2BCE48', 'pink' : '#FFA8BB', 'blue' : '#0075DC',
             'honeydew' : '#FFCC99',  'violet' : '#740AFF', 'orpiment' : '#FFA405', 'mallow' : '#C20088',
             'uranium' : '#E0FF66', 'wine' : '#990000', 'lime' : '#9DCC00', 'caramel' : '#993F00',
             'amethyst' : '#F0A3FF', 'quagmire' : '#426600', 'jade' : '#94FFB5', 'navy' : '#003380',
             'khaki' : '#8F7C00', 'forest' : '#005C31', 'turquoise' : '#00998F'
            }

class ColourPack(object):
    def __init__(self):
        self._cdd = dict()
        self._order = list()
        
    def addColour(self, name, rgbhex):
        self._cdd[name] = rgbhex
        self._order.append(name)
        colour = QtGui.QColor()
        colour.setNamedColor(rgbhex)
        self.__setattr__(name, colour)
        
    def namedColours(self):
        return self._cdd.keys()
        
    def colourOrder(self):
        return self._order

gaColours = ColourPack()
kellyColours = ColourPack()
    
for col in gacolours:
    gaColours.addColour(col, gacolours[col])

for col in kellycolours:
    kellyColours.addColour(col, kellycolours[col])
   
def main():
    import sys
    from PyQt5.QtWidgets import (QApplication, QGridLayout, QWidget,
        QLabel)
    from PyQt5.QtGui import QPalette


    class GridWidget(QWidget):
        
        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):
            grid = QGridLayout()
            self.setLayout(grid)
            labellist = []; colourlist = []; pallist = [];    
            for i, col in enumerate(gaColours.namedColours()):
                lab = QLabel(); lab.setText(col)
                labellist.append(lab)
                grid.addWidget(labellist[i],i,0)
                collab = QLabel(); colourlist.append(collab)
                lpal = QPalette(); pallist.append(lpal)
                colourlist[i].setAutoFillBackground(True)
                pallist[i].setColor(QPalette.Window, gaColours.__getattribute__(col)); 
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