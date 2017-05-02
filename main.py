"""main.py

Main function for trib application

Antony Hallam
2017-04-25

Has sys.argv options
	
	-p		Adds subfolders of trib directory to sys.path if missing.

"""


import sys, os, inspect

trib_folder = os.path.realpath(os.path.abspath(os.path.dirname(
						inspect.getfile( inspect.currentframe() ))))

# sort out missing pythong path variables with -p option
if '-p' in sys.argv:
	if trib_folder not in sys.path:
		sys.path.insert(0,trib_folder)
		
	subpaths = ['lib', 'tribgui', os.path.join('tribgui','_qtdesigner')]
	iter = 1
	for sub in subpaths:
		tribsubpath = os.path.join(trib_folder,sub)
		if tribsubpath not in sys.path:
			sys.path.insert(iter, tribsubpath)
			iter+=1

# connect to lib packages
libpath = os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())),'lib'))
# add libpath to sys.path
if libpath not in sys.path:
    sys.path.insert(0, libpath)

from PyQt5 import QtGui,QtWidgets
from tribgui import tribMainWindow
    
   
def main():
    app = QtWidgets.QApplication(sys.argv)
    form = tribMainWindow.tribMainApp()
    form.show()
    app.exec_()
	
if __name__ == '__main__':
	main()

