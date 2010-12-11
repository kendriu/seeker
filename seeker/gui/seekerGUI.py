#! /usr/bin/python
# -*- coding: utf-8 -*-
from gui_queue import Queued
import sys
import dialog
import mode
from seeker.text.vectorbuilder import stringify_array

from seeker.text.query import *

__author__ = "andy"
__date__ = "$2010-10-09 14:29:49$"



try:
    import pygtk
    import gtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk.glade
except:
    sys.exit(1)

class SeekerGUI(Queued):
    """Obsluga  GUI"""
    
    RESET_FILES = 'Resetuj pliki'
    FILES_LOADING = 'Wczytuję i przygotowuję dane z plików. Proszę czekać...'
    ENTRY_KEYWORD_EMPTY = 'Pola wyszukiwania puste. Lub wypełnione niepoprawnie'
    MESSAGE_CHOOSE_BOTH_FILES = ('Ostrzeżenie', 'Źle wybrane pliki', 'Obydwa pliki muszą wybrane, aby mó załadować dane.')
    
    CONTEXT_FILE_LOADING = 1
    CONTEXT_IS_ON = 2
    CONTEXT_ENTRY_KEYWORDS = 3
    
    def __init__(self,file_manager):
        Queued.__init__(self)
        #Set the Glade file
        self.gladefile = "Seeker.glade"
        self.label_old = None
        self.wTree = gtk.glade.XML(self.gladefile)
        self.caution = dialog.Caution(self.wTree.get_widget('caution'))
        self.statusbar = self.wTree.get_widget('statusbar')
        window = self.wTree.get_widget('text_results')
        self.buffer = gtk.TextBuffer()
        window.set_buffer(self.buffer)
        self.file_manager = file_manager
        self.__set_mode_tfidf()

        #Create our dictionary and connect it
        dic = {"on_main_window_destroy": gtk.main_quit,
            "on_btn_load_files_clicked": self.__btn_load_files_clicked,
            "on_btn_search_clicked":self.__execute_search,
            "on_btn_execute_clicked":self.__execute_search,
            "on_mn_documents_activate":self.__show_stemmed_documents,
            "on_mn_keywords_activate":self.__show_stemmed_keywords,
            "on_mn_kmeans_activate": self.__set_mode_kmeans,
            "on_mn_tfidf_activate": self.__set_mode_tfidf,
            "on_caution_response" : self.caution.close}
        self.wTree.signal_autoconnect(dic)
        
    def __btn_load_files_clicked(self, widget):
        documents_filename = self.__get_filename_from_chooser('chooser_documents')
        keywords_filename = self.__get_filename_from_chooser('chooser_keywords')
        if all((documents_filename,keywords_filename)):         
            self.statusbar.push(self.CONTEXT_FILE_LOADING,self.FILES_LOADING)
            data = (self.file_manager.get_keywords_from(keywords_filename),
            self.file_manager.get_documents_from(documents_filename))
            self.mode.set_data(data)     
            self.__enable_search_area()
            self.statusbar.pop(self.CONTEXT_FILE_LOADING)
        else:
            self.caution.show_dialog_with(*self.MESSAGE_CHOOSE_BOTH_FILES)
            
       
    def __get_filename_from_chooser(self, chooser_name):
        '''
        Pobiera nazwę pliku z chooser'a
        '''
        chooser = self.wTree.get_widget(chooser_name)
        return chooser.get_filename()
        

    def __trigger_load_files_label(self, widget):
        if self.label_old == None:
            self.label_old = widget.get_label()
            widget.set_label(self.RESET_FILES)
            print self.label_old
        else:
            widget.set_label(self.label_old)
            self.label_old = None
            print self.RESET_FILES
    
    def __enable_search_area(self):
        widgets = ('entry_keywords','btn_search','menuitem1','btn_execute','entry_seed','entry_max_repeats')
        for w in widgets:        
            w = self.wTree.get_widget(w)
            w.set_sensitive(True)
            
    def __execute_search(self,widget):
        self.statusbar.pop(self.CONTEXT_ENTRY_KEYWORDS)
        
        success = self.mode.execute_search()
        if(success):
            prepared = self.mode.get_prepared()
            self.__show_text(prepared) 
            self.__show_extenions() 
        else:
            self.statusbar.push(self.CONTEXT_ENTRY_KEYWORDS, self.ENTRY_KEYWORD_EMPTY)
    
    def __show_extenions(self):
        input =  self.wTree.get_widget('entry_keywords')
        
        w = self.wTree.get_widget("query_ext_box")
        w.foreach(w.remove)

        docs = self.mode.text_manager.documents
        keys = self.mode.text_manager.keywords
        extensions = QueryExtensions(docs, keys, self.mode.text_manager)
        
        ext_query = [input.get_text().strip()]
        def on_toggled(widget, data):
            if widget.get_active():
                ext_query.append(data[0].stemmed)
            else:
                ext_query.remove(data[0].stemmed)

            input.set_text(" ".join(ext_query))

        for k, ex in extensions.get_extensions_for_query(input.get_text()).items():
            for e in ex:
                window = gtk.CheckButton(e[0].original)
                w.add(window)
                window.connect('toggled', on_toggled, e) 
                
        w.foreach(lambda x: x.show())

    def __show_text(self,tuple):
        self.buffer.set_text('\n'.join(tuple));
    
    def __show_stemmed_documents(self,widget):
        self.__show_text([d.stemmed + '\n' for d in self.mode.text_manager.documents])
     
    def __show_stemmed_keywords(self,widget):
        self.__show_text(stringify_array(self.mode.text_manager.keywords))
    
    def __set_mode_kmeans(self,widget=None):
        print 'zmieniam tryb na kmeans' 
        self.mode = mode.Kmeans(self.wTree)
    
    def __set_mode_tfidf(self,widget=None):
        print 'zmieniam tryb na tfidf'
        self.mode = mode.Tfidf(self.wTree)
        
        

def run(file_manager):
    '''
    Odpala GUI programu.
    Do działania potrzebuje klasy zarządzającej tekstami oraz klasy dekodującej zawartość plików  
    '''
    seeker = SeekerGUI(file_manager) #@UnusedVariable
    try:
        gtk.threads_init()
    except:
        print "W trakcie kompilacji nie była włączona obsługa wątków pyGTK!"
        import sys #@Reimport
        sys.exit(1)
    
    gtk.threads_enter()   
    gtk.main()
    gtk.threads_leave()
    
if __name__ == "__main__":
    print "you are in seekerGUI.py"
