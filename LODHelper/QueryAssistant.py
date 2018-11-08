import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.chunk import *
from sklearn import svm
import re

from NLPHelper.Basic_NLP_Tasks import NER_Retriever, Basic_NLP_Tasks

###
##
#
class QueryAssistant():

    

    def __init__(self):
        super().__init__()
        self.NER_Retriever = NER_Retriever()

        
    
    def test(self, content):
        print('(+) QUERY PREP - 0.1')
        arrOfEntities = []
        otherwordlist = []
        arrOfOtherWords = {}

        arrOfResult = []

        get_custom_tok = PunktSentenceTokenizer(content)
        tokens = get_custom_tok.tokenize(content)
        print('(+) QUERY PREP - 1.0 INIT RDY')

        ### MOVE TO OWN FUNCITON LATER
        #words = nltk.word_tokenize(content)
        #all_words = nltk.FreqDist(words)
        #filtered_word_freq = dict((word, freq) for word, freq in all_words.items() if not word.isdigit() and word not in self.stop_words)
        #print(filtered_word_freq)
    

        try:
            print('(+) QUERY PREP - 1.2') 
            otCounter = 0
            for i in tokens:
                words = nltk.word_tokenize(i)
                
                ## MOVE TO SEPERATE FUNCTION (REMOVE STOPWORDS)
                sentence_filtered = self.NER_Retriever.remove_stopwords(words)

                tagged = nltk.pos_tag(sentence_filtered)
                namedEnt = nltk.ne_chunk(tagged, binary=True)

                for chunk in namedEnt:
                    if hasattr(chunk, 'label') and str(' '.join(c[0] for c in chunk)) not in arrOfEntities:
                        print(chunk.label(), ' '.join(c[0] for c in chunk))                      
                        arrOfResult.append(str((chunk.label(), ' '.join(c[0] for c in chunk))))
                        arrOfEntities.append(str(' '.join(c[0] for c in chunk)))
  

                print('(+) QUERY PREP - 2.12')
                arrOfOtherWords['sentence_' + str(otCounter)] = []
                ##IGNORE STEMMING##
                #arrOfOtherWords['sentence_' + str(otCounter)].append(self.NER_Retriever.stem_words(self.findTags(tagged)))
                ##
                arrOfOtherWords['sentence_' + str(otCounter)].append(self.NER_Retriever.findTags(tagged))
                otCounter += 1
                
            

            
            ## Shift through other words
            for key, value in arrOfOtherWords.items():
                for word in value[0]:
                    if word not in otherwordlist and word not in arrOfEntities and re.match("^[a-zA-Z0-9_]*$", word):
                        if word[-1] == 's' and word not in arrOfEntities and word not in otherwordlist:
                            word = word[:-1]
                            otherwordlist.append(word)
                        else:
                            otherwordlist.append(word)

            ##IGNORE
            #otherwordlist = self.NER_Retriever.isEnglishWord(otherwordlist)           
            
            
            print('----'*20)
            for a in arrOfEntities:
                print(a)

            print('----'*20)
            for w in otherwordlist:
                print(w)

            return arrOfEntities, otherwordlist

        except Exception as e:
            print(str(e))



     
        

