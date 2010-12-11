#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2010-11-04

@author: Andrzej Skupień
'''
from porterstemmer import *
from textbuilder import *
from vectorbuilder import *
from group import *
import random
from seeker.text.vectorbuilder import stringify_array

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
    
    def set_keywords(self, keywords):
        words = []
        for word in keywords:
            words.append(self.text_builder.get_keyword_for(word))
        self.keywords = tuple(words)
        
    def set_documents(self, documents):
        docs = []
        for doc in documents:
            docs.append(self._document_function(doc))
        self.documents = tuple(docs)
        self.vector_builder = Vector_Builder(self.keywords, self.documents)
        self._assign_vectors_to_documents()
   
    def _assign_vectors_to_documents(self):
        docs = self.documents
        for i, doc in enumerate(docs):
            print 'signing vector'
            self.documents[i].vector = self.vector_builder.get_vector_for(doc)
            self.documents[i].freq_vector = self.vector_builder.get_freq_vector_for(doc)
        print 'done with vectors'
        
    
    
class Tfidf(Manager):
    def __init__(self):
        Manager.__init__(self)
        self._document_function = self.text_builder.get_document_for
    def set_query(self, query):
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
    
    def set_seed(self, seed):
        value = int(seed)
        if (value <= 0):
            raise ValueError('Właściwość %s pownna być dodatnia. Podano "%s"' % (property, seed))
        self.seed = value
        
    def set_max_repeats(self, max_repeats):
        value = int(max_repeats)
        if (value <= 0):
            raise ValueError('Właściwość %s pownna być dodatnia. Podano "%s"' % (property, max_repeats))
        self.max_repeats = value
         
    def __set_positive_property(self, property, value):
        value = int(value)
        if (value <= 0):
            raise ValueError('Właściwość %s pownna być dodatnia. Podano "%s"' % (property, value))
        property = value
    def get_list(self):
        
        groups = [Group(doc) for doc in random.sample(self.documents, self.seed)]
# wyciąganie wartości unikatowych
#        unique_groups = []
#        unique_groups_categories = []
#        for group in groups:
#            if group.medoid.category not in unique_groups_categories:
#                unique_groups_categories.append(group.medoid.category)
#                unique_groups.append(group)
#        groups = unique_groups
       
        i = 0
        while True:
            print '\nIteracja: %i ' % (i + 1,)
            for group in groups:
                group.reset()
            for doc in self.documents:
                best_group = groups[0]
                for group in groups[1:]:
                    if group.medoid.vector.count_cosinus_to(doc.vector) > best_group.medoid.vector.count_cosinus_to(doc.vector):
                        best_group = group
                best_group.documents.append(doc)
            no_changes = True
            for group in groups:
                if(group.has_changed()):
                    format = 'Nastąpiła zmiana w grupie: %s'
                    no_changes = False
                    group.select_new_medoid()
                else:
                    format = 'Brak zmian w grupie: %s'
                print  format % (group.medoid.category,)
                                                    
            i += 1
            if i == self.max_repeats or no_changes:
                break
        groups.sort(key=lambda group: group.medoid.category)
        return groups
