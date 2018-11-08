import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.chunk import *
from sklearn import svm
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import re

from SentHelper.Sentiment import SentHelper

###
##
#
class Basic_NLP_Tasks():
    def __init__(self):
        super().__init__()
        self.stop_words = set(stopwords.words("English"))
        self.PortStemmer = PorterStemmer()
        self.SentHelper = SentHelper()
        self.eng_vocab = set(w.lower() for w in nltk.corpus.words.words())

    def return_tasks(self):
        return 'NULL'

    def remove_stopwords(self, sentence):
        sentence = self.tok_words(sentence)
        sentence_filtered = []
        sentence_filtered = [w for w in sentence if not w in self.stop_words]
        sentence_filtered = self.tok_to_sent(sentence_filtered)
        return sentence_filtered

    def stem_words(self, words):
        words = [self.PortStemmer.stem(word) for word in words if not word.isdigit()]
        return words

    ## For finding other words
    def findTags(self, tagList):
        arr = []
        testarr = []
        for word, tag in tagList:
            tag = str(tag).strip().upper()
            if(tag == 'NNS' or tag == 'NN' or tag == 'VB' or tag == 'NNP'):
                testarr.append(tag)
                arr.append(word)
        
        return arr

    def isEnglishWord(self, words):
        words = [word for word in words if word in self.eng_vocab]
        print(words)
        return words

    def find_sentiment(self, tweet):
        print(tweet)
        
        sent_val, conf = self.SentHelper.sentiment(tweet)
        print("{}      ->   {}   ->    {}\n".format(tweet, sent_val, str(conf)))
        return sent_val, conf

    def tok_words(self, content):
        get_custom_tok = PunktSentenceTokenizer(content)
        tokens = get_custom_tok.tokenize(content)
        return tokens

    def tok_to_sent(self, tok):
        sentence = ' '.join(t for t in tok)
        return sentence


class POS_Retriever(Basic_NLP_Tasks):
    def __init__(self):
        super().__init__()

    def find_POS(self, content):
        arrResult = self.getPOS(content)
        return arrResult

        

    def getPOS(self, content):
        
        arrOfResult = []
        get_custom_tok = PunktSentenceTokenizer(content)
        tokens = get_custom_tok.tokenize(content)
        try: 
            for i in tokens:
                tagged = nltk.pos_tag(nltk.word_tokenize(i), lang='eng')      
                arrOfResult = tagged
            return arrOfResult

        except Exception as e:
            print(str(e))
           


class NER_Retriever(Basic_NLP_Tasks):
    def __init__(self):
        super().__init__()
    
    def find_NER(self, content):
        arrResults = self.getNER(content)
        return arrResults

    def getNER(self, content):
        get_custom_tok = PunktSentenceTokenizer(content)
        tokens = get_custom_tok.tokenize(content)
        arrOfResult = []
        try: 
            for i in tokens:
                text = ''
                words = nltk.word_tokenize(i)
                tagged = nltk.pos_tag(nltk.word_tokenize(i))
                namedEnt = nltk.ne_chunk(tagged, binary=True)
                arrOfResult = self.cleanEntityList(arrOfResult, words, namedEnt)
            return arrOfResult

        except Exception as e:
            print(str(e))

    def cleanEntityList(self, arr, sentence, ent):
        arr = []
        for chunk in ent:
            if hasattr(chunk, 'label'):
                arr.append(str((chunk.label(), ' '.join(c[0] for c in chunk))))
        return arr