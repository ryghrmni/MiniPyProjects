import tkinter as tk
from tkinter import messagebox
import pyttsx3
import speech_recognition as sr
import os
import wave

def text_to_speech():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Input Error", "Please enter some text.")
        return
    
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', engine.getProperty('voices')[0].id)
    
    # Save the speech to a file
    file_path = "output.wav"
    engine.save_to_file(text, file_path)
    engine.runAndWait()

    messagebox.showinfo("Success", f"Text-to-Speech conversion completed. File saved as {file_path}.")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            status_label.config(text="Recognizing...")
            text = recognizer.recognize_google(audio)
            text_output.config(state=tk.NORMAL)
            text_output.delete("1.0", tk.END)
            text_output.insert(tk.END, text)
            text_output.config(state=tk.DISABLED)
            status_label.config(text="Recognition completed.")
        except sr.UnknownValueError:
            status_label.config(text="Could not understand the audio.")
        except sr.RequestError as e:
            status_label.config(text=f"Request error: {e}")

def on_option_change(event):
    option = option_var.get()
    if option == "Text to Speech":
        text_input_label.grid(row=1, column=0, padx=10, pady=10)
        text_input.grid(row=1, column=1, padx=10, pady=10)
        text_to_speech_button.grid(row=2, columnspan=2, padx=10, pady=10)
        speech_to_text_button.grid_forget()
        text_output_label.grid_forget()
        text_output.grid_forget()
    elif option == "Speech to Text":
        text_input_label.grid_forget()
        text_input.grid_forget()
        text_to_speech_button.grid_forget()
        speech_to_text_button.grid(row=2, columnspan=2, padx=10, pady=10)
        text_output_label.grid(row=3, column=0, padx=10, pady=10)
        text_output.grid(row=3, column=1, padx=10, pady=10)

# Create the main window
root = tk.Tk()
root.title("Speech and Text Converter")

# Option selection
option_var = tk.StringVar(value="Text to Speech")
option_menu = tk.OptionMenu(root, option_var, "Text to Speech", "Speech to Text", command=on_option_change)
option_menu.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Text to Speech widgets
text_input_label = tk.Label(root, text="Enter text:")
text_input = tk.Text(root, height=5, width=40)
text_to_speech_button = tk.Button(root, text="Convert to Speech", command=text_to_speech)

# Speech to Text widgets
speech_to_text_button = tk.Button(root, text="Convert Speech to Text", command=speech_to_text)
text_output_label = tk.Label(root, text="Recognized text:")
text_output = tk.Text(root, height=5, width=40, state=tk.DISABLED)

# Status label
status_label = tk.Label(root, text="Select an option to get started")

# Start with Text to Speech option
on_option_change(None)

# Run the application
root.mainloop()
