#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 13:33:38 2018

@author: chandresh
"""
import enchant, requests, json
from nltk.tokenize import word_tokenize
import string
from collections import Counter, OrderedDict, defaultdict
from metaphone import doublemetaphone
from Levenshtein import distance
import kenlm,math

mydict= enchant.Dict('en_US')
list_of_char_to_be_included = list(string.ascii_lowercase)
#remove 'a' and 'i' as they are legal words
list_of_char_to_be_included.remove('a')
list_of_char_to_be_included.remove('i')

url = " http://localhost:8080/JavaApiTest/rest/hello"
headers= {"Content-Type":"application/json", "Accept":"application/json"}
MAX_DIST="2"

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
 
def confusion_set_generation(w, max_dist):
    # any repititions of more than 3 letters are reduced back to 3 letters follwoing Kaufmann and
     #Kalita (2010)
    w = strip_extra_letters(w)
#    Second, IV words within a thresh-
#    old T c character edit distance of the given OOV
#    word are calculated 
    payload = {"query":w, "max_dist":max_dist}
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
Step 2. Slang correction
"""
# load slang dict
slang_match ={}
with open('/home/chandresh/ckm/data/slang/myslang.json', 'r') as fid:
    slangdict= json.load(fid)
    
    list_length= len(oov_words)
    count=[]
    for i in range(list_length):
        if oov_words[i].lower() in slangdict:
            count.append(i)            
    for i in count:
        slang_match[oov_words[i]]= slangdict[oov_words[i].lower()]
    for i in sorted(count, reverse=True):
        del oov_words[i]

"""
Step 3. Confusion set generation
"""

confusionset=dict()
for w in oov_words:
    confusionset[w] = confusion_set_generation(w, max_dist=MAX_DIST)
    
"""
Step 4. Double Metaphone for decoding IV words to their phonetics
"""
reduced_cf_set = defaultdict(list)
for oov_word, iv_words in confusionset.items():
    oov_phonetic = doublemetaphone(oov_word)[0]
    for word in iv_words:
        iv_phonetic = doublemetaphone(word[0])[0]
        if distance(oov_phonetic, iv_phonetic) <=1:
            reduced_cf_set[oov_word].append(word[0])
"""
step 5. Rank the IV words using a language model
"""
model=kenlm.LanguageModel('/home/chandresh/ckm/data/lm/news.arpa')

for oov_word, cf_wordset in reduced_cf_set.items():
    list_length= len(cf_wordset)
    for i in range(list_length):
        lm_score = model.score(cf_wordset[i])
        reduced_cf_set[oov_word][i] = (cf_wordset[i], lm_score)
        
    # sort the list and pick top 10%
    reduced_cf_set[oov_word].sort(reverse=True, key=lambda item:item[1])
    length= len(reduced_cf_set[oov_word])
    reduction =math.ceil( length*.2)
    if reduction>0:
        reduced_cf_set[oov_word]=reduced_cf_set[oov_word][0:reduction+1]
    

 










