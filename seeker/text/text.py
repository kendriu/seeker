#!/usr/bin/env python
# -*- coding: utf-8 -*-
__all__=('Text',)

class Text():

    """
    Klasa bazowa dla wszystkich textów
    
    :version:
    :author: Andrzej Skupień
    """

    def __init__(self, original, stemmed):
        """
        @param string original : treść orginalna
        @param string stemmed : treść zestemmowana
        @author Andrzej Skupień
        """
        self.original = original
        self.stemmed = stemmed
    def __str__(self):
        return self.stemmed
    def split(self,sep,maxsplit = -1):
        return self.stemmed.split(sep,maxsplit)

import unittest

class TestText(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.ORIGINAL = 'tekst orginalny'
        self.STEMMED = 'tekst zestemowany'   
        self.text = Text(self.ORIGINAL,self.STEMMED)   
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def test__init__(self):      
        self.assertEqual(self.text.original,self.ORIGINAL , 'źle przypisana wartość orginalna')
        self.assertEqual(self.text.stemmed,self.STEMMED,'źle przypisana warość zestemmowana')
    
    def test__str__(self):
        self.assertEqual(self.STEMMED,str(self.text),'Tekst potraktowany jako string powinien zwracać wersję zestemmowaną')

        
if __name__ == '__main__':
    unittest.main()