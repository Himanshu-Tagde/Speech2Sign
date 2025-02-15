import os
from PIL import Image
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import easygui
import string
import speech_recognition as sr
import threading  


ASL = "E:\spacece\Automatic-Indian-Sign-Language-Translator-ISL-master\Automatic-Indian-Sign-Language-Translator-ISL-master\letters_ASL"
ISL = "E:\spacece\Automatic-Indian-Sign-Language-Translator-ISL-master\Automatic-Indian-Sign-Language-Translator-ISL-master\letters_ISL"

letters_folder = ""  # Will be set based on the user's choice


arr = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

# Global variable to store recognized speech text
recognized_text = ""

# Function to handle text input
def handle_text_input(text):
    if text:
        
        for char in text.lower():
            if char in string.ascii_lowercase:
                # Check for each letter
                image_address = f'{letters_folder}/{char}.jpg'
                if os.path.exists(image_address):
                    image = Image.open(image_address)
                    image_numpy_format = np.asarray(image)
                    plt.imshow(image_numpy_format)
                    plt.title(f"Image for '{char}'")
                    plt.show(block=False)
                    plt.pause(1)  # Pause to show image before closing
                    plt.close()
                else:
                    print(f"No image found for '{char}'")
            else:
                print(f"Character '{char}' is not a valid input.")

# Function to perform speech recognition asynchronously
def speech_to_text():
    def listen_and_recognize():
        global recognized_text
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening... Speak now!")
            audio = r.listen(source)
            try:
                recognized_text = r.recognize_google(audio)
                print(f"Recognized Text: {recognized_text}")
                easygui.msgbox(f"Recognized Text: {recognized_text}", title="Speech to Text")
                show_in_sign_language_button()  # Show button to show recognized text in sign language
            except sr.UnknownValueError:
                easygui.msgbox("Sorry, I could not understand the audio.", title="Error")
            except sr.RequestError:
                easygui.msgbox("Could not request results from the speech recognition service.", title="Error")

    
    threading.Thread(target=listen_and_recognize, daemon=True).start()

# Function to display "Show in Sign Language" button after speech to text
def show_in_sign_language_button():
   
    if recognized_text:
        response = easygui.buttonbox("Do you want to see this in Sign Language?", choices=["Show in Sign Language", "Cancel"])
        if response == "Show in Sign Language":
            handle_text_input(recognized_text)  

# Function to set the language (ASL or ISL)
def set_language_choice():
    global letters_folder
    response = easygui.buttonbox("Choose a Sign Language:", choices=["ASL", "ISL"])
    
    if response == "ASL":
        letters_folder = ASL
        print("ASL folder selected.")
    elif response == "ISL":
        letters_folder = ISL
        print("ISL folder selected.")
    else:
        easygui.msgbox("No valid choice made. Exiting.")
        exit()

# Main GUI loop
set_language_choice()  # Ask user to choose language before proceeding

while True:
    choices = ["Text Input", "Speech to Text", "Exit"]
    reply = easygui.buttonbox("Choose an action:", choices=choices)

    if reply == "Text Input":
        text_input = easygui.enterbox("Enter the text for which you want images :", "Text Input")
        handle_text_input(text_input)  # Pass the entered text to the function
    elif reply == "Speech to Text":
        speech_to_text()  # Start speech recognition
    elif reply == "Exit":
        break
