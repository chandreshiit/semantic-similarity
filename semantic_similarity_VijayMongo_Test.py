#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 16:56:16 2018

@author: chandresh
"""
from pywsd import disambiguate
from pywsd.similarity import max_similarity as maxsim
from nltk.corpus import  wordnet as wn
from nltk.tokenize import word_tokenize
import numpy as np
from collections import defaultdict
# initiaalize constaants
alpha = 0.2
beta  = 0.45
benchmark_similarity = 0.8025
gamma = 1.8

"""
Semantic similarity based on the paper:
    Calculating the similarity between words and sentences using a lexical database and corpus statistics
TKDE, 2018
"""
          
def _synset_similarity(s1,s2):
    L1 =dict()
    L2 =defaultdict(list)
       
    for syn1 in s1:
        L1[syn1[0]] =list()
        for syn2 in s2:                                     
            
            subsumer = wn.synset(syn1[1].name()).lowest_common_hypernyms(wn.synset(syn2[1].name()), simulate_root=True)[0]
            h =subsumer.max_depth() + 1 # as done on NLTK wordnet        
            syn1_dist_subsumer = wn.synset(syn1[1].name()).shortest_path_distance(subsumer,simulate_root =True)
            syn2_dist_subsumer = wn.synset(syn2[1].name()).shortest_path_distance(subsumer,simulate_root =True)
            l  =syn1_dist_subsumer + syn2_dist_subsumer
            f1 = np.exp(-alpha*l)
            a  = np.exp(beta*h)
            b  = np.exp(-beta*h)
            f2 = (a-b) /(a+b)
            sim = f1*f2
            L1[syn1[0]].append(sim)          
            L2[syn2[0]].append(sim)
    return L1, L2       
    
def getSimilarity(s1,s2, word_order = False):
    
    try:
        s1_wsd = disambiguate(s1) # using default disambiguation
        s2_wsd = disambiguate(s2)
    except TypeError:
        print("s2:",s1)
        sys.exit(0)
    # remove None synsets
    s1_wsd = [syn  for syn in s1_wsd if syn[1]]
    s2_wsd = [syn  for syn in s2_wsd if syn[1]]
    
    #vector_length = max(len(s1_wsd), len(s2_wsd))
    try:
        L1,L2 = _synset_similarity(s1_wsd,s2_wsd)
        V1 =np.array( [max(L1[key]) for key in L1.keys()])
        V2 = np.array([max(L2[key]) for key in L2.keys()])
        S  = np.linalg.norm(V1)*np.linalg.norm(V2)
        C1 = sum(V1>=benchmark_similarity)
        C2 = sum(V2>=benchmark_similarity)
    
        Xi = (C1+C2) / gamma
    
        if C1+C2 == 0:
            Xi = max(V1.size, V2.size) / 2.0
            
        sem_similarity = S/Xi    
    except ValueError:
        sem_similarity = 0
    # computing word order similarity
    word_ord_similarity = 0
    delta = 1.0
    if word_order:
        tokens1 = word_tokenize(s1)
        tokens2 = word_tokenize(s2)
        len1 = len(tokens1)
        len2 = len(tokens2)
    
        maxlen = len1
        if maxlen< len2:
            maxlen = len2
        r1 =list(range(maxlen))
        r2 =[0 for _ in range(maxlen)]
        if maxlen == len1:
            for i, v in enumerate(tokens2):
                if v in tokens1:
                    r2[i]=tokens1.index(v)+1
                else:
                    r2[i]= i
        else:
            for i, v in enumerate(tokens1):
                if v in tokens2:
                     r2[i]= tokens2.index(v)+1
                else:
                    r2[i]= i 
        word_ord_similarity = np.linalg.norm(np.array(r1) - np.array(r2)) / np.linalg.norm(np.array(r1) + np.array(r2))
        delta = 0.8 # set delta for convex combination of semantic similarity and word order similarity
    
    
    return delta*sem_similarity + (1 - delta)*word_ord_similarity

   
    

if __name__ =='__main__':
   
    s1="sun sets in the west"
    s2="sun rises in the east"
    flag=True
    print('similarity between '+'\"'+s1+'\"'+' and ' +'\"'+ s2+'\"'+ 'is: '+str(getSimilarity(s1,s2,flag)))










