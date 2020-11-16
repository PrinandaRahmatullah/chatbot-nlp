import tkinter
import json
import pickle
import string
import numpy as np
import random
import nltk

from tkinter import *
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from tensorflow.keras.models import Sequential, load_model


intents = json.loads(open('dataset/bandaaceh.json').read())
model = load_model('model/model.h5')
words = pickle.load(open('model/indo_words.pkl', 'rb'))
classes = pickle.load(open('model/indo_classes.pkl', 'rb'))

# Create stemmer and stopwords
stemmer = StemmerFactory().create_stemmer()
stopwords = StopWordRemoverFactory().get_stop_words()


def clean_up_sentence(sentence):
    # tokenization, case floding, filtering, and stemming inputs from user
    sentence = nltk.word_tokenize(sentence)
    sentence = [word.lower() for word in sentence]
    sentence = [
        word for word in sentence if word not in stopwords and word.isalpha() and word not in string.punctuation]
    sentence = [stemmer.stem(word) for word in sentence]

    return sentence


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


# Fungsi untuk membaca kelas dan memberikan list dari respon
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


# Fungsi untuk menampilkan respon dari chatbot
def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return res


# Membuat tampilan GUI

# Fungsi untuk menampilkan chat/respon
def send():
    msg = EntryBox.get().strip()
    EntryBox.delete(0, END)

    if all(x.isalpha() or x.isspace() for x in msg):
        if msg.lower() == "exit":
            base.quit()

        if msg != '':
            ChatLog.config(state=NORMAL)
            ChatLog.config(foreground="#442265", font=("Calibri", 12))

            ChatLog.insert(END, "Kamu :\n\t" + msg + '\n\n')
            res = chatbot_response(msg)
            ChatLog.insert(END, "Robot :\n\t" + res + '\n\n')

            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)


# Fungsi untuk menampilkan about me
def about_me():
    tkinter.messagebox.showinfo(
        "About Me", "Prinanda Rahmatullah\nStudent of Informatics Department Syiah Kuala University\n\nDosen Pembimbing Lapangan : Viska Mutiawani, B.IT, M.IT.\n\n\xA9 Internship Program on Dinas Kominfotik Banda Aceh August 2020")


# Membuat window tKinter
base = Tk()
base.title("Chatbot Banda Aceh Smart City")
base.geometry("450x600")
base.resizable(width=FALSE, height=FALSE)

# Membuat menu bar
menu = Menu(base)
base.config(menu=menu)

filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu, font=("Monospace Regular", 12))
filemenu.add_command(label="Exit", command=base.quit,
                     font=("Monospace Regular", 11))

helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu, font=("Monospace Regular", 12))
helpmenu.add_command(label="About", command=about_me,
                     font=("Monospace Regular", 11))


# History Chat
ChatLog = Text(base, bd=0, bg="white", height="8",
               width="50", font="Calibri", padx=5, pady=5)
ChatLog.config(state=DISABLED)

# Scrollbar
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="left_ptr")
ChatLog['yscrollcommand'] = scrollbar.set
ChatLog.insert(
    END, "Kamu :\n\t" + "Selamat Datang di room Chat Robot. Ada yang bisa dibantu?" + '\n\n')
# Tombol utk mengirim pertanyaan + gambar
photo = PhotoImage(file="static/assets/send2.png")
SendButton = Button(base, font=("Monospace Regular", 10, "bold"), image=photo, width="10", height=5,
                    bd=0, activebackground="#EEEEEE", fg='#000000',
                    command=send)

# Tambah tombol Enter untuk kirim pertanyaan
base.bind('<Return>', lambda enter: send())

# Membuat input box
EntryBox = Entry(base, bd=0, bg="white", font=("Helvetica", 16))

# Label Copyright
my_name = Label(text="\xA9 KKP Kominfotik 2020")

# Place all components on the screen
scrollbar.place(x=430, y=6, height=500)
ChatLog.place(x=6, y=6, height=500, width=420)
SendButton.place(x=374, y=515, height=50, width=70)
EntryBox.place(x=6, y=515, height=50, width=360)
my_name.pack(side="bottom", pady=10)

base.mainloop()
