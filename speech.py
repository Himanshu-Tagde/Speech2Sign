from flask import Flask, render_template, request, url_for
import os

app = Flask(__name__)

# Paths for ASL and ISL image folders (static folder is handled by Flask automatically)
ASL_PATH = "E:\spacece\Automatic-Indian-Sign-Language-Translator-ISL-master\Automatic-Indian-Sign-Language-Translator-ISL-master\static\ASL"
ISL_PATH = "E:\spacece\Automatic-Indian-Sign-Language-Translator-ISL-master\Automatic-Indian-Sign-Language-Translator-ISL-master\static\ISL"

# Function to translate text into sign language images
def get_sign_language_images(text, language):
    folder_path = ASL_PATH if language == "ASL" else ISL_PATH
    images = []
    for letter in text.lower():
        if letter.isalpha() or letter.isdigit():
            image_filename = f"{letter}.jpg"
            image_path = os.path.join(folder_path, image_filename)
            
            if os.path.exists(image_path):
                image_url = url_for('static', filename=f"{language.upper()}/{image_filename}")
                images.append(image_url)
            else:
                images.append(url_for('static', filename="placeholder.jpg"))  # Ensure you have a placeholder image in the static folder
    return images

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    # Get input values from the user
    text_input = request.form.get("text_input")
    speech_input = request.form.get("speech_input")
    language_choice = request.form.get("language")

    # Use text input if available, otherwise use speech input
    input_text = text_input if text_input else speech_input

    if input_text:
        # Get corresponding sign language images
        images = get_sign_language_images(input_text, language_choice)
        return render_template('index.html', images=images, input_text=input_text, language=language_choice)

    return render_template('index.html', images=None)

if __name__ == '__main__':
    app.run(debug=True)
