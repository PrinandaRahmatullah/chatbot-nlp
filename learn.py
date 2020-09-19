import tkinter
from tkinter import messagebox, Button
from tkinter import *

me = tkinter.Tk()
# me.geometry("400x600")


def helloCallBack():
    msg = messagebox.showinfo("Hello Prinanda", "Hello Rahmatullah")


# # Label
# L = Label(me,
#           text="KKP 2020",
#           fg="black",
#           bg='white',
#           width=30,
#           height=10
#           )
# L.place(x=0, y=0)


# Button
B = Button(me,
           text="Click",
           command=helloCallBack,
           width=10,
           height=5,
           bg="green",
           fg="white"
           )
# B.place(x=300, y=500)

label = Label(me, text="Fill Name")

# Entry
E = Entry(me, fg="black", bg="#FFFFFF", width=100)


label.pack()
E.pack()
B.pack()

photo = PhotoImage(file="assets/tele.png")
button = Button(me, text="Tanya", image=photo, compound='left', bg="white")
button.pack()


me.mainloop()
