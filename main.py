#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
/home/andy/workspace/seeker/src/main.py
'''
__author__ = 'andy'
__date__ = 2010-10-24

import seeker
from seeker import text
from seeker import file

seeker.gui.run(text.manager.Tfidf(),file.Manager())
