import json
import pickle
import string
import numpy as np
import random
import nltk

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from tensorflow.keras.models import Sequential, load_model


intents = json.loads(open('dataset/pola.json').read())
model = load_model('model/chatbot_model.h5')
words = pickle.load(open('model/words.pkl', 'rb'))
classes = pickle.load(open('model/classes.pkl', 'rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array and stem each word - create short form for word
    # return [lemmatizer.lemmatize(word.lower()) for word in (nltk.word_tokenize(sentence))]
    return [word.lower() for word in (nltk.word_tokenize(sentence))]
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence


def bow(sentence, words, show_details=True):
    # tokenize the pattern
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


@socketio.on('send message')
def handle_my_custom_event(data):
    resp = chatbot_response(str(data))
    print("Server menerima input : " + str(data) + " resp : " + chatbot_response(resp))
    emit('response message', resp)
