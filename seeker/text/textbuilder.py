#!/usr/bin/env python
# -*- coding: utf-8 -*-

from porterstemmer import *
from query import *
from text import *
import string
import unittest

__all__=('Text_Builder','translate_non_alphanumerics')

class Text_Builder(object):

    """
     Klasa budująca obiekty klasy Text. Obiekty zwracane mają ustawioną zestemmowaną
     wersję.

    :version:
    :author: Andrzej Skupień
    """

    def __init__(self, stemmer):
        self.stemmer = stemmer

    def get_keyword_for(self, string):
        text = Text(string,self.__stemm_string(string));
        
        return text

    def get_document_for(self, string):
        text = Text(string,self.__stemm_string(string))
        text.title,rest = string.split('\n',1)
        return text
    def get_categorized_document_for(self, string):
        category,string = string.split('\n',1)     
        text = Text(string,self.__stemm_string(string))
        text.category = category
        return text

    def get_query_for(self, string):
        query = Query(string,self.__stemm_string(string))
        return query
    
    def __stemm_string(self,string):
        '''
        Zwraca zestemmowaną postać stringa. Dodatkowo duże litery są zamieniane na małe oraz
        oraz usuwane są znaki zdefinoiowane w self.ILEGALCHARACTERS
        '''
        #usunięcie niedozwolonych znaków i zamiana dużych liter na małe
        string = translate_non_alphanumerics(string).lower()
        #podział stringu na słowa
        splitted = string.split(None)
        
        #stemmonwanie wyrazów i zwrot wersji zestemowanej
        return ' '.join((self.stemmer.stem(x,0,len(x)-1) for x in splitted))

def translate_non_alphanumerics(to_translate, translate_to=u' '):
    not_letters_or_digits = u'!"#%\'()*+,-./:;<=>?@[\]^_`{|}~'
    if isinstance(to_translate, unicode):
        translate_table = dict((ord(char), unicode(translate_to))
                               for char in not_letters_or_digits)
    else:
        assert isinstance(to_translate, str)
        translate_table = string.maketrans(not_letters_or_digits,
                                           translate_to
                                              *len(not_letters_or_digits))
    return to_translate.translate(translate_table)


class Test_Text_Builder(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.text_builder = Text_Builder(PorterStemmer())
        self.STRING = 'This are some strings. String contains: flies, elements and other words.'
        self.STEMMED = 'thi ar some string string contain fli element and other word'
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def test__init__(self):
        string = 'jakis string'
        builder = Text_Builder(string)
        self.assertEqual(string, builder.stemmer)
    
    def test_keyword_for(self):
        keyword = self.text_builder.get_keyword_for(self.STRING)
        expected = Text(self.STRING,self.STEMMED);
        self.assertTextsEqual(keyword, expected)
    
    def test_Non_UTF_Characters(self):
        docs = ('''GMU Machine Learning and Inference Laboratory
... 2002 Copyright Š 2002-2003 Machine Learning and Inference Laboratory
Front page created by Guido Cervone and Janejira Kalsmith. ... 
Description: Research on Theories of Learning, Inference, and Discovery Data Mining and Knowledge Discovery, User...
''','''Yahoo! Groups : machine-learning
machine-learning ˇ Machine Learning, [ Join This Group! ]. Home, Messages, Links,
Members Only, Chat, ... Machine Learning mailing list: machine-learning@egroups.com. ... 
Description: An unmoderated mailing list intended for people in computer sciences, statistics, mathematics, and...
        ''' )
        
        x =  [self.text_builder.get_document_for(doc) for doc in docs]
        

    def test_document_for(self):
        title = 'This is title with flies.'
        title_stemmed = 'thi is titl with fli'
        string = '\n'.join((title,self.STRING,self.STRING))
        stemmed = ' '.join((title_stemmed,self.STEMMED,self.STEMMED))
        document = self.text_builder.get_document_for(string)
        expected = Text(string,stemmed)
        expected.title = title
        self.assertTextsEqual(document, expected)
        self.assertHasAttribute('title', document, 'TextBuilder nie ustawił tytułu')
        self.assertEqual(document.title,expected.title,'TextBuilder źle ustawił tytuł dokumentu')
  
    def test_query_for(self):
        query = self.text_builder.get_query_for(self.STRING)
        expected = Query(self.STRING,self.STEMMED);
        self.assertTextsEqual(query, expected)
        
    def assertTextsEqual(self,actual,expected):
        '''
        depends on:
         - TestText()
        '''     
        self.assertEqual(type(actual), type(expected), 'Builder zwraca obiekty złego typu')
        self.assertEqual(actual.original,expected.original,'Bulider źle ustawia tekst orginalny')
        self.assertEqual(actual.stemmed,expected.stemmed, 'Builder źle ustawia tekst zestemmowany')
        
    def assertHasAttribute(self,attr_name,object,msg = None):
        if not msg:
            msg = "Obiekt: %s nie posiada arybutu o nazwie '%s'"%(object,attr_name)
        if not hasattr(object, attr_name):
            self.fail(msg)
        
if __name__ == '__main__':
    unittest.main()