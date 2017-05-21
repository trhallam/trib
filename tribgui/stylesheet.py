"""stylesheet

This file contains the styles of the trib program

"""
from tribgui.colourpack import tribColours


def coloursub(sss):
    # Takes sss the style sheet string and replaces references to know colour keys with rgb text values.
    rgb = tribColours.rgbDict()
    for key in rgb:
        rgbv = rgb[key]; print(rgbv)
        sss=sss.replace(key, 'rgb(%d, %d, %d)'%(rgbv[0],rgbv[1],rgbv[2]))
    return sss


def tribmainstyle(widget):
    widget.setStyleSheet("""
        QWidget {
            background-color: rgb(250, 250, 250);
            selection-color: rgb(93, 87, 107);
            selection-background-color: rgb(139, 218, 249);
            }
            
        """)


def tribtablestyle(widget):
    widget.setStyleSheet(coloursub("""
        QTableWidget {
            selection-color: tribStone;
            selection-background-color: tribBlue;
            font: bold 9pt;
            font-family: 'Ariel'
        }
        """))

def tribchartmenustyle(widget):
    widget.setStyleSheet(coloursub("""
        QPushButton {
                background : tribSnow;
                border: None
                 }
                
        QPushButton:hover {
                border: 2px solid tribBlue;
                       }
        """))



def main():
    rgb = tribColours.rgbDict()
    print(rgb)

    teststring = """
    QPushButton!:hover {
                background : tribSnow;
                 }
                
    QPushButton:hover {
                border: 2px solid tribStone;
                backgroundL tribStone
                       }
    """

    print (teststring)
    print (coloursub(teststring))

if __name__ == "__main__":
    main()