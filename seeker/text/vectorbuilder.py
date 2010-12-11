#!/usr/bin/env python
# -*- coding: utf-8 -*-
from text import *
from tfidf import *
from vector import *
import porterstemmer
import textbuilder
import unittest

__all__ = ('Vector_Builder','stringify_array')
class Vector_Builder(object):

    """
     Budowniczy wektorów. Przed stworzeniem wektora, należy podać

    :version:
    :author:Andrzej Skupień
    """

    def __init__(self, keywords, documents):
        """
        @param tuple keywords : krotka ustawiająca kolejność składowych dla tworzonych wektorów TF-IDF
        @param tuple documents : Dokumenty dla których liczony jest TF-IDF
        @return  :
        @author Andrzej Skupień
        """
        self.keywords = stringify_array(keywords)
        self.documents = stringify_array(documents)

    def get_vector_for(self, text):
        """
         zwraca wekorTF-IDF dla podanego tekstu

        @param Text text : tekst dla którego trzeba wyliczyć wektor TF-IDF
        @return tuple :
        @author Andrzej Skupień
        """
        vector = []
        keywords = self.keywords
        for word in keywords:
            try:
                tfidf_value = tfidf(str(word), str(text), self.documents)
            except ZeroDivisionError:
                tfidf_value = 0
            vector.append(tfidf_value)
        return Vector(vector)
            
    def get_freq_vector_for(self, text):
        """
		Zwraca wektor częstości wystapień każdego keyworda w tekscie.
        
        @param text: tekst dla którego trzeba wyliczyć wektor
        @return: Vectorfreq
        @uthor: Tomasz Sobkowiak
        """
        vector = []
        for word in self.keywords:
            try:
                f = freq(word, text)
            except ZeroDivisionError:
                f = 0
            vector.append(f)
        return Vector(vector)
        
def stringify_array(array):
    '''
    Na każdym z elementów wywoływana jest funkcja str(x).
    @param tuple array: 
    @return list: lista elementów. Na każdym elemencie został wywołana funkcja str(x)
    '''
    return [str(x) for x in array]

class Test_Vector_Builder(unittest.TestCase):
    '''depends:
        Test_Text_Builer
     '''
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.text_builder = textbuilder.Text_Builder(porterstemmer.PorterStemmer())
        self.keywords = self.__get_keywords()
        self.documents = self.__get_documents()
        self.vector_builder = Vector_Builder(self.keywords, self.documents)
    def __get_keywords(self):
        keywords = ('string', 'element', 'word')
        return [self.text_builder.get_keyword_for(x) for x in keywords]
    
    def __get_documents(self):
        documents = ('Text about string.\nThis text is only about string',
                     'Text about elements and words.\nThis text is about elements and words',
                     'Text about evrything.\n This text is about: elements,words and strings',
                     'Nothing.\n This text is not important')
        return [self.text_builder.get_document_for(x) for x in documents]
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def test__init__(self):
        self.assertEqual(stringify_array(self.keywords), self.vector_builder.keywords)
        self.assertEqual(stringify_array(self.documents), self.vector_builder.documents)
    
    def test_get_vector_for(self):
        documents = stringify_array(self.__get_documents())
        
        expected = ((0.15403270679109896, 0.0, 0.0),
                 (0.0, 0.11552453009332421, 0.11552453009332421),
                 (0.063013380050904122, 0.063013380050904122, 0.063013380050904122),
                 (0.0, 0.0, 0.0))        
        for i,doc in enumerate(documents):
            vector = self.vector_builder.get_vector_for(doc)
            self.assertEqual(expected[i],vector.tuple,'Vector_builder źle tworzy wektory dla tekstów')
    def test_Non_UTF_Characters(self):
        docs = ('''GMU Machine Learning and Inference Laboratory
... 2002 Copyright 2002-2003 Machine Learning and Inference Laboratory
Front page created by Guido Cervone and Janejira Kalsmith. ... 
Description: Research on Theories of Learning, Inference, and Discovery Data Mining and Knowledge Discovery, User...
''','''Yahoo! Groups : machine-learning
machine-learning Machine Learning, [ Join This Group! ]. Home, Messages, Links,
Members Only, Chat, ... Machine Learning mailing list: machine-learning@egroups.com. ... 
Description: An unmoderated mailing list intended for people in computer sciences, statistics, mathematics, and...
        ''' )
        
        x =  [tfidf('', doc, docs) for doc in docs]
        print x
        
        
if __name__ == '__main__':
    unittest.main()


