import tkinter
import json
import pickle
import numpy as np
import random
import nltk
import string
import glob

# from nltk.stem import WordNetLemmatizer
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

nltk.download('punkt')

# Load file
words = []
classes = []
documents = []

# folders = glob.glob("dataset/*.json")
# for fol in folders:
#     data_file = open(fol).read()

data_file = open('dataset/bandaaceh.json').read()
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


words = [w.lower() for w in words if w not in string.punctuation]
words = sorted(list(set(words)))

# sort classes
classes = sorted(list(set(classes)))

print(len(documents), "documents")
print(len(classes), "classes")

# Save to file in binary
pickle.dump(words, open('model/indo_words.pkl', 'wb'))
pickle.dump(classes, open('model/indo_classes.pkl', 'wb'))


# Create Data Training and Testing
training = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [word.lower() for word in pattern_words]

    # create our bag of words array with 1, if word match found in current pattern
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
        # output is a '0' for each tag and '1' for current tag (for each pattern)
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])  # feature and it class in binary
# print(training)

# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)
# create train and test lists. X - patterns, Y - intents
train_x = list(training[:, 0])  # feature from words vector
train_y = list(training[:, 1])  # label for class/tag
print("Training data created")


# BUILD MODEL

# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# equal to number of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))
model.summary()

# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd, metrics=['accuracy'])

# fitting and saving the model
hist = model.fit(np.array(train_x), np.array(train_y),
                 epochs=200, batch_size=5, verbose=1)
model.save('model/model.h5', hist)
print("model created")
