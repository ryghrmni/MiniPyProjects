import tkinter as tk
from tkinter import messagebox, scrolledtext
from nltk.corpus import wordnet as wn
import pyttsx3
import random
import difflib

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Global variables for word info
current_word_info = ""
vocabulary_words = []
current_word_index = 0
dark_mode = False  # Global variable to track the mode (light/dark)

def toggle_mode():
    """Switch between light and dark modes."""
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        root.configure(bg='#2b2b2b')
        dictionary_frame.configure(bg='#2b2b2b')
        navbar_frame.configure(bg='#444444')
        flashcard_frame.configure(bg='#2b2b2b')
        learning_english_frame.configure(bg='#2b2b2b')
        
        # Update widgets to dark mode
        menu_label.config(bg='#2b2b2b', fg='white')
        title_label.config(bg='#2b2b2b', fg='white')
        flashcard_title.config(bg='#2b2b2b', fg='white')
        learning_label.config(bg='#2b2b2b', fg='white')
        placeholder_label.config(bg='#2b2b2b', fg='white')
        entry.config(bg='#555555', fg='white')
        text_area.config(bg='#555555', fg='white')
        flashcard_label.config(bg='#555555', fg='white')

        # Update button text
        mode_button.config(text="Light Mode", bg='#555555', fg='white')
    else:
        root.configure(bg='#f0f0f0')
        dictionary_frame.configure(bg='#f0f0f0')
        navbar_frame.configure(bg='#FF5722')
        flashcard_frame.configure(bg='#f0f0f0')
        learning_english_frame.configure(bg='#f0f0f0')

        # Update widgets to light mode
        menu_label.config(bg='#f0f0f0', fg='black')
        title_label.config(bg='#f0f0f0', fg='black')
        flashcard_title.config(bg='#f0f0f0', fg='black')
        learning_label.config(bg='#f0f0f0', fg='black')
        placeholder_label.config(bg='#f0f0f0', fg='black')
        entry.config(bg='white', fg='black')
        text_area.config(bg='white', fg='black')
        flashcard_label.config(bg='white', fg='black')

        # Update button text
        mode_button.config(text="Dark Mode", bg='#FF5722', fg='black')

def get_word_info():
    word = entry.get().strip()
    if not word:
        messagebox.showerror("Input Error", "Please enter a word.")
        return

    synsets = wn.synsets(word)
    text_area.delete(1.0, tk.END)

    if not synsets:
        # Find the most similar word using difflib
        similar_words = difflib.get_close_matches(word, wn.words(), n=1)
        if similar_words:
            suggestion = similar_words[0]
            messagebox.showinfo("Did you mean?", f"No matches found for '{word}'. Did you mean '{suggestion}'?")
            entry.delete(0, tk.END)
            entry.insert(0, suggestion)
            synsets = wn.synsets(suggestion)
        else:
            text_area.insert(tk.END, f"No synsets found for the word '{word}'\n")
            return

    word_info = ""
    for i, synset in enumerate(synsets, 1):
        pos = synset.pos()
        definition = synset.definition()
        examples = synset.examples()

        info = f"Synset {i}:\n"
        info += f"Part of Speech (POS): {pos}\n"
        info += f"Definition: {definition}\n"
        
        if examples:
            info += f"Examples: {', '.join(examples)}\n"
        
        info += "\n"
        word_info += info

    text_area.insert(tk.END, word_info)
    global current_word_info
    current_word_info = word_info

def pronounce_word():
    word = entry.get().strip()
    if not word:
        messagebox.showerror("Input Error", "Please enter a word.")
        return
    engine.say(word)
    engine.runAndWait()

def speak_word_info():
    if current_word_info:
        engine.say(current_word_info)
        engine.runAndWait()
    else:
        messagebox.showerror("No Info", "Please get word info first.")

# ---------------- Flashcard Vocabulary Feature ----------------

def load_random_words():
    """Load 10 random words with their definitions from WordNet."""
    global vocabulary_words, current_word_index
    vocabulary_words = random.sample(list(wn.words()), 10)
    current_word_index = 0
    show_flashcard_word()

def show_flashcard_word():
    """Display the current word and its definition in the flashcard."""
    global current_word_index
    if current_word_index < len(vocabulary_words):
        word = vocabulary_words[current_word_index]
        synsets = wn.synsets(word)
        if synsets:
            definition = synsets[0].definition()  # Taking the first synset definition
        else:
            definition = "Definition not available."

        flashcard_text.set(f"Word: {word}\n\nDefinition: {definition}")
    else:
        flashcard_text.set("End of flashcards. You can restart or go back to the menu.")

def next_flashcard():
    """Move to the next word in the flashcard."""
    global current_word_index
    if current_word_index < len(vocabulary_words) - 1:
        current_word_index += 1
        show_flashcard_word()
    else:
        messagebox.showinfo("Flashcards", "You've reached the last word.")

def pronounce_flashcard_word():
    """Pronounce the current flashcard word."""
    if current_word_index < len(vocabulary_words):
        word = vocabulary_words[current_word_index]
        engine.say(word)
        engine.runAndWait()
    else:
        messagebox.showerror("Error", "No word available to pronounce.")

def learn_vocabulary():
    """Open the flashcard interface for learning vocabulary."""
    load_random_words()
    menu_frame.pack_forget()
    flashcard_frame.pack(fill="both", expand=True)

# ---------------- GUI Setup ----------------

# Create the main window
root = tk.Tk()
root.title("Word Meaning and Pronunciation")
root.geometry("600x400")
root.configure(bg='#f0f0f0')

# Load the background image
bg_image = tk.PhotoImage(file="E:/Projects/MiniPyProjects/dictionary-application/image.png")

# ---------------- Main Menu Frame ----------------
menu_frame = tk.Frame(root, bg="#f0f0f0")
menu_frame.pack(fill="both", expand=True)

# Create a label for the background image
bg_label = tk.Label(menu_frame, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

menu_label = tk.Label(menu_frame, text="Welcome to the Application", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
menu_label.pack(pady=20)

dictionary_button = tk.Button(menu_frame, text="Dictionary", font=("Arial", 14), bg="#4CAF50", fg="white", width=20, command=lambda: open_frame(dictionary_frame))
dictionary_button.pack(pady=10)

learning_button = tk.Button(menu_frame, text="Learning English", font=("Arial", 14), bg="#2196F3", fg="white", width=20, command=lambda: open_frame(learning_english_frame))
learning_button.pack(pady=10)

# ---------------- Dictionary Frame ----------------
dictionary_frame = tk.Frame(root, bg="#f0f0f0")

# Create a navigation bar frame for the Back button and mode toggle
navbar_frame = tk.Frame(dictionary_frame, bg="#FF5722", height=40)
navbar_frame.pack(fill="x", side="top")

back_button = tk.Button(navbar_frame, text="Back to Menu", font=("Arial", 12), bg="#FF5722", fg="white", command=lambda: open_frame(menu_frame))
back_button.pack(side="left", padx=10, pady=5)

# Mode toggle button (top right)
mode_button = tk.Button(navbar_frame, text="Dark Mode", font=("Arial", 12), bg="#FF5722", fg="black", command=toggle_mode)
mode_button.pack(side="right", padx=10, pady=5)

# Title under the navbar
title_label = tk.Label(dictionary_frame, text="Word Meaning and Pronunciation", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# Word entry
label = tk.Label(dictionary_frame, text="Enter a word:", font=("Arial", 12), bg="#f0f0f0")
label.pack(pady=10)

entry = tk.Entry(dictionary_frame, width=30, font=("Arial", 12))
entry.pack(pady=10)

# Create buttons for dictionary options
button_frame = tk.Frame(dictionary_frame, bg="#f0f0f0")
button_frame.pack(pady=10)

info_button = tk.Button(button_frame, text="Get Word Info", font=("Arial", 12), bg="#4CAF50", fg="white", width=15, command=get_word_info)
info_button.grid(row=0, column=0, padx=10, pady=10)

pronounce_button = tk.Button(button_frame, text="Pronounce Word", font=("Arial", 12), bg="#2196F3", fg="white", width=15, command=pronounce_word)
pronounce_button.grid(row=0, column=1, padx=10, pady=10)

speak_info_button = tk.Button(button_frame, text="Speak Word Info", font=("Arial", 12), bg="#FF5722", fg="white", width=15, command=speak_word_info)
speak_info_button.grid(row=0, column=2, padx=10, pady=10)

# Create a text area to display the word information
text_area = scrolledtext.ScrolledText(dictionary_frame, wrap=tk.WORD, font=("Arial", 12), width=60, height=10)
text_area.pack(padx=10, pady=10)

# ---------------- Flashcard Frame for "Learn Vocabulary" ----------------
flashcard_frame = tk.Frame(root, bg="#f0f0f0")

# Flashcard title
flashcard_title = tk.Label(flashcard_frame, text="Flashcards: Learn Vocabulary", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
flashcard_title.pack(pady=10)

# Flashcard content
flashcard_text = tk.StringVar()
flashcard_label = tk.Label(flashcard_frame, textvariable=flashcard_text, font=("Arial", 14), bg="#f0f0f0", wraplength=500, justify="left")
flashcard_label.pack(pady=10)

# Flashcard buttons
flashcard_button_frame = tk.Frame(flashcard_frame, bg="#f0f0f0")
flashcard_button_frame.pack(pady=20)

pronounce_flashcard_button = tk.Button(flashcard_button_frame, text="Pronounce Word", font=("Arial", 12), bg="#4CAF50", fg="white", command=pronounce_flashcard_word)
pronounce_flashcard_button.grid(row=0, column=0, padx=10, pady=10)

next_flashcard_button = tk.Button(flashcard_button_frame, text="Next Word", font=("Arial", 12), bg="#2196F3", fg="white", command=next_flashcard)
next_flashcard_button.grid(row=0, column=1, padx=10, pady=10)

# ---------------- Learning English Frame ----------------
learning_english_frame = tk.Frame(root, bg="#f0f0f0")

navbar_frame = tk.Frame(learning_english_frame, bg="#FF5722", height=40)
navbar_frame.pack(fill="x", side="top")

back_button = tk.Button(navbar_frame, text="Back to Menu", font=("Arial", 12), bg="#FF5722", fg="white", command=lambda: open_frame(menu_frame))
back_button.pack(side="left", padx=10, pady=5)

# Title under the navbar
learning_label = tk.Label(learning_english_frame, text="Learning English", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
learning_label.pack(pady=20)

# Vocabulary learning option
learn_vocabulary_button = tk.Button(learning_english_frame, text="Learn Vocabulary", font=("Arial", 14), bg="#4CAF50", fg="white", width=20, command=learn_vocabulary)
learn_vocabulary_button.pack(pady=10)

# Placeholder for other options such as Grammar Lessons, Listening, and Speaking
placeholder_label = tk.Label(learning_english_frame, text="More features coming soon...", font=("Arial", 12), bg="#f0f0f0")
placeholder_label.pack(pady=10)

# ---------------- Utility Functions ----------------

def open_frame(frame):
    """Helper function to switch between frames."""
    dictionary_frame.pack_forget()
    learning_english_frame.pack_forget()
    flashcard_frame.pack_forget()
    menu_frame.pack_forget()

    frame.pack(fill="both", expand=True)

# Start with the main menu
open_frame(menu_frame)

# Start the Tkinter event loop
root.mainloop()