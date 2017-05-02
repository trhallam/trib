import sys, os, inspect

print(sys.argv)

print(sys.path)

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
	
print(sys.path)