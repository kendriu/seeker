#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2010-11-04

@author: andy
'''

class Reader(object):
    '''
    Klasa obługująca wyjątki przy czytaniu linii.
    Klasa odczytuje plik linia po linii.
    Zwraca poszczególne linie jako elementy krotki
    '''


    def __init__(self, filepath):
        self.filepath = filepath
        self.content = []
    
    def get_content(self):
        for line in file(self.filepath):
            self._read_line(unicode(line,'Latin-1'))
        return self.content
    
    def _read_line(self,line):
        line = line.strip();
        if(len(line)):
            self.content.append(line)
            
        