import json
import pickle
import numpy as np
import random
import nltk
import string

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.stem import WordNetLemmatizer
# from keras.models import Sequential, load_model
# from keras.layers import Dense, Activation, Dropout
# from keras.optimizers import SGD

nltk.download('punkt')
nltk.download('wordnet')


# Load file
words = []
classes = []
documents = []
# ignore_words = ['?','!',]

data_file = open('pola.json').read()
intents = json.loads(data_file)


# Preporcess data
for intent in intents['intents']:
    for pattern in intent['patterns']:

        # tokenize word
        w = nltk.word_tokenize(pattern)
        words.extend(w)

        # add doc in corpus
        documents.append((w, intent['tag']))

        # add tag to class list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# print(f"Words :\n{words}\nclasses :\n{classes}\ndocuments :\n{documents}")
# print(f"Words :\n{words}\n")

# lemmatization, case folding, and remove duplicate
lemmatizer = WordNetLemmatizer()
stemmer = StemmerFactory().create_stemmer()

# words = [lemmatizer.lemmatize(w.lower()) for w in words]
words = [stemmer.stem(w.lower()) for w in words if w not in string.punctuation]

words = sorted(list(set(words)))

print(f"Words :\n{words}\n")
# print(f"classes :\n{classes}\n")
# print(f"documents :\n{documents}")
