'''
make.py

Antony Hallam
2017-04-27

script to call pyuic5 to make all the tribDesign UI from Qt Designer
'''

from subprocess import call
from os.path import join

maker='pyuic5'
inputDir = '_qtdesigner'
inputType = '.ui'
outputType = '.py'

uiFiles = ['tribDesign', #main window
           'tribDialogAbout' #about dialog window
		  ]

#construct each file
for file in uiFiles:
    inFile = join(inputDir,file+inputType)
    outFile= file+outputType
    call([maker,inFile,'-o',outFile])