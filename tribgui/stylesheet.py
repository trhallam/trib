"""stylesheet

This file contains the styles of the trib program

"""
from tribgui.colourpack import tribColours


def coloursub(sss):
    # Takes sss the style sheet string and replaces references to know colour keys with rgb text values.
    rgb = tribColours.rgbDict()
    for key in rgb:
        rgbv = rgb[key]
        sss=sss.replace(key, 'rgb(%d, %d, %d)'%(rgbv[0],rgbv[1],rgbv[2]))
    return sss


def tribmainstyle(widget):
    widget.setStyleSheet(coloursub("""
        QWidget {
            background-color: tribSnow;
            selection-color: tribStone;
            selection-background-color: tribBlue;
            }
            
        """))


def tribtablestyle(widget):
    widget.setStyleSheet(coloursub("""
        QTableWidget {
            background-color: white;
            selection-color: tribStone;
            selection-background-color: tribBlue;
            font: 9pt;
            font-family: 'Ariel'
        }
        
        QComboBox {
                font: 9pt;
                font-family: 'Ariel';
                min-height: 30px
        }
        """))

def tribchartmenustyle(widget):
    widget.setStyleSheet(coloursub("""
        QPushButton {
                background : tribSnow;
                border: None
                 }
                
        QPushButton:hover {
                border: 1px solid tribBlue;
                background : rgba(139, 218, 249, 50%)
                       }
                       
        QComboBox {
                font: 9pt;
                font-family: 'Ariel';
                min-height: 24px
        }
        """))

def tribaboutdialogstyle(widget):
    widget.setStyleSheet(coloursub("""
        QPushButton {
                background : tribSnow;
                border: None;
                 }

        QPushButton:hover {
                border: 1px solid tribBlue;
                background : rgba(139, 218, 249, 50%);
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