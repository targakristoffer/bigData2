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


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers
    
    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)

            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

short_pos = open("short_reviews/positive.txt", "r").read()
short_neg = open("short_reviews/negative.txt", "r").read()

documents = []
all_words = []

# J is adjective, r is adverb, and v is verb
# allowed_word_types = ["J", "R", "V"]
allowed_word_types = ["J", "R", "V"]

for p in short_pos.split('\n'):
    documents.append((p, "pos"))
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())
    
for p in short_neg.split('\n'):
    documents.append((p, "neg"))
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())
    

short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)

save_documents = open("pickled_algos/documents.pickle","wb")
pickle.dump(documents, save_documents)
save_documents.close()

all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:5000]
save_word_features = open("pickled_algos/word_features5k.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]

save_features = open("featuresets.pickle", "wb")
pickle.dump(featuresets, save_features)
save_features.close()


random.shuffle(featuresets)
training_set = featuresets[:10000]
testing_set = featuresets[10000:]


#-------------------------------------------------------------------#
classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy: ", (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)

save_classifier = open("pickled_algos/originalnaivebayes5k.pickle", "wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

#-------------------------------------------------------------------#
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB Classifier accuracy: ", (nltk.classify.accuracy(MNB_classifier,testing_set))*100)

save_classifier = open("pickled_algos/MNB_classifier5k.pickle", "wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

#-------------------------------------------------------------------#
BNB_classifier = SklearnClassifier(BernoulliNB())
BNB_classifier.train(training_set)
print("BNB Classifier accuracy: ", (nltk.classify.accuracy(BNB_classifier,testing_set))*100)

save_classifier = open("pickled_algos/BNB_classifier5k.pickle", "wb")
pickle.dump(BNB_classifier, save_classifier)
save_classifier.close()

#-------------------------------------------------------------------#
LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression Classifier accuracy: ", (nltk.classify.accuracy(LogisticRegression_classifier,testing_set))*100)

save_classifier = open("pickled_algos/LogisticRegression_classifier5k.pickle", "wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()

#-------------------------------------------------------------------#
SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier Classifier accuracy: ", (nltk.classify.accuracy(SGDClassifier_classifier,testing_set))*100)

save_classifier = open("pickled_algos/SGDC_classifier5k.pickle", "wb")
pickle.dump(SGDClassifier_classifier, save_classifier)
save_classifier.close()

#-------------------------------------------------------------------#
LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC Classifier accuracy: ", (nltk.classify.accuracy(LinearSVC_classifier,testing_set))*100)

save_classifier = open("pickled_algos/LinearSVC_classifier5k.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()





voted_classifier = VoteClassifier(SGDClassifier_classifier, classifier, MNB_classifier, BNB_classifier, LogisticRegression_classifier, LinearSVC_classifier)
print("Voted Classifier accuracy: ", (nltk.classify.accuracy(voted_classifier,testing_set))*100)
