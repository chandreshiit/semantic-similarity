#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 13:33:38 2018

@author: chandresh
"""
import enchant, requests, json
from nltk.tokenize import word_tokenize
import string
from collections import Counter, OrderedDict

mydict= enchant.Dict('en_US')
list_of_char_to_be_included = list(string.ascii_lowercase)
#remove 'a' and 'i' as they are legal words
list_of_char_to_be_included.remove('a')
list_of_char_to_be_included.remove('i')

url = " http://localhost:8080/RestApiDemoTomcat/rest/hello"
headers= {"Content-Type":"application/json", "Accept":"application/json"}

def detect_oov(str):
    list_of_words = word_tokenize(str.lower())
    one_length_token = [ w  for w in list_of_words if (len(w) == 1 and w not in ['a','i'])]
    list_of_words = set(list_of_words) - set(one_length_token)
    check_oov = [w  for w in list_of_words if not mydict.check(w)]
    check_oov.extend(one_length_token)
    return check_oov

def strip_extra_letters(w):
     freqdict = Counter(w)
     od = OrderedDict.fromkeys(w)
     newstr=''
     for letter in od:
         if freqdict[letter]>3:
             freqdict[letter]=3
         newstr+= letter*freqdict[letter]
     return newstr
 
def confusion_set_generation(w):
    # any repititions of more than 3 letters are reduced back to 3 letters follwoing Kaufmann and
     #Kalita (2010)
    w = strip_extra_letters(w)
#    Second, IV words within a thresh-
#    old T c character edit distance of the given OOV
#    word are calculated 
    payload = {"query":w, "max_dist":"2"}
    candidates_kedit_away_from_w = requests.post(url,
                                                 data=json.dumps(payload),
                                                 headers=headers)
    if candidates_kedit_away_from_w.status_code == 200:
        return candidates_kedit_away_from_w.json()[w]
    
"""
Step 1. OOV detection
"""
oov_words  = detect_oov('willll rch thr b4 u')    
#print(oov_words)
"""
Step 2. Confusion set generation
"""

confusionset=dict()
for w in oov_words:
    confusionset[w] = confusion_set_generation(w)
    


    