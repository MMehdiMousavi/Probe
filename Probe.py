##############################################################################
# IMPORTS, FLAGS, AND FOLDERS
##############################################################################
import os
import sys
import time

import numpy as np
from pykeyboard import PyKeyboard

from Probe_utils import MK, Probe, WindowMgr, KeyUtils, generate_settings

LINUX = 'linux'
WINDOWS = 'win32'

# Switch focus to the game window
if sys.platform == LINUX:
    # In Linux, we can shift focus to a window by using the wmctrl program

    gameName = "Loft (64-bit, PCD3D_SM5)"
    os.system('wmctrl -a ' + gameName)
elif sys.platform == WINDOWS:
    # In Windows, we can use the class defined above
    w = WindowMgr()


    w.find_window_wildcard(".*(64-bit, PCD3D_SM5)")
    w.set_foreground()

##############################################################################
# GLOBAL VARIABLES
##############################################################################
# to sense environment and move
delay = 0.75
burnintime = 1000
nSteps = 2
count = 0
stepsize = 8
current_location = np.zeros(2)
steps = np.zeros(nSteps)

##############################################################################
# REMEMBER
##############################################################################
# print(look_list)
# print(nextstep_list)

##############################################################################
# LOOKING AROUND RANDOMLY
##############################################################################
moves_file = "ProbeLog\Supercaustics.txt"

ku = KeyUtils()
pkey = Probe()
k = PyKeyboard()
generate_settings(10, moves_file)

##############################################################################
# GATHER DATA
##############################################################################
file = open(moves_file)
for i in range(nSteps):
    for action in list(file.readlines()):
        Mat, HDRI, Lighting = action.split()

        Mat = int(Mat)
        HDRI = int(HDRI)
        Lighting = int(Lighting)
        k.tap_key('M', n=Mat, interval=0.01)
        k.tap_key('H',n=HDRI, interval=0.01)
        k.tap_key('L', n=HDRI, interval=0.01)
        Probe.capture()
        Probe.reset()

# Pause at the end to avoid transitioning away from the game too abruptly
time.sleep(0.5)

# Switch focus back to the Python window
if sys.platform == LINUX:
    # Using Alt-Tab in Linux. A more robust way would be to identify the
    # window from which the script was launched
    ku.alt_tab()
elif sys.platform == WINDOWS:
    # Assumes that the Python script was launched from a command window
    w.find_window_wildcard(".*PyCharm*.")
    w.set_foreground()
