#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Moduł opisuje tyby działania aplikacji
Dostępne tryby:
 - TFIDF
 - KMEANS

'''
__author__ = 'andy'
__date__ = 2010 - 11 - 27

class Base:
    def __init__(self, wTree):
        self.hbox_kmeans = wTree.get_widget('hbox_kmeans')
        self.hbox_tfidf = wTree.get_widget('hbox_tfidf')
        pass
    def _set_visibility_to_hbox(self,tfidf,kmeans):       
        self.hbox_tfidf.set_visible(tfidf)        
        self.hbox_kmeans.set_visible(kmeans)
        
class Tfidf(Base):
    def __init__(self, wTree, text_manager):
        Base.__init__(self, wTree)
        self._set_visibility_to_hbox(True, False)
	self.text_manager = text_manager
    
    def execute_search(self, text):
        
        self.text_manager.set_query(text)
        result = self.text_manager.get_list()
        prepared = ['Podobieństwo: %f\nTytuł: %s\n' % (d.cosinus, d.title) for d in result]
        return prepared

class Kmeans(Base):
    
    def __init__(self, wTree):
        Base.__init__(self, wTree)
        self._set_visibility_to_hbox(False, True)
    def execute_search(self, text):
        pass
