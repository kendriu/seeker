#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2010-11-04

@author: andy
'''
from reader import *

class Documents(Reader):
    '''
    klasa porafi odczytać plik dokumentów
    '''


    def __init__(self,filepath):
        Reader.__init__(self, filepath)
        self.buffer = []
    def get_content(self):
        self.__empty_buffer()
        return Reader.get_content(self)
    
    def _read_line(self,line):
        line = line.strip()
        if(len(line)):
            self.buffer.append(line)
        else:
            self.__empty_buffer()
            
    def __empty_buffer(self):
        if(len(self.buffer)):
            self.content.append('\n'.join(self.buffer))
            self.buffer = []
        