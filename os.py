# #!/usr/bin/env python

import os

#Get the current OS Name
print('OS Name: ' + os.name)
#Get the current working dir
print('\n')
print('Current working directory: ' + os.getcwd())
#List the files and dirs in the current dir
print('\n')
print('Contents of the current working directory: ')
print( os.listdir('.'))

try:
    filename = 'rootzones.txt'
    f = open(filename, 'rU')
    text = f.read()
    f.close()
except IOError:
    print('\n')
    print('Problem reading: ' + filename)

"""
the below will be useful for the deployment script to add zones
the input parameter can be input from the bash script and it will
continue to write new zones until there is no more input
"""
rootzones = "rootzones.txt"
try:
    file = open(rootzones, 'w')
    file.write("Hello")
    file.close()
    file = open(rootzones, 'r')
    rootzonesOut = file.read()
    print('\n')
    print('Output of \"' + rootzones + '\" that we just wrote to: ' + rootzonesOut)
except IOError:
    print('\n')
    print('Problem with: ' + rootzones)