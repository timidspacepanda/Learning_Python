#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 17:04:41 2025

@author: kpetchsaiprasert
"""

# Step 1: Define different strategies
class AdditionStrategy:
    def execute(self, a, b):
        return a + b

class MultiplicationStrategy:
    def execute(self, a, b):
        return a * b

# Step 2: Context class that uses a strategy
class Calculator:
    def __init__(self, strategy):
        self._strategy = strategy
        
    def set_strategy(self, strategy):
        self._strategy = strategy
        
    def caclulate(self, a, b):
        return self._strategy.execute(a, b)
    
# Step 3: Use the strategies
if __name__ == "__main__":
    add_strategy = AdditionStrategy()
    mult_strategy = MultiplicationStrategy()
    
    calc = Calculator(add_strategy)
    print(calc.caclulate(5, 3))
    
    calc.set_strategy(mult_strategy)
    print(calc.caclulate(5, 3))