# -*- coding: utf-8 -*-
"""
Created on Tue May 19 16:08:45 2020

@author: harsh
"""

import collections
import heapq

sigma = 2
itemSetSize = 3

dat_file = 'retail_25k.dat'

def  getTransaction(dat_file,itemSetSize):
    transactions = []
    A = open(dat_file,'r')
    for line in A.readlines():
        trans = [int(item) for item in line.split(" ")[:-1]]
        if len(trans) < itemSetSize:
            continue
        trans = set(trans) 
        if len(trans) < itemSetSize: 
            continue
        transactions.append(trans)
    return transactions

def cleanTransaction(transactions,sigma,itemSetSize):
    
    newTransactions = []
    counter = collections.defaultdict(int)
    for trans in transactions:
        if len(trans) < itemSetSize:
            continue
        
        newTransactions.append(trans)
        
        for item in trans:
            counter[item] += 1
        
    discard = [ key  for key,value in counter.items() if value < sigma]

    
    if not len(discard):
        return newTransactions

    del transactions
    transactions = []
    
    flag = False
    for trans in newTransactions:
        a = trans.difference(discard)
        if len(a) < itemSetSize:
            flag = True
            continue
        transactions.append(a)
    
    if flag:
        return cleanTransaction(transactions,sigma,itemSetSize)
    else:
        return transactions

transactions = getTransaction(dat_file,itemSetSize)
t = cleanTransaction(transactions,sigma,itemSetSize)   


counter = collections.defaultdict(int)


for m in t:
    for k in m:
        counter[k] += 1
        


h = [(value,key) for key,value in counter.items()]


h = sorted(h,reverse = True)



i = 0

item2code = {}
code2item = {}
for value,key in h:
    item2code[key] = i 
    code2item[i] = key
    i += 1


newTrans = []
for trans in t:
    print(trans)
    c = [item2code[item] for item in trans]
    newTrans.append(c)
    

    
# FPGrowth Constructions


class FPGrowth:
    def __init__(self):
        self.root = FPNode(None,-1)
        self.itemHeaderLastLink = {}
        self.itemHeaderFirstLink = {}
    
    def insert(self,trans):
        root = self.root        
        for item in sorted(trans):
            if item not in root.childrens:
                root.childrens[item] = FPNode(root,item)
                
                if item not in self.itemHeaderFirstLink:
                    self.itemHeaderFirstLink[item] = root.childrens[item]
                    self.itemHeaderLastLink[item] = root.childrens[item]
                else:
                    self.itemHeaderLastLink[item].nextLink = root.childrens[item]
                    self.itemHeaderLastLink[item] = self.itemHeaderLastLink[item].nextLink
            
            root.childrens[item].freq += 1
            root = root.childrens[item]

    def getConditionalPaths(self,item,minItemSetSize):
        node = self.itemHeaderFirstLink[item] 
        counter = collections.defaultdict(int)
        
        while node and node.item != -1:
            tempNode = node
            print(node.item,node.freq)
            freq = node.freq
            
            while tempNode and tempNode.item != -1:
                counter[tempNode.item] += freq
                tempNode = tempNode.parent
            node = node.nextLink
            
        paths = []
        pathsFreq  = []
        node = self.itemHeaderFirstLink[item] 
        while node and node.item != -1:
            tempNode = node
            freq = node.freq
            p = []
            while tempNode and tempNode.item != -1:
                if counter[tempNode.item] >= sigma:
                    p.append(tempNode)
                tempNode = tempNode.parent
            
            if len(p) >= minItemSetSize:
                paths.append(p)
                pathsFreq.append(freq)    
            node = node.nextLink
            
        return paths

    
        
        
class FPNode:
    def __init__(self,parent,item):
        self.parent = parent # parent is node
        self.childrens = {}
        self.item = item
        self.nextLink = None
        self.freq = 0
        
FPTree = FPGrowth()

for m in newTrans:
    FPTree.insert(m)
    

