#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 22:18:23 2025

@author: kpetchsaiprasert
"""

# Step 1: Define some product classes
class Dog:
    def speak(self):
        return "Woof!"
    
class Cat: 
    def speak(self):
        return "Meow!"

# Step 2: Create a Factory to generate objects
class AnimalFactory:
    @staticmethod 
    def create_animal(animal_type: str):
        if animal_type.lower() == "dog":
            return Dog()
        elif animal_type.lower() == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")
            
# Step 3: Use the factory
if __name__ == "__main__":
    factory = AnimalFactory()
    
    dog = factory.create_animal("dog")
    cat = factory.create_animal("cat")
    
    print(dog.speak()) # Output: Woof!
    print(cat.speak()) # Output: Meow!