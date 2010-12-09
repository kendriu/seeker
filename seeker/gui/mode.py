#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Moduł opisuje tryby działania aplikacji
Dostępne tryby:
 - TFIDF
 - KMEANS

'''
__author__ = 'andy'
__date__ = 2010 - 11 - 27

class Base:
    def __init__(self, wTree):
        self.wTree = wTree
        self.hbox_kmeans = wTree.get_widget('hbox_kmeans')
        self.hbox_tfidf = wTree.get_widget('hbox_tfidf')
        
    def _set_visibility_to_hbox(self,tfidf,kmeans):       
        self.hbox_tfidf.set_visible(tfidf)        
        self.hbox_kmeans.set_visible(kmeans)
          
class Tfidf(Base):
    def __init__(self, wTree, text_manager):
        Base.__init__(self, wTree)
        self._set_visibility_to_hbox(True, False)
        self.text_manager = text_manager
        self.input =  self.wTree.get_widget('entry_keywords')
    
    def execute_search(self): 
        text = self.input.get_text().strip()
        if(text):
            self.text_manager.set_query(text)
            result = self.text_manager.get_list()
            self.prepared = ['Podobieństwo: %f\nTytuł: %s\n' % (d.cosinus, d.title) for d in result]
            return True
        else:
            return False
        
    def get_prepared(self):
        return self.prepared
        

class Kmeans(Base):
    
    def __init__(self, wTree):
        Base.__init__(self, wTree)
        self._set_visibility_to_hbox(False, True)
        self.input_seed = self.wTree.get_widget('entry_seed')
        self.input_max_repeats = self.wTree.get_widget('entry_max_repeats')
        
    def execute_search(self, text):
        seed = self.input_seed.get_text().strip()
        max_repeats = self.input_max_repeats().get_text().strip()
        return self.__try_prepare(seed, max_repeats)
    
    def __try_prepare(self,seed,max_repeats):
        try:
            self.__prepare(int(seed), int(max_repeats))
        except ValueError:
            return False
        return True
    
    def __prepare(self,seed,max_repeats):
        pass
