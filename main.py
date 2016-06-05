#!/usr/bin/python

import os
import wikipedia
from nltk import *
from nltk.wsd import lesk
from nltk.corpus import wordnet
from nltk.tag.stanford import StanfordNERTagger
from nltk.stem.wordnet import WordNetLemmatizer

def main():
    path = os.path.join(os.getcwd())
    for pfolder in os.listdir(path):
        path = os.path.join(os.getcwd(),pfolder)
        if os.path.isdir(path) == True:
            for subfolder in os.listdir(path):
                path = os.path.join(os.getcwd(),pfolder,subfolder)
                try: 
                    rawtext = open(os.path.join(path, "en.tok.off.pos"))
                    readfile(rawtext)
                except:
                    pass
    
def readfile(rawtext):
    text_string = str()
    for line in rawtext:
        text_string += line.split()[3]
        text_string += ' '
        
    nouns, sents, lemmas = nounLemmas(text_string)
    noun_dict = nounDict(sents, lemmas)
    
    for c, noun in enumerate(lemmas):
        print(nouns[c], "\t", wikipedia.page(noun).url)
    
def nounLemmas(text):
    text = text
    tokens = wordpunct_tokenize(text)
    sents = sent_tokenize(text)
    pos_tagged = pos_tag(tokens, tagset="universal")
    lemmatizer = WordNetLemmatizer()
    
    noun_lemmas = [lemmatizer.lemmatize(word[0], wordnet.NOUN)\
    for word in pos_tagged  if word[1] == "NOUN"]
    
    nouns = [word for word in pos_tagged if word[1] == "NOUN"]
    
    return nouns, sents, noun_lemmas

def nounDict(sents, noun_lemmas):
    noun_syn_dict = dict()
    for noun in noun_lemmas:
        if noun.isalpha() == True:
            key = str(noun)
            synsets = wordnet.synsets(noun, pos="n")
            noun_syn_dict[key] = synsets
    non_ambi_dict = dict()
    ambi_noun_dict = dict()
    for noun in noun_syn_dict:
        if len(noun_syn_dict[noun]) == 1:
            non_ambi_dict[noun] = noun_syn_dict[noun]
        if len(noun_syn_dict[noun]) > 1:
            ambi_noun_dict[noun] = noun_syn_dict[noun]
            
    #print("NOT AMBIGU:\n", non_ambi_dict)
    #print("AMBIGU:\n", ambi_noun_dict)
    
    noun_dict = disAmbi(sents, ambi_noun_dict)
    for noun in non_ambi_dict:
        noun_dict[noun]= non_ambi_dict[noun]
    
    return noun_dict

def disAmbi(sents, ambi_nouns):
    noun_dict = dict()
    for noun in ambi_nouns:
        noun_dict[noun] = lesk(sents, noun, "n")
    return noun_dict
        
def nertag(text):
    st = StanfordNERTagger('stanford-ner-2015-12-09/classifiers/english.conll.4class.distsim.crf.ser.gz', 'stanford-ner-2015-12-09/stanford-ner-3.6.0.jar')
    print(st.tag(text.split()))

main()
