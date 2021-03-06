# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 10:17:28 2017

@author: tony
"""

import os, sys, inspect
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(\
                os.path.abspath(\
                    os.path.dirname(\
                        inspect.getfile( inspect.currentframe() ))))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

 # Info:
 # cmd_folder = os.path.dirname(os.path.abspath(__file__)) # DO NOT USE __file__ !!!
 # __file__ fails if script is called in different ways on Windows
 # __file__ fails if someone does os.chdir() before
 # sys.argv[0] also fails because it doesn't not always contains the path