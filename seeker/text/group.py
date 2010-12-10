#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Group:
    
    def __init__(self,medoid):
        self.medoid = medoid
        self.documents = []
        self.previous_documents = []
    
    def has_changed(self):
        return not self.documents == self.previous_documents
    
    def reset(self):
        self.previous_documents = self.documents
        self.documents = []
        
    def select_new_medoid(self):
        for doc in self.documents:
            doc.summed_cosinus_to_others = 0
            for doc2 in self.documents:
                if doc == doc2:
                    continue
                doc.summed_cosinus_to_others += doc.vector.count_cosinus_to(doc2.vector)
                


        self.medoid = max(self.documents,key=lambda document: document.summed_cosinus_to_others)
        
