'''
trib_main.py

Antony Hallam
2017-04-25
'''


import sys, os, inspect

# connect to lib packages
libpath = os.path.abspath(\
            os.path.join(\
                os.path.dirname(inspect.getfile(inspect.currentframe()\
                        )),'lib'\
            )\
          )
# add libpath to sys.path
if libpath not in sys.path:
    sys.path.insert(0, libpath)

from PyQt5 import QtGui,QtWidgets
from tribgui import tribGui
    
   
def main():
	app = QtWidgets.QApplication(sys.argv)
	form = tribGui.tribApp()
	form.show()
	app.exec_()
	
if __name__ == '__main__':
	main()

