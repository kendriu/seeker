#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2010-11-04

@author: andy
'''
from reader import *
from documents import *

class Manager():
    '''
    Klasa osłonowa dla czytników plików.
    Potrafi odczytać zawartość pliku ze słowami kluczowymi oraz plik z dokumentami
    '''
    
    def get_keywords_from(self,filepath):
        reader = Reader(filepath)
        return reader.get_content()
    
    def get_documents_from(self,filepath):
        reader = Documents(filepath)
        return reader.get_content()
        
        