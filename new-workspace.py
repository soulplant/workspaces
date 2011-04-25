#!/usr/bin/python

from __future__ import with_statement

import os
import glob
import optparse

WORKSPACE_DIR = os.path.join(os.path.expanduser('~'), '.workspaces')

(options, args) = optparse.OptionParser().parse_args()

if len(args) < 1:
    print "usage: nw workspace_name [files]"
    exit(1)

project_path = os.getcwd()
project_name = args.pop(0)

files = []
for arg in args:
    files.extend(glob.glob(arg))

with open(os.path.join(WORKSPACE_DIR, project_name), 'w') as f:
    f.write(project_path + "\n\n")
    [f.write(file + "\n") for file in files]
