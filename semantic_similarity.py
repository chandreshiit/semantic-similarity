#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 16:56:16 2018

@author: chandresh
"""
from pywsd import disambiguate
#from pywsd.similarity import max_similarity as maxsim
from nltk.corpus import  wordnet as wn
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
            
            subsumer = syn1[1].lowest_common_hypernyms(syn2[1], simulate_root=True)[0]
            h =subsumer.max_depth() + 1 # as done on NLTK wordnet        
            syn1_dist_subsumer = syn1[1].shortest_path_distance(subsumer,simulate_root =True)
            syn2_dist_subsumer = syn2[1].shortest_path_distance(subsumer,simulate_root =True)
            l  =syn1_dist_subsumer + syn2_dist_subsumer
            f1 = np.exp(-alpha*l)
            a  = np.exp(beta*h)
            b  = np.exp(-beta*h)
            f2 = (a-b) /(a+b)
            sim = f1*f2
            L1[syn1[0]].append(sim)          
            L2[syn2[0]].append(sim)
    return L1, L2       
    
def getSimilarity(s1,s2):
    
    s1_wsd = disambiguate(s1) # using default disambiguation
    s2_wsd = disambiguate(s2)
    
    # remove None synsets
    s1_wsd = [syn  for syn in s1_wsd if syn[1]]
    s2_wsd = [syn  for syn in s2_wsd if syn[1]]
    
    #vector_length = max(len(s1_wsd), len(s2_wsd))
    
    L1,L2 = _synset_similarity(s1_wsd,s2_wsd)
    V1 =np.array( [max(L1[key]) for key in L1.keys()])
    V2 = np.array([max(L2[key]) for key in L2.keys()])
    S  = np.linalg.norm(V1)*np.linalg.norm(V2)
    C1 = sum(V1>=benchmark_similarity)
    C2 = sum(V2>=benchmark_similarity)

    Xi = (C1+C2) / gamma

    if C1+C2 == 0:
        Xi = max(V1.size, V2.size) / 2
    return S/Xi


if __name__ =='__main__':
    s1= 'cyclone hit my home badly'
    s2 ='hurricane striked my house severly'
    
    print('similarity between '+'\"'+s1+'\"'+' and ' +'\"'+ s2+'\"'+ 'is: '+str(getSimilarity(s1,s2)))









