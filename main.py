import os
from nltk.tag.stanford import StanfordNERTagger

def main():
	readfile()
	
def readfile():
    path = os.path.join(os.getcwd())
    for pfolder in os.listdir(path):
        path = os.path.join(os.getcwd(),pfolder)
        if os.path.isdir(path) == True:
            for subfolder in os.listdir(path):
                path = os.path.join(os.getcwd(),pfolder,subfolder)
                rawtext = open(os.path.join(path, "en.tok.off.pos.ent"))
                nertag(rawtext)
            
def nertag(rawtext):
	st = StanfordNERTagger('stanford-ner-2014-06-16/classifiers/english.conll.4class.distsim.crf.ser.gz', 'stanford-ner-2014-06-16/stanford-ner-3.4.jar')
	for sentence in rawtext:
		st.tag(sentence.split()) 
main()
