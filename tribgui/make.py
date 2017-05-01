"""make.py

Antony Hallam
2017-04-27

script to call pyuic5 to make all the tribDesign UI from Qt Designer
"""

from subprocess import call, check_output
from os.path import join
import os

print(os.getcwd())

maker ='pyuic5'
indir = '_qtdesigner'
intype = '.ui'
outtype = '.py'

uiFiles = ['tribDesignMainWindow',        # main window
            'tribDesignDialogAbout',      # about dialog window
            'tribDesignFDTables'          # main window2
           ]

rcmaker = 'pyrcc5'
intyperc = '.qrc'
outtyperc = '_rc.py'
rcFiles = ['tribDesignResource'       # icons etc
           ]

for file in uiFiles:
    infile = join(indir, file+intype)
    outfile = join(indir, file+outtype)
    call([maker, infile, '-o', outfile])

for file in rcFiles:
    infile = join(indir, file+intyperc)
    outfile = join(indir, file+outtyperc)
    call([rcmaker, infile, '-o', outfile])
