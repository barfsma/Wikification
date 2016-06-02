#!/usr/bin/python

import os
from nltk.tag.stanford import StanfordNERTagger

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
    nertag(text_string)
                    
def nertag(text):
    st = StanfordNERTagger('stanford-ner-2015-12-09/classifiers/english.conll.4class.distsim.crf.ser.gz', 'stanford-ner-2015-12-09/stanford-ner-3.6.0.jar')
    print(st.tag(text.split()))
main()
