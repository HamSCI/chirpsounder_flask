#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# enable debugging
#import cgitb
#cgitb.enable()

import sys
import os

file_dir = os.path.dirname(__file__)
ret0 = sys.path.insert(0,file_dir)

from chirpsounder_flask import app as application
