"""make.py

Antony Hallam
2017-04-27

script to call pyuic5 to make all the tribDesign UI from Qt Designer
"""

from subprocess import call, check_output
from os.path import join
import os

print(os.getcwd())

maker='pyuic5'
indir = '_qtdesigner'
intype = '.ui'
outtype = '.py'

uiFiles = ['tribDesign',      # main window
            'tribDialogAbout'  # about dialog window
           ]
# check files exist
for file in uiFiles:
    infile = join(indir, file+intype)
    outfile = file+outtype
    # print(infile, ':\t', os.path.isfile(infile))

    # check_output([maker, infile, '-o', outfile])

    call([maker, infile, '-o', outfile])