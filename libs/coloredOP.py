#!/usr/bin/python3  

# coloredOP : generate Colored output. 
# Consider README.md for more info.  

import os
color = True # colored output 

if os.name == 'nt' or os.name == 'mac':
    color = False	

# colors
class colors:
    if color:
        RED = '\x1b[91m'        # red 
        GREEN = '\x1b[92m'      # green
        ORANGE = '\x1b[93m'     # orange
        BLUE = '\x1b[94m'       # blue
        PURPLE = '\x1b[95m'     # purple
        CYAN = '\x1b[36m'       # cyan
        GREY = '\x1b[97m'       # Grey
        BYELLOW = '\x1b[97;43m' # yellow background
        BGREEN = '\x1b[97;42m'  # green background
        BRED = '\x1b[97;41m'    # red background
    else:
        RED = GREEN = ORANGE = BLUE = PURPLE = CYAN = GREY = BYELLOW = BGREEN = BRED = END = ''

# bullets 
class bullets:
    if color:
        INFO = '\x1b[1m\x1b[97m[!]\x1b[0m'     # informational bullet '[!]'
        ERROR = '\x1b[1m\x1b[91m[-]\x1b[0m'    # ERROR bullet '[-]'
        CProcess = '\x1b[1m\x1b[93m[*]\x1b[0m' # process/progress bullet '[*]'
        OK = '\x1b[1m\x1b[92m[+]\x1b[0m'       # OK/GOOD bullet '[+]'
        DONE = '\x1b[1m\x1b[96m[+]\x1b[0m'     # informational bullet '[+]'
        DEBUG = '\x1b[1m\x1b[95m[~]\x1b[0m'    # debug bullet '[~]'
    else:
        INFO = '[!]'
        ERROR = '[-]'
        CProcess = '[*]'
        OK = '[+]'
        DONE = '[+]'
        DEBUG = '[~]'

# char attribs
if color:
    BOLD = '\x1b[1m'       # bold 
    UNDERLINE = '\033[4m'  # underline
    END = '\x1b[0m'        # end the colored string
else:
    BOLD = UNDERLINE = END = ''
