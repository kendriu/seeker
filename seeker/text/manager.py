#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2010-11-04

@author: Andrzej Skupień
'''
from porterstemmer import *
from textbuilder import *
from vectorbuilder import *

class Manager():
    '''
        Klasa osłonowa dla pakietu text. 
        Z całego pakietu tylko ona powinna byc używana.
        Sposób i kolejonść użycia:
        1. Podajemy słowa kluczowe - set_keywords(keywords)
        2. Podajemy dokumenty za pomocą  - set_documents(documents)
        3. gdy przyjdzie zapytanie. ustawiamy je za pomoca komendy set_query(query)
        4. lista wynikowa pobierana jest przy pomocy polecenia get_list.
        
        
    '''


    def __init__(self):
        stemmer = PorterStemmer()
        self.text_builder = Text_Builder(stemmer)
        self._document_function = None
    
    def set_keywords(self,keywords):
        words = []
        for word in keywords:
            words.append(self.text_builder.get_keyword_for(word))
        self.keywords = tuple(words)
        
    def set_documents(self,documents):
        docs = []
        for doc in documents:
            docs.append(self._document_function(doc))
        self.documents = tuple(docs)
        self.vector_builder = Vector_Builder(self.keywords, self.documents)
        self._assign_vectors_to_documents()
   
    def _assign_vectors_to_documents(self):
        docs = self.documents
        for i,doc in enumerate(docs):
            print 'signing vector'
            self.documents[i].vector = self.vector_builder.get_vector_for(doc)
        print 'done with vectors'
        
    
    
class Tfidf(Manager):
    def __init__(self):
        Manager.__init__(self)
        self._document_function = self.text_builder.get_document_for
    def set_query(self,query):
        query = self.text_builder.get_query_for(query)
        query.vector = self.vector_builder.get_vector_for(query)
        self.query = query
    
    def get_list(self):
        query = self.query
        if query:
            for d in self.documents:
                query.add_document(d)
            return query.get_similiarity_list()
        else:
            return ''


class Kmeans(Manager):
    def __init__(self):     
        Manager.__init__(self)
        self._document_function = self.text_builder.get_categorized_document_for