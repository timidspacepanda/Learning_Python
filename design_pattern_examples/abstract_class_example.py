#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 17:14:16 2025

@author: kpetchsaiprasert
"""
from abc import ABC, abstractmethod

# Abstract class
class Animal(ABC):
    @abstractmethod
    def make_sound(self): # Abstract method (no implementation)
        pass
    
    def sleep(self): # Regular method (has implementation)
        print("Sleeping...")
        
# Concrete subclass
class Dog(Animal):
    def make_sound(self): # Must implement abstract method
        print("Bark!")
        
class Cat(Animal):
    def make_sound(self):
        print("Meow!")
        
# Usage
dog = Dog()
dog.make_sound()
dog.sleep()