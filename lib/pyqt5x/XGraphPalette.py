"""XGraphPalette

This file contains the colour definitions for the trib application.

"""

from PyQt5 import QtGui


"""
Contains all the colour definitions necessary for items in Trib.
"""

colours = {'tribBlue' : [139, 218, 249],
           'tribCoral': [255, 127, 127],
           'tribSnow' : [250, 250, 250],
           'tribOlive': [154, 188, 171],
           'tribStone': [93, 87, 107]
          }

def createcolor(name, r,g,b,alpha=255):
    color = QtGui.QColor(r, g, b, alpha=alpha)
    color.setNamedColor(name)
    return color

tribBlue  = createcolor('tribBlue',  *colours['tribBlue'])
tribCoral = createcolor('tribCoral', *colours['tribCoral'])    
tribSnow  = createcolor('tribSnow',  *colours['tribSnow'])
tribOlive = createcolor('tribOlive', *colours['tribOlive'])
tribStone = createcolor('tribStone', *colours['tribStone'])

def main():
    print(tribBlue)
    
    
if __name__ == "__main__":
    main()