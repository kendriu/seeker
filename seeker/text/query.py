#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy

from text import *
from seeker import utils
from operator import itemgetter

__all__ = ('Query', 'QueryExtensions')
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
        
class QueryExtensions:
    
    def __init__(self, documents, keywords, text_manager):
        self.documents = documents
        self.keywords = keywords
        self.text_builder = text_manager.text_builder

        self.matrix = self.__create_assoc_matrix(self.documents)

    def __create_assoc_matrix(self, documents):
        m = [list(d.freq_vector) for d in self.documents]        
        assoc_matrix = numpy.transpose(numpy.matrix(m))
        assoc_matrix = assoc_matrix * numpy.transpose(assoc_matrix)        
        return utils.MatrixProxy(assoc_matrix)
    
    def get_keyword_index(self, keyword):
        key = keyword.stemmed

        def getter(k):
            return k.stemmed

        try:
            return map(getter, self.keywords).index(key)
        except ValueError:
            return -1;

    def remove_duplicated_entries(self, seq):

        def stemmed_getter(x):
            return x[0].stemmed

        return utils.unique(seq, idfun=stemmed_getter)

    def get_extension_for_keyword(self, word): 
        key = self.text_builder.get_keyword_for(word)
        word_index = self.get_keyword_index(key)

        if word_index < 0:
            return []

        sorted_indexes = self.matrix.sorted_nonzero_indexes(word_index)
        word_assoc_vector = self.matrix.get_word_vector(word_index)
        extensions = [(self.keywords[x], word_assoc_vector[x]) for x in sorted_indexes]
        unique = self.remove_duplicated_entries(extensions)
       
        unique.sort(key=itemgetter(1), reverse=True)
        return unique

    def get_extensions_for_query(self, q):
        words = q.split(" ")
        extensions = {}        
        count = int(4 / len(words) + 0.5)
        for word in words:
            extensions[word] = self.get_extension_for_keyword(word)[1:count+1] 
        return extensions
    

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
