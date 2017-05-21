"""main.py

Main function for trib application

Antony Hallam
2017-04-25

Options:
    -h --help       Loads this help documentation
    -p --paths      Adds subfolders of trib directory to sys.path if missing.
    -o --openfile   Opens a session .json file
    
Examples:
    
"""

from PyQt5 import QtGui,QtWidgets
import getopt, sys, os, inspect
from os.path import expanduser, join

_debug = 0

global userhome
userhome = join(expanduser("~"),'Documents')

def usage():
    print (__doc__)


def main():
    argv = sys.argv[1:]
    open_on_load = False
    try:
        opts, args = getopt.getopt(argv, "hpo:d", ["help", "paths", "openfile"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-d':
            global _debug
            _debug = 1
        elif opt in ("-p", "--paths"):
            print('Loading Paths')
            trib_folder = os.path.realpath(os.path.abspath(os.path.dirname(
                inspect.getfile( inspect.currentframe() ))))
        
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
                
        elif opt in ("-o", "--openfile"):
            filename = arg
            if os.path.isfile(filename):
                open_on_load = True
            else:
                print('Únknown File: ',filename)
                sys.exit()

    from tribgui import mainWindow
            
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    mw = mainWindow.mainApp()

    if open_on_load:
      mw.openSession(filename)

    mw.show()
    app.exec_()

if __name__ == '__main__':
    main()

