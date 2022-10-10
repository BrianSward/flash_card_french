# Imports
from tkinter import *
import pandas
import random
import json

# Constants & Data
BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
words = {}

try:
    data = pandas.read_csv("data/learn_these_words.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
    words = data.to_dict(orient="records")
else:
    words = data.to_dict(orient="records")


# Functions
def mark_done():
    global current_word
    global timer
    window.after_cancel(timer)
    current_word = random.choice(words)
    canvas.itemconfig(flash_title, text="French", fill="black")
    canvas.itemconfig(flash_word, text=current_word['French'], fill="black")
    canvas.itemconfig(app_background, image=front_img)
    timer = window.after(3000, func=flip_over)


def flip_over():
    canvas.itemconfig(flash_title, text="English", fill="white")
    canvas.itemconfig(flash_word, text=current_word['English'], fill="white")
    canvas.itemconfig(app_background, image=back_img)


def mark_known():
    """here the index = False prevents repeat indexing"""
    words.remove(current_word)
    data = pandas.DataFrame(words)
    data.to_csv("data/learn_these_words.csv", index=False)
    mark_done()


# UI Dev
window = Tk()

window.title("Flash(man) Cards Project")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50, width=800, height=530)

# logic to make card flip after 3000 ms
timer = window.after(3000, func=flip_over)

canvas = Canvas(width=800, height=530, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="./images/card_front.png")
back_img = PhotoImage(file="./images/card_back.png")
app_background = canvas.create_image(400, 265, image=front_img)
canvas.grid(column=0, row=0, columnspan=2)
flash_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
flash_word = canvas.create_text(400, 265, text="Word", font=("Ariel", 60, "bold"))

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, command=mark_done, bg=BACKGROUND_COLOR, highlightthickness=0)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, command=mark_known, bg=BACKGROUND_COLOR, highlightthickness=0)
right_button.grid(column=1, row=1)

mark_done()

window.mainloop()
