#!/usr/bin/env python

# Filename: moreterm.py
# Description:
# This is the script to be run by the student to spawn more terminals.
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
#
# It will perform the following tasks:
# a. If the lab has only one container, only one terminal for that
#    container will be spawned
# b. If the lab has multiple containers, the number of terminals
#    specified in the start.config will be used, unless
#    the user passed the optional argument specifying the number of
#    terminal

import glob
import json
import md5
import os
import re
import subprocess
import sys
import time
import zipfile
from netaddr import *
import ParseStartConfig
import labutils

LABS_ROOT = os.path.abspath("../../labs/")

def DoMoreterm(start_config, mycwd, labname, container, num_terminal):
    mycontainer_name = '%s.%s.student' % (labname, container)
    if not labutils.IsContainerCreated(mycontainer_name):
        print('container %s not found' % mycontainer_name)
        exit(1)
    for x in range(num_terminal):
        spawn_command = "gnome-terminal -x docker exec -it %s bash -l &" % mycontainer_name
        #print "spawn_command is (%s)" % spawn_command
        os.system(spawn_command)

    return 0

def usage():
    sys.stderr.write("Usage: moreterm.py <labname> [<container>] [<requested_term>]\n")
    exit(1)

# Usage: (see usage)
def main():
    #print "moreterm.py -- main"
    num_args = len(sys.argv)
    print('numargs %d' % num_args)
    container = None
    requested_term = 1
    if num_args < 2:
        usage()
    elif num_args == 2:
        requested_term = 0
        container = sys.argv[1]
    elif num_args == 3:
        if type(sys.argv[2]) is int:
            requested_term = int(sys.argv[2])
            container = sys.argv[1]
        else:
            container = sys.argv[2]
    elif num_args == 4:
        requested_term = int(sys.argv[3])
        container = sys.argv[2]
    else:
        usage()

    labname = sys.argv[1]
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config")
    start_config_path = os.path.join(config_path,"start.config")

    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, "student")

    DoMoreterm(start_config, mycwd, labname, container, requested_term)

    return 0

if __name__ == '__main__':
    sys.exit(main())

