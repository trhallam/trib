"""env.py

Run this application with additional function to call to ensure all environments are defined

Antony Hallam
2017-04-25

Options:
    -h --help       Loads this help documentation
    -p --paths      Adds subfolders of trib directory to sys.path if missing.
    -o --openfile   Opens a session .json file
    
Examples:
    
"""

import getopt, sys, os, inspect

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
	
#from tribgui.widgetIDTable import *
from tribgui.widgetIDChart import *

if __name__ == "__main__":
    main()