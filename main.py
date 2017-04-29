'''
trib_main.py

Antony Hallam
2017-04-25
'''


import sys
from PyQt5 import QtGui,QtWidgets

from qtgui import tribGui

def main():
	app = QtWidgets.QApplication(sys.argv)
	form = tribGui.tribApp()
	form.show()
	app.exec_()
	
if __name__ == '__main__':
	main()

