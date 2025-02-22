from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Folder paths to ASL and ISL image datasets
asl_path = "static/ASL"
isl_path = "static/ISL"

# Function to translate text into sign language images
def get_sign_language_images(text, language):
    folder_path = asl_path if language == "ASL" else isl_path
    images = []
    for letter in text.lower():
        if letter.isalpha():
            image_filename = f"{letter}.jpg"
            image_path = os.path.join(folder_path, image_filename)
            images.append(image_path)
    return images

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get input values from the user
        text_input = request.form.get("text_input")
        speech_input = request.form.get("speech_input")
        language_choice = request.form.get("language")

        # Use text input if available, otherwise use speech input
        input_text = text_input if text_input else speech_input

        if input_text:
            # Get corresponding sign language images
            images = get_sign_language_images(input_text, language_choice)
            return render_template("index.html", images=images, input_text=input_text, language=language_choice)

    return render_template("index.html", images=None)

if __name__ == "__main__":
    app.run(debug=True)
