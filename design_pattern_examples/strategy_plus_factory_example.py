#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 21:07:43 2025

@author: kpetchsaiprasert
"""

from typing import List, Callable

# --- Strategy function ---
def bubble_sort(data: List[int]) -> List[int]:
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        for j in range(n - i -1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j +1] = arr[j + 1], arr[j]
    return arr

def quick_sort(data: List[int]) -> List[int]:
    if len(data) <= 1:
        return data
    pivot = data[0]
    left = [x for x in data[1:] if x <= pivot]
    right = [x for x in data[1:] if x > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)

def reverse_sort(data: List[int]) -> List[int]:
    return sorted(data, reverse=True)

# --- Factory ---
class SortFactory:
    strategies = {
        "bubble": bubble_sort,
        "quick": quick_sort,
        "reverse": reverse_sort
        }
    
    @staticmethod
    def get_strategy(name: str) -> Callable[[List[int]], List[int]]:
        if name not in SortFactory.strategies:
            raise ValueError(f"Unknown sort strategy: {name}")
        return SortFactory.strategies[name]
   
# --- Context ---
class Sorter:
    def __init__(self, strategy: Callable[[List[int]], List[int]]):
        self.strategy = strategy
    
    def sort(self, data: List[int]) -> List[int]:
        return self.strategy(data)
    
        
    # --- Client code ---
if __name__ == "__main__":
    data = [5, 3, 8, 1 ,4]
    
    # Choose strategy via Factory
    strategy = SortFactory.get_strategy("quick")
    sorter = Sorter(strategy)
    print("Quick sort:", sorter.sort(data))
    
    strategy = SortFactory.get_strategy("bubble")
    sorter = Sorter(strategy)
    print("Bubble sort:", sorter.sort(data))
    
    strategy = SortFactory.get_strategy("reverse")
    sorter = Sorter(strategy)
    print("Reverse sort:", sorter.sort(data))