import json
import pickle
import string
import numpy as np
import random
import nltk
import os
import glob

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit, send
from tensorflow.keras.models import Sequential, load_model

intents = json.loads(open('dataset/bandaaceh.json').read())
model = load_model('model/model.h5')
words = pickle.load(open('model/indo_words.pkl', 'rb'))
classes = pickle.load(open('model/indo_classes.pkl', 'rb'))

# Create stemmer
stemmer = StemmerFactory().create_stemmer()


def clean_up_sentence(sentence):
    # case folding, stemming, and tokenization inputs from user
    sentence = sentence.lower()
    sentence = stemmer.stem(sentence)

    return nltk.word_tokenize(sentence)


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the input_pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return(np.array(bag))


# # Fungsi untuk membaca kelas dan memberikan list dari respon
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


# Fungsi untuk memperoleh respon berdasarkan list respon yang diperoleh dari fungsi predict_class
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result


# # Fungsi untuk menampilkan respon dari chatbot
def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return res


# Web Framework = Flask
app = Flask(__name__,
            static_folder="static",
            static_url_path="")

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)


@app.route('/')
def sessions():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@socketio.on('send message')
def handle_my_custom_event(data):
    resp = chatbot_response(str(data))
    # print("Server menerima input : " + str(data) + "\nresp : " + resp)
    emit('response message', resp)
