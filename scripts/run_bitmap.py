#!/usr/bin/env python3

import sys
import getopt

from matrix import *

###########
avatar = """
    ###    
  #######  
 ######### 
 ######### 
##### #####
####   ####
##### #####
 ######### 
 ######### 
  #######  
    ###    
"""
###########

def main():
    opts, args = getopt.getopt(sys.argv[1:], "", ["reset", "test", "bitmap="])
    values = []

    for opt, arg in opts:
        if (opt == "--reset"):
            values = bitmap.hex()
        elif (opt == "--test"):
            values = bitmap.ascii(avatar, "0000FF00")
        elif (opt == "--bitmap"):
            values = bitmap.hex(arg)

    display.update(values)

if __name__ == '__main__':
    main()
