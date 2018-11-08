import nltk
import random
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.tokenize import word_tokenize
import pickle

from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode
import statistics


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def find_max_mode(self, list1):
        list_table = statistics._counts(list1)
        len_table = len(list_table)

        if len_table == 1:
            max_mode = statistics.mode(list1)
        else:
            new_list = []
            for i in range(len_table):
                new_list.append(list_table[i][0])
            max_mode = max(new_list)
        return max_mode
    
    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return self.find_max_mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(self.find_max_mode(votes))
        conf = choice_votes / len(votes)
        return conf

document_f = open("pickles/documents.pickle","rb")
documents = pickle.load(document_f)
document_f.close()

word_features5k_f = open("pickles/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()

#----------------------------------------------------------------------------------#

featuresets_f = open("pickles/featuresets.pickle", "rb")
featuresets = pickle.load(featuresets_f)
featuresets_f.close()

random.shuffle(featuresets)
print(len(featuresets))

training_set = featuresets[:10000]
testing_set = featuresets[10000:]


open_file = open("pickles/originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickles/MNB_classifier5k.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickles/BNB_classifier5k.pickle", "rb")
BNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickles/LogisticRegression_classifier5k.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickles/LinearSVC_classifier5k.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickles/SGDC_classifier5k.pickle", "rb")
SGDC_classifier = pickle.load(open_file)
open_file.close()

voted_classifier = VoteClassifier(classifier, LinearSVC_classifier, MNB_classifier, BNB_classifier, LogisticRegression_classifier, SGDC_classifier)

class SentHelper():

    def __init__(self):
        super().__init__()



    def find_features(self, document):
        words = word_tokenize(document)
        features = {}
        for w in word_features:
            features[w] = (w in words)

        return features


    def sentiment(self, text):
        feats = self.find_features(text)
        return voted_classifier.classify(feats), voted_classifier.confidence(feats)
    
