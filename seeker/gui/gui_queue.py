#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
gui_queue.py
Ten moduł wykonuje zadania, które pozwalają uniknąć problemów z wątkami w systemach Linux i Windows
Inne moduły mogą go stosować bez żadnej dodatkowej wiedzy na temat gtk.
'''

#Kod udostępniony na licencji Python License dla książki Python

import gtk
import random
import socket
from threading import RLock
#import timeoutsocket #używane dla set_timeout()

class gui_queue:
    '''
    Budzi wątek GUI, który czyści wykonuje zadania z kolejki
    '''
    def __init__(self, gui, listenport=0):
        '''Jeśli listenport jest równe 0, tworzy losowy por do nasłuchiwania'''
        self.mylock = RLock()
        self.myqueue = []
        if listenport == 0:
            self.listenport = random.randint(1025, 10000)
        else:
            self.listenport = listenport
        print "Lokalna kolejka GUI nasłuchuje na porcie %s" % self.listenport
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", self.listenport))
        self.listensocket = s
        self.listensocket.listen(300) # nasłuchiwanie aktywności
        self.gui = gui
        return
    
    def append(self, command, args):
        '''Metodę tą może wykonać dowolny wątek'''
        self.mylock.acquire()
        self.myqueue.append((command, args))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.01)
        try:
            s = s.connect(("localhost", self.listenport))
        except:
            pass
        self.mylock.release()
        return
    
    def clearqueue(self, socket, x):
        '''
        Metoda wywyoływana tylko przez główny wątek GUI .
        Pamiętaj o zwracaniu wartości 1.
        '''
        self.listensocket.accept()
        for i in self.myqueue:
            (command,args) = i
            self.gui.handle_gui_queue(command,args)
        self.myqueue = []
        return 1
        
        
class Queued:
    
    def __init__(self):
        self.gui_queue = gui_queue(self)
        import gobject
        gobject.io_add_watch(self.gui_queue.listensocket, gobject.IO_IN,self.gui_queue.clearqueue)
        
    def handle_gui_queue(self,command,args):
        '''
        Wywołanie zwrotne używane przez gui_queue, gdy otrzyma od nas polecenie.
        Polecenie (commnand) jest ciągiem znaków.
        Parametr args zawiera listę argumentów polecenia
        '''
        gtk.threads_enter()
        method = getattr(self, command, None)
        if method:
            apply(method,args)
        else:
            print "Nierozpoznana akcja %s: %s"%(command, args)
        gtk.threads_leave()
        return 1
        
    def gui_queue_append(self,command, args):
        self.gui_queue.append(command, args)
        return 1
    
if __name__ == "__main__":
    print "Hello world"



