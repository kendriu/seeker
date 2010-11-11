#!/usr/bin/env python
# -*- coding: utf-8 -*-

from text import *
__all__ = ('Query',)
class Query (Text):

    """
     Zapytanie z wyszukiwarki

    :version:
    :author:Andrzej Skupień
    """
    
    def __init__(self,original,stemmed):
        Text.__init__(self, original, stemmed)
        self.documents = []

    def add_document(self, document):
        """
         dodaje dokument do zapytania. Uwaga: żeby użyć tej funkcji, do obiektu klasy Query
         należy najpierw ustawić wektor TFIDF dla documentu i zapytania 
         (query.vector = Vector(),document.vector = Vector())
        @raise AttributeError: wtedy kiedy nie został ustawiony wektor TFIDF dla dokumentu lub vectora
        @param Oriented document: dokument ,do którego trzeba porównać zapytanie
        @return bool :
        @author Andrzej Skupień
        """
        
        document.cosinus = self.vector.count_cosinus_to(document.vector)
        self.documents.append(document);

    def get_similiarity_list(self):
        """
         zwraca listę dokumentów posortowaną według podobieństwa do zapytania. Każdy
         dokument z listy ma nadany atrybut 'cosinus', przechowujący cosinus
         kąta tworzenego przez wektor TFIDF dokumenu i zapytania. 
        
        @return touple :
        @author Andrzej Skupień
        """
        self.documents.sort(key=lambda document: document.cosinus, reverse=True)
        return self.documents
        
            
    

import unittest
from vector import *

class TestQuery(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.query = Query('original','stemmed');
        self.query.vector = Vector((0.0, 0.0, 1.0))
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def test_add_document(self):
        mocks = [self.__get_simple_Mock(),
                 self.__get_simple_Mock()]
        self.assertEqual([], self.query.documents)
        self.query.add_document(mocks[0])
        self.assertEqual([mocks[0]], self.query.documents)
        self.query.add_document(mocks[1])
        self.assertEqual(mocks, self.query.documents)
    def __get_simple_Mock(self):
        mock = Mock()
        mock.vector = Vector((0.0, 0.0, 0.0))
        return mock
    
    def test_add_document_raises_AtrributeError(self):
        mock = self.__get_simple_Mock()
        self.failUnlessRaises(AttributeError, self.query.add_document, (mock,))
    
    def test_get_similiarity_list(self):     
        test_vectors = ((9.0, 1.0, 6.0),
                        (1.0, 2.0, 3.0),
                        (0.0, 0.0, 0.0),
                        (2.0, 2.0, 2.0),
                        )
        cosinuses = (0.80178372573727319, 0.57735026918962584, 0.55234477073899402, 0.0)
        mocks = []
        for i, x in enumerate(test_vectors):
            mock = Mock()
            mock.vector = Vector(x)
            mock.cosinus = cosinuses[i]
            self.query.add_document(mock)
            mocks.append(mock)
        mocks.sort(key=lambda mock: mock.cosinus, reverse=True)
        self.assertEqual(mocks,self.query.get_similiarity_list())

class Mock():  
    pass  
        
if __name__ == '__main__':
    unittest.main()
