#! /usr/bin/python
# -*- coding: utf-8 -*-
from gui_queue import Queued
import sys
import dialog
from seeker.text.vectorbuilder import stringify_array

__author__ = "andy"
__date__ = "$2010-10-09 14:29:49$"



try:
    import pygtk
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
    ENTRY_KEYWORD_EMPTY = 'Pole wyszukiwania jest puste.'
    MESSAGE_CHOOSE_BOTH_FILES = ('Ostrzeżenie', 'Źle wybrane pliki', 'Obydwa pliki muszą wybrane, aby mó załadować dane.')
    CONTEXT_FILE_LOADING = 1
    CONTEXT_IS_ON = 2
    CONTEXT_ENTRY_KEYWORDS = 3
    def __init__(self,text_manager,file_manager):
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
        self.input =  self.wTree.get_widget('entry_keywords')
        self.text_manager = text_manager
        self.file_manager = file_manager

        #Create our dictionay and connect it
        dic = {"on_main_window_destroy": gtk.main_quit,
            "on_btn_load_files_clicked": self.__btn_load_files_clicked,
            "on_btn_search_clicked":self.__execute_search,
            "on_mn_documents_activate":self.__show_stemmed_documents,
            "on_mn_keywords_activate":self.__show_stemmed_keywords,
            "on_caution_response" : self.caution.close}
        self.wTree.signal_autoconnect(dic)
    def test(self,widget):
        print 'raz'
    def __btn_load_files_clicked(self, widget):
        documents_filename = self.__get_filename_from_choser('chooser_documents')
        keywords_filename = self.__get_filename_from_choser('chooser_keywords')
        if all((documents_filename,keywords_filename)):         
            self.statusbar.push(self.CONTEXT_FILE_LOADING,self.FILES_LOADING)
            data = (self.file_manager.get_keywords_from(keywords_filename),
            self.file_manager.get_documents_from(documents_filename))
            self.text_manager.set_keywords(data[0])
            self.text_manager.set_documents(data[1])
            self.__enable_search_area()
            self.statusbar.pop(self.CONTEXT_FILE_LOADING)
        else:
            self.caution.show_dialog_with(*self.MESSAGE_CHOOSE_BOTH_FILES)
            
       
    def __get_filename_from_choser(self, chooser_name):
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
        widgets = ('entry_keywords','btn_search','menuitem1')
        for w in widgets:        
            w = self.wTree.get_widget(w)
            w.set_sensitive(True)
    def __execute_search(self,widget):
        self.statusbar.pop(self.CONTEXT_ENTRY_KEYWORDS)
        text = self.input.get_text().strip()
        if(text):
            self.text_manager.set_query(text)
            result = self.text_manager.get_similiarity_list()
            prepared = ['Podobieństwo: %f\nTytuł: %s\n'%(d.cosinus,d.title) for d in result]
            print '\n'.join(prepared)
            self.__show_text(prepared)  
        else:
            self.statusbar.push(self.CONTEXT_ENTRY_KEYWORDS, self.ENTRY_KEYWORD_EMPTY)
    def __show_text(self,tuple):
        self.buffer.set_text('\n'.join(tuple));
    
    def __show_stemmed_documents(self,widget):
        self.input.set_text('')
        self.__show_text([d.stemmed + '\n' for d in self.text_manager.documents])
     
    def __show_stemmed_keywords(self,widget):
        self.input.set_text('')
        self.__show_text(stringify_array(self.text_manager.keywords))
      

def run(text_manager,file_manager):
    '''
    Odpala GUI programu.
    Do działania potrzebuje klasy zarządzającej tekstami oraz klasy dekodującej zawartość plików  
    '''
    seeker = SeekerGUI(text_manager, file_manager) #@UnusedVariable
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
