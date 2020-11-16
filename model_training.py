import json
import pickle
import numpy as np
import random
import nltk
import string
import glob

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

# Load file
words = []
classes = []
documents = []

data_file = open('dataset/bandaaceh.json').read()
intents = json.loads(data_file)

# Create stemmer and stopwords
stemmer = StemmerFactory().create_stemmer()
stopwords = StopWordRemoverFactory().get_stop_words()

# Preporcess data
for intent in intents['intents']:
    for pattern in intent['input_patterns']:

        # Word tokenization
        pattern = nltk.word_tokenize(pattern)
        # Case folding
        pattern = [word.lower() for word in pattern]
        # Filtering
        pattern = [
            word for word in pattern if word not in stopwords and word.isalpha() and word not in string.punctuation]
        # Stemming
        pattern = [stemmer.stem(word) for word in pattern]

        # insert to words list
        words.extend(pattern)

        # add doc in corpus
        documents.append((pattern, intent['tag']))

        # add tag to class list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])


# Sort words and classes
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# Save to file in binary
pickle.dump(words, open('model/indo_words.pkl', 'wb'))
pickle.dump(classes, open('model/indo_classes.pkl', 'wb'))


# Create Data Training and Testing (In vector shape of words and classes)
training = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]

    # create our bag of words array with 1, if word match found in current pattern
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
        # output is a '0' for each tag and '1' for current tag (for each pattern)
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])  # feature and it class in binary

# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)
# create train and test lists. X - input_patterns, Y - intents
X_train = list(training[:, 0])  # feature from words vector
y_train = list(training[:, 1])  # label for class/tag
print("Training data created")


# BUILD MODEL
# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# equal to number of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(X_train[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))
model.summary()

# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
# sgd = SGD(lr=0.0015, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer="adam", metrics=['accuracy'])

# fitting and saving the model
hist = model.fit(np.array(X_train), np.array(y_train),
                 epochs=150, batch_size=5, verbose=1)
model.save('model/model.h5', hist)
print("model created")
