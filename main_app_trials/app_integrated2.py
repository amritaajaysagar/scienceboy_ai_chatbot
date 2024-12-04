from flask import Flask, request, jsonify, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from science import get_weather  # Science-related functions
import os
import time

#from calculator import calculate  # Calculator function
from hawking_chat import hawking_voice  # Hawking TTS
from ocr_solver import extract_text_from_image  # OCR Solver
from latex_converter import convert_to_latex  # LaTeX Conversion

import json
import random
import logging
import re
import pyttsx3
import speech_recognition as sr
from flask import Flask, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# User data storage
USER_DATA_FILE = "user_data.json"


""" def save_user_data(data):
    
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f)


def get_user_data():
    
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {} """


# Create a chatbot instance
chatbot = ChatBot(
    "MyChatBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
    ],
)

# Train the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

# Load custom training data
with open("custom_corpus.json") as f:
    custom_data = json.load(f)
    custom_conversations = custom_data["conversations"]
    structured_data = []
    for convo in custom_conversations:
        user, bot = convo
        structured_data.extend([user.strip(), bot.strip()])

    # Train using ListTrainer
    custom_trainer = ListTrainer(chatbot)
    custom_trainer.train(structured_data)

print("Chatbot trained successfully.")


@app.route("/")
def index():
    return render_template("chat_integrated2.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message").strip().lower()
        response = ""
        # Call the get_user_data function to handle greetings and profile creation
        #response = get_user_data(user_message)


        # If the response is a greeting, return it immediately
        """ if response:
            return jsonify({"bot_message": response}) """


        # Check for specific commands in the user's message
        if "hey bot" in user_message:
            response = get_user_data(user_message)
        
        elif "calculator" in user_message:
            response = calculator()
        elif "hawking" in user_message:
            response = "What would you like Stephen Hawking to say?"
        elif "solve image" in user_message:
            response = "Please upload an image containing text or equations."
        elif re.search(r"[0-9\+\-\*/\^=\(\)]", user_message):  # Check for mathematical symbols/numbers
            response = convert_to_latex(user_message)
        elif "weather" in user_message:
            response = get_weather()
        elif "voice chat" in user_message:
            response = redirect(url_for("voice_chat"))
  
        else:
            # Default response from chatbot
            response = chatbot.get_response(user_message)
        # Convert the response to speech
        # Convert the response to speech if it's not a redirect
        """ if isinstance(response, str):  # Ensure response is a string before processing
            audio_file = synthesize_voice(response)
            return jsonify({"bot_message": response, "audio": audio_file}) """
        
        # Return the response if it's a redirect
        #return response

        # Log user interaction
        logging.info(f"User: {user_message} | Bot: {response}")
        return jsonify({"bot_message": str(response)})

    except Exception as e:
        logging.error(f"Error during chat processing: {e}")
        return jsonify({"error": "Something went wrong."}), 500



@app.route('/calculator', methods=['GET'])
def calculator():
    return render_template("calculator.html")

@app.route('/game', methods=['GET'])
def game():
    return render_template("game.html")


""" @app.route("/hawking", methods=["POST"])
def hawking_chat():
   
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Text is required for voice synthesis."}), 400
    audio_file = hawking_voice(text)
    return jsonify({"audio":f"/static/{audio_file}"}) """

@app.route("/hawking", methods=["POST"])
def hawking_chat():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Text is required for voice synthesis."}), 400
    audio_file = hawking_voice(text)  # Returns "response.mp3"
    return jsonify({"audio": audio_file})  # Prepend the dynamic route
 
@app.route('/response.mp3', methods=['GET'])
def serve_response():
    return send_file('response.mp3', mimetype='audio/mpeg')

""" @app.route("/hawking", methods=["POST"])
def hawking_chat():
    
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Text is required for voice synthesis."}), 400
    
    # Generate a unique filename
    audio_file = f"response_{int(time.time())}.mp3"
    audio_path = os.path.join('static/audio', audio_file)  # Ensure this directory exists
    hawking_voice(text, audio_path)  # Update this function to accept the path """
    
    #return jsonify({"audio": f"/static/audio/{audio_file}"})  # Serve from static
@app.route("/solve_image", methods=["POST"])
def solve_image():
    """Handle image-based text extraction."""
    if "image" not in request.files:
        return jsonify({"error": "Image file is required."}), 400

    image_file = request.files["image"]
    image_path = f"static/{image_file.filename}"
    image_file.save(image_path)
    extracted_text = extract_text_from_image(image_path)
    return jsonify({"extracted_text": extracted_text})


@app.route("/latex", methods=["POST"])
def latex_route():
    #equation = request.json.get("equation")
    user_message = request.json.get("message").strip().lower()
    equation=user_message
    if not equation:
        return jsonify({"error": "Equation is required for LaTeX conversion."}), 400

    try:
        # Convert to LaTeX using the fixed function
        latex_code = convert_to_latex(user_message)
        return jsonify({"latex": latex_code})
    except Exception as e:
        logging.error(f"Error in LaTeX conversion: {e}")
        return jsonify({"error": f"Error converting equation: {e}"}), 

@app.route("/start_voice_chat", methods=["GET"])
def start_voice_chat():
    return redirect(url_for("voice_chat"))

# Route for voice chat
@app.route("/voice_chat", methods=["GET", "POST"])
def voice_chat():
    if request.method == "POST":
        # Capture audio from the microphone
        with sr.Microphone() as source:
            print("Say something...")
            audio = recognizer.listen(source)

            try:
                # Recognize speech using Google Speech Recognition
                user_message = recognizer.recognize_google(audio)
                print(f"User said: {user_message}")

                # Process the recognized text with chatbot
                response = "You said: " + user_message  # Default response

                # Send recognized text to your chatbot here
                response = chatbot.get_response(user_message)

                # Convert chatbot's response to speech
                audio_file = synthesize_voice(response)

                return jsonify({"audio": audio_file})

            except sr.UnknownValueError:
                return jsonify({"error": "Sorry, I could not understand your speech."}), 400
            except sr.RequestError:
                return jsonify({"error": "Sorry, there was an issue with the speech service."}), 500

    # If GET request, simply return the voice chat page
    return render_template("voice_chat.html")






if __name__ == "__main__":
    app.run(debug=True)
