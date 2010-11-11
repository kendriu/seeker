#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

__all__ = ('Vector',)
class Vector(object):
    """
     Wektor TF-IDF. Kolejne składowe wektora są miarami TF-IDF dla odpowiednich słów
     kluczowych (obiektów klasy Keyword). Wektory powinny być budowane wyłącznie za
     pomocą klasy Vector_Builder.

    :version:
    :author:Andrzej Skupień
    """
    def __init__(self, vector):
        '''
        @param tuple vector: kolejne wartości odpowiadają składowym wektora TF-IDF
        '''
        self.tuple = tuple(vector)

    def count_cosinus_to(self, vector):
        """
         funkcja licząca cosinus kąta stworzonym z drugim wektorem.
         Ilość składowych obydwu wektorów musi być równa

        @param Vector vector: drugi wektor. 
        @return float : cosinus kąta. W przypadku gdy długośc eukliesowa ktoregoś wektora jest równa zero
        funkcja również zwróci zero
        @author Andrzej Skupień
        """
        denominator = self.euclid_length()*vector.euclid_length()
        if denominator:
            return self.dot_product_for(vector) / denominator
        else:
            return 0.0
        
    
    def euclid_length(self):
        """
        zwraca euklidesową długość wektora
        @return float: euklidesową długośc wektora
        """
        return math.sqrt(sum((math.pow(x, 2) for x in self.tuple)))
    
    
    def dot_product_for(self, vector):
        """
        zwraca iloczyn skalarny dla tego i podanego w argumencie wektora.
        Ilość składowych obydwu wektorów musi być równa
        @raise ValueError: Jeżeli długość wektora wejściowego jest różna od tego wektora
        @return float: drugi wektor
        """
        if len(vector) != len(self):
            raise ValueError("Podany 'vector' jest nieprawidłowej długości")
        dot_product = 0
        for index,value in enumerate(self.tuple):
            dot_product += value * vector.tuple[index]
        return dot_product

    
    def __len__(self):
        """
        zwraca ilość składowych wektora
        @return integer:
        """
        return len(self.tuple)

import unittest

class TestVector(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.TUPLE = (1, 2, 3)
        self.vector = Vector(self.TUPLE)
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def test__init__(self):
        self.assertEqual(self.TUPLE, self.vector.tuple, 'źle przepisany wektor')   
        
    def test__len__(self):
        self.assertEqual(len(self.TUPLE), len(self.vector), 'Wektor źle podaje swoją długość')
    def test_euclid_length(self):           
        length = math.sqrt(1 * 1 + 2 * 2 + 3 * 3)
        self.assertEqual(length, self.vector.euclid_length(), 'wektor źle oblicza długośc euklidesową') 
   
    def test_dot_product_for(self): 
        second_vector = Vector((4,5,6))
        dot_product = (1 * 4 + 2 * 5 + 3 * 6)
        self.assertEqual(dot_product,
                          self.vector.dot_product_for(second_vector),
                          'Wektor źle liczy cosinusowe podobieństwo wektorów')
        
    def test_cosinus_for(self):
        second_vector = Vector((4,5,6))
        cosinus = (1 * 4 + 2 * 5 + 3 * 6)/(math.sqrt(1*1+2*2+3*3)*math.sqrt(4*4+5*5+6*6))
        self.assertEqual(cosinus, self.vector.count_cosinus_to(second_vector),'Wektor źle liczy podobieństwo')
    def test_dot_product_for_raises_ValueException_when_shorter(self):
        self.failUnlessRaises(ValueError, self.vector.dot_product_for, (Vector((1, 2)),))
    def test_dot_product_for_raises_ValueException_when_longer(self):
        self.failUnlessRaises(ValueError, self.vector.dot_product_for, (Vector((1, 2, 3, 4)),))
    def test_dot_product_for_not_raises_ValueException(self):
        
        try:
            self.vector.dot_product_for(Vector((4,5,6)))
        except ValueError:
            self.assertFalse('Funkcja rzuciła nieprawdłowo wyjątek ValueError')
if __name__ == '__main__':
    unittest.main()


