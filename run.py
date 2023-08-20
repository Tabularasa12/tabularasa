#!/usr/bin/python
# -*- coding : utf-8 -*-
import os
import sys
from utils.functions import clean_py_path
from flask.cli import main

args = sys.argv
path = os.path.dirname(__file__)

if os.path.basename(args[0]) == os.path.basename(__file__):
    os.chdir(path)
    if len(args) == 1:
        sys.argv = [path, "run"]
    elif len(args) > 1:
        if args[1] == 'clean':
            if len(args) == 3:
                if args[2] != 'apps':
                    path = os.path.join(path, args[2])
                else:
                    path = os.path.join(path, 'apps', args[2])
            clean_py_path(path)
        if  args[1] == 'debug':
            sys.argv = [path, "run", '--debug']
    if 'run' in sys.argv:
        main()



