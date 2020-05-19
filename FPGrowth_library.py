# -*- coding: utf-8 -*-
"""
Created on Tue May 19 04:33:46 2020

@author: harsh
"""
import pyfpgrowth

transactions = [[1, 2, 5],
                [2, 4],
                [2, 3],
                [1, 2, 4],
                [1, 3],
                [2, 3],
                [1, 3],
                [1, 2, 3, 5],
                [1, 2, 3]]

patterns = pyfpgrowth.find_frequent_patterns(transactions, 2)

for key in patterns.keys():
    if len(key) > 2:
        print(key)
        