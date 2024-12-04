from flask import Flask, request, jsonify, render_template, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer  
from science import get_weather
import requests
import json
import logging
import re
import pyttsx3
import speech_recognition as sr

app = Flask(__name__)

# In-memory user data (this can be replaced with a more permanent storage solution like a database)
user_data = {}
# Load the responses from the responses.json file
def load_responses():
    with open('responses.json') as f:
        return json.load(f)

responses = load_responses()

def get_response(intent):
    if intent in responses:
        # Randomly pick a response from the list
        import random
        return random.choice(responses[intent])
    else:
        return responses["default"]

intents = {
    "greetings": responses["greetings"],
    "farewells": responses["farewells"],
    "how_are_you": responses["how_are_you"],
    "default": responses["default"]
}


@app.route("/")
def index():
    return render_template("intend_based.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message").strip().lower()
        response = ""

        # Check for specific commands in the user's message
        if "hey bot" in user_message or "hello" in user_message:
            response = get_response("greetings")
        elif "how are you" in user_message:
            response = get_response("how_are_you")
        elif "bye" in user_message or "goodbye" in user_message:
            response = get_response("farewells")
        elif "calculator" in user_message:
            response = calculator()
        elif "voice chat" in user_message:
            return redirect(url_for("voice_chat"))
        #elif re.search(r"[0-9\+\-\*/\^=\(\)]", user_message):  # Check for mathematical symbols/numbers
        #    response = convert_to_latex(user_message)
        elif "weather" in user_message:
            response = get_weather()
        elif "track" in user_message:
            response = iss_location()
        elif "game" in user_message:
            response = game()
        elif "what can you do" in user_message:
            response = "Many things, would you like to know were the International space station is at right now?"
        elif "plot" in user_message:
            response = plot_function()
        elif "astronomy picture" in user_message or "apod" in user_message:
            apod = get_apod()
            if "error" in apod:
                response = apod["error"]
            else:
                response = f"Here is today's Astronomy Picture of the Day: {apod['title']}.\n{apod['explanation']}\nImage: {apod['image_url']}"

        logging.info(f"User: {user_message} | Bot: {response}")
        return jsonify({"bot_message": str(response), "status": "success"})

    except Exception as e:
        logging.error(f"Error during chat processing: {e}")
        return jsonify({"error": "Something went wrong.", "status": "failed"}), 500


@app.route('/calculator', methods=['GET'])
def calculator():
    return render_template("calculator.html")

@app.route('/game', methods=['GET'])
def game():
    return render_template("game.html")


@app.route("/voice_chat", methods=["GET", "POST"])
def voice_chat():
    return render_template("voice_chat.html")

@app.route("/iss_location", methods=["GET"])
def iss_location():
    try:
        # Make a GET request to the ISS API to get the current location of the ISS
        response = requests.get("http://api.open-notify.org/iss-now.json")
        
        # If the response is successful, parse the JSON data
        if response.status_code == 200:
            data = response.json()
            location = data.get("iss_position")
            latitude = location.get("latitude")
            longitude = location.get("longitude")
            timestamp = data.get("timestamp")

            # Return the location and timestamp in the response
            return jsonify({
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": timestamp
            })
        else:
            return jsonify({"error": "Failed to fetch ISS location."}), 400

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
@app.route("/plot_function")
def plot_function():
    return redirect("https://www.geogebra.org/graphing") 




# zi0e2jfdJjCwSAZIFATxvxOQf1hB84DWkEv9Sv00

import requests
@app.route('/get_apod', methods=['GET'])
def get_apod():
    api_key = "zi0e2jfdJjCwSAZIFATxvxOQf1hB84DWkEv9Sv00"  # Replace with your API key from NASA
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        image_url = data.get("url")
        title = data.get("title")
        explanation = data.get("explanation")
        return {"image_url": image_url, "title": title, "explanation": explanation}
    else:
        return {"error": "Failed to fetch APOD"}



if __name__ == "__main__":
    app.run(debug=True)
