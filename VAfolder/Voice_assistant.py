import speech_recognition as sr
r = sr.Recognizer()
############################
import tkinter as tk
from tkinter import ttk
############################
import os
############################
import time
############################
import textwrap
############################
root = tk.Tk()
root.configure(bg = "#c5dea4")
root.title("Voice assitant")
root.geometry("400x300+300+300")
root.resizable(False, False)
#############################
root.columnconfigure(1, weight = 1)
root.rowconfigure(1, weight = 1)
#############################
cur_lang = "English"
image_path = os.path.join(os.path.dirname(__file__), 'mic.png')
microphone_icon = tk.PhotoImage(file =image_path)
#############################
langs = ("English", "Lietuvių")
langs_var = tk.StringVar(value=langs)
lang_option_menu = ttk.OptionMenu(root, langs_var, langs[0], *langs, command= lambda selected_value: change_lang(selected_value))
lang_option_menu.grid(column=1, row=0, sticky=tk.W)
lang_option_menu.configure(width = 7)
#############################
button = ttk.Button(root, text = "Listen", image = microphone_icon, compound = tk.LEFT, command = lambda: Button_click_en())

def change_lang(selected_value):
    global cur_lang
    cur_lang = selected_value
    if cur_lang == "English":
        button.configure(text="Listen", command=Button_click_en)
    elif cur_lang == "Lietuvių":
        button.configure(text="Klausyti", command=Button_click_lt)
    label.config(text = "")

button.grid(column = 1, row = 2, pady = 60, sticky = tk.N)

label = tk.Label(root, text = "", font = ("Comic Sans", 18), bg = root["background"])
label.grid(column = 1, row = 1)

def Button_click_lt():    
    label.config(text = "Klausau...", fg = "#3d3803", bg = root["background"])
    root.update()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            transcript = r.recognize_google(audio, language = "lt-LT")
            arithmetic_replacements = {"plius": "+", "minus": "-", "kart": "*", "padalinta iš": "/", "padalinti iš": "/", 
        "dalinti":"/", "du": "2","nulis": "0", "vienas": "1", "du": "2", "trys": "3", "keturi": "4", "penki": "5",
        "šeši": "6", "septyni": "7","aštuoni": "8", "devyni": "9"}
            for old_word, new_word in arithmetic_replacements.items():
                    transcript = transcript.replace(old_word, new_word)
            transcript_wrap = textwrap.fill("Jūs pasakėte: " + transcript, 34)
            if "apskaičiuoti" in transcript or "skaičiuoti" in transcript.split():
                new_transcript = transcript.replace("apskaičiuoti", "")
                try:
                    result = textwrap.fill(str(eval(new_transcript)))
                    transcript_wrap += "\n\n" + "Atsakymas = " + result
                except ZeroDivisionError:
                    zero_division_error_wrap = textwrap.fill("\n\nKlaida: dalyba iš nulio", 34)
                    transcript_wrap += "\n\n" + zero_division_error_wrap
                except (SyntaxError, TypeError):
                    syntax_error_wrap = textwrap.fill("\n\n Klaida: neteisinga matematinė išraiška", 34)
                    transcript_wrap += "\n\n" + syntax_error_wrap
            label.config(text = transcript_wrap, fg = "#3d3803", bg = root["background"])
        except sr.UnknownValueError:
            label.config(text = "Atleiskite, tačiau aš jūsų neišgirdau.")

def Button_click_en():    
    label.config(text = "Listening...", fg = "#3d3803", bg = root["background"])
    root.update()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            transcript = r.recognize_google(audio, language = "en-US")
            transcript_wrap = textwrap.fill("You said: " + transcript, 34)
            if "calculate" in transcript.split():
                new_transcript = transcript.replace("calculate", "")
                try:
                    result = textwrap.fill(str(eval(new_transcript)))
                    transcript_wrap += "\n\n" + "Result = " + result
                except ZeroDivisionError:
                    zero_division_error_wrap = textwrap.fill("\n\nError: division by zero", 35)
                    transcript_wrap += "\n\n" + zero_division_error_wrap
                except SyntaxError:
                    syntax_error_wrap = textwrap.fill("\n\n Error: invalid expression")
                    transcript_wrap += "\n\n" + syntax_error_wrap
            label.config(text = transcript_wrap, fg = "#3d3803", bg = root["background"])
        except sr.UnknownValueError:
            label.config(text = "I'm sorry, but I could not hear you")

root.mainloop()


