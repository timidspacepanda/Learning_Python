#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 22:06:23 2025

@author: kpetchsaiprasert
"""

# Singleton using a metaclass
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # If instance doesn't exist, create one
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
# Example singleton class
class SingletonClass(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value
        
    def show_value(self):
        print(f"Singleton value: {self.value}")
            
# Usage
a = SingletonClass(10)
b = SingletonClass(20)

a.show_value() # Output: Singleton value: 10
b.show_value() # Output: Singleton value: 10
            
        