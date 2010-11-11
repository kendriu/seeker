#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Moduł obsługujący wyskakujące okienko

'''
__author__ = 'andy'
__date__ = 2010 - 10 - 24

class Caution():
    def __init__(self, widget):
        self.widget = widget
    
    def show_dialog_with(self, title, text, secondary_text):
        self.widget.set_title(title)
        self.widget.set_property('text',text)
        self.widget.set_property('secondary-text', secondary_text)
        self.widget.show()
        
    def close(self,widget,response):
        widget.hide()
        
        
        
