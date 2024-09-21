import json
import pickle
import numpy as np
import random
import nltk
import string
# nltk.download('punkt')

from matplotlib import pyplot as plt
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Load file
words = []
classes = []
documents = []

data_file = open('dataset/bandaaceh.json').read()
intents = json.loads(data_file)

# Create stemmer and stopwords
stemmer = StemmerFactory().create_stemmer()
stopwords = StopWordRemoverFactory().get_stop_words()

# Preprocess data
for intent in intents['intents']:
    for pattern in intent['input_patterns']:
        # Word tokenization
        pattern = nltk.word_tokenize(pattern)
        # Case folding
        pattern = [word.lower() for word in pattern]
        # Filtering (remove stopwords, punctuation, and non-alphabetic tokens)
        pattern = [
            word for word in pattern if word not in stopwords and word.isalpha() and word not in string.punctuation]
        # Stemming
        pattern = [stemmer.stem(word) for word in pattern]

        # Add to words list
        words.extend(pattern)

        # Add document (pattern + tag)
        documents.append((pattern, intent['tag']))

        # Add tag to class list if it's not already there
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Sort words and classes
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# Save words and classes to file (binary)
pickle.dump(words, open('model/indo_words.pkl', 'wb'))
pickle.dump(classes, open('model/indo_classes.pkl', 'wb'))

# Create training data (In vector form of words and classes)
training = []
output_empty = [0] * len(classes)  # Create an empty output array

# training set, bag of words for each sentence
for doc in documents:
    # Initialize our bag of words
    bag = []
    pattern_words = doc[0]

    # Create bag of words array (1 if word is in pattern, 0 otherwise)
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # Create output row (1 for the current tag, 0 for others)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# Shuffle and convert training data to numpy array
random.shuffle(training)
training = np.array(training, dtype=object)

# Split into X and y (features and labels)
X_train = np.array(list(training[:, 0]))  # Feature from word vector
y_train = np.array(list(training[:, 1]))  # Label for class/tag

print("Training data created")

# BUILD MODEL
# Create model: 3 layers (128, 64 neurons, output layer based on number of classes)
model = Sequential()
model.add(Dense(128, input_shape=(len(X_train[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(classes), activation='softmax'))  # Output layer for classes

model.summary()

# Compile model
model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])

# Callbacks for EarlyStopping and ModelCheckpoint
early_stop = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
model_checkpoint = ModelCheckpoint('model/best_model.h5', monitor='loss', save_best_only=True, verbose=1)

# Fit model with callbacks
hist = model.fit(X_train, y_train, epochs=150, batch_size=5, verbose=1, callbacks=[early_stop, model_checkpoint])

# Save the final model (if not the best one)
model.save('model/model.h5')

print("Model created and saved")
