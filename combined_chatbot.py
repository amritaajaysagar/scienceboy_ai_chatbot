from flask import Flask, request, jsonify, render_template, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer  
from hawking_chat import hawking_voice
import requests
import json
import logging
import re
import pyttsx3
import speech_recognition as sr
from flask import Flask, request, jsonify, render_template
from gtts import gTTS
import os
import tempfile
from latex_converter import convert_to_latex 
from googletrans import Translator
from branch_bound import branch_and_bound
import numpy as np
from scipy.optimize import linprog

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
# Create and train the chatbot
chatbot = ChatBot(
    "MyChatBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
    ],
)

# Train the chatbot with ChatterBot corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")
#trainer.train("chatterbot.corpus.spanish")



# Load custom training data
with open("custom_corpus.json") as f:
    custom_data = json.load(f)
    custom_conversations = custom_data["conversations"]
    structured_data = []
    for convo in custom_conversations:
        user, bot = convo
        structured_data.extend([user.strip(), bot.strip()])

    custom_trainer = ListTrainer(chatbot)
    custom_trainer.train(structured_data)

print("Chatbot trained successfully.")

@app.route("/")
def index():
    return render_template("combined.html")

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
        elif "quiz" in user_message:
            response = render_template("quiz.html")
        elif "voice chat" in user_message:
            return redirect(url_for("voice_chat"))
        elif re.search(r"[0-9\+\-\*/\^=\(\)]", user_message):  # Check for mathematical symbols/numbers
            response = latex_route()
        elif "weather" in user_message:
            response = get_weather()
        elif "hawking" in user_message:
            response = hawking()   
        elif "track" in user_message:
            response = iss_location()
        elif "game" in user_message:
            response = game()
        
        elif "what can you do" in user_message:
            response = "Many things, would you like to know were the International space station is at right now?"
        elif "plot" in user_message:
            response = plot_function()
        elif "translate this to" in user_message and ":" in user_message:
            response = translate(user_message)
        elif "astronomy picture" in user_message or "apod" in user_message:
            apod = get_apod()
            if "error" in apod:
                response = apod["error"]
            else:
                response = f"Here is today's Astronomy Picture of the Day: {apod['title']}.\n{apod['explanation']}\nImage: {apod['image_url']}"
        elif "solve" in user_message:
            response=solve()
          

        
        
        else:
            # Default response from chatbot
            response = chatbot.get_response(user_message)

        logging.info(f"User: {user_message} | Bot: {response}")
        return jsonify({"bot_message": str(response), "status": "success"})
    except Exception as e:
        logging.error(f"Error during chat processing: {e}")
        return jsonify({"error": "Something went wrong.", "status": "failed"}), 500


@app.route('/calculator', methods=['GET'])
def calculator():
    return render_template("calculator.html")

@app.route('/quiz', methods=['GET'])
def quiz():
    return render_template("quiz.html")

@app.route('/game', methods=['GET'])
def game():
    return render_template("game.html")


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
    api_key = "zi0e2jfdJjCwSAZIFATxvxOQf1hB84DWkEv9Sv00"  
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

@app.route("/voice_chat", methods=["GET", "POST"])
def voice_chat():
    
    if request.method == "GET":
        # Render the voice chat page (template) when the GET request is made
        return render_template("voice_chat.html")

    if request.method == "POST":
        # Get the user message from the frontend
        user_message = request.json.get("message")

        if user_message:
            print(f"User said: {user_message}")
            
            # Process the user's message with the chatbot
            chatbot_response = chatbot.get_response(user_message)
            print(f"Bot response: {chatbot_response}")

            # Convert the chatbot's response to speech
            audio_file_path = synthesize_voice(str(chatbot_response))

            return jsonify({"bot_message": str(chatbot_response), "audio": audio_file_path})

    return jsonify({"error": "No message received"}), 400

# Function to convert text to speech using gTTS
def synthesize_voice(text):
    tts = gTTS(text=text, lang='en')
    # Save audio file temporarily
    temp_audio = tempfile.mktemp(suffix=".mp3", dir="static/")
    tts.save(temp_audio)
    return 

@app.route("/latex", methods=["POST"])
def latex_route():
    user_message = request.json.get("message").strip().lower()
    equation = user_message
    if not equation:
        return jsonify({"error": "Ofcourse, What is the expression."}), 400

    try:
        # Convert the equation to LaTeX format
        latex_code = convert_to_latex(equation)
        return jsonify({"latex": latex_code})
    except Exception as e:
        logging.error(f"Error in LaTeX conversion: {e}")
        return jsonify({"error": f"Error converting equation: {e}"}), 500

def hawking(user_message):
    text = user_message
    audio_file = hawking_voice(text)
    return jsonify({"audio": audio_file})

API_KEY = "5bd569ef15994e94db0132c4cf485649" 
CITY = 'Kamloops,CA' 
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

@app.route('/weather', methods=['GET'])
def get_weather():
    try:
        API_KEY = "5bd569ef15994e94db0132c4cf485649" 
        CITY = 'Kamloops,CA' 
        BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
        # Make a request to the OpenWeatherMap API
        response = requests.get(f"{BASE_URL}q={CITY}&appid={API_KEY}&units=metric")  # Use metric for Celsius
        data = response.json()

        # Check if the API call was successful
        if data["cod"] == "404":
            return jsonify({"error": "City not found"}), 404

        # Extracting weather data
        weather_data = {
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "windSpeed": data["wind"]["speed"]
        }

        # Return weather data as JSON
        return jsonify(weather=weather_data)

    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the API call
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/translate', methods=['POST'])
def translate():
    try:
        # Get user input from the POST request
        user_input = request.json.get("message", "").strip().lower()

        # Check if the input matches the expected format
        if "translate this to" in user_input and ":" in user_input:
            # Parse the input
            _, language_and_text = user_input.split("to", 1)
            target_language, text_to_translate = language_and_text.split(":", 1)

            # Clean up extracted parts
            target_language = target_language.strip()
            text_to_translate = text_to_translate.strip()

            # Validate extracted parts
            if not target_language or not text_to_translate:
                return jsonify({"bot_message": "Invalid input. Please provide both language and text."})

            # Perform translation using Google Translate
            translator = Translator()
            translated = translator.translate(text_to_translate, dest=target_language).text

            return jsonify({"bot_message": f"The translation is: {translated}"})
        else:
            # Handle invalid formats
            return jsonify({"bot_message": "Invalid format. Use: translate this to [language]: [text]"})
    except Exception as e:
        # Log the error and respond with an error message
        return jsonify({"bot_message": f"An error occurred during translation: {str(e)}"})

@app.route('/solve', methods=['POST'])
def solve():
    try:
        # Extract the input after "solve"
        params = user_message.split("solve")[1].strip()

        # Normalize to JSON-compatible format
        params = (
            params.replace("c:", '"c":')
                .replace("A:", '"A_eq":')
                .replace("b:", '"b_eq":')
                .replace("and", ",")
        )
        print("Normalized params:", params)
        # Parse the string as JSON
        data = json.loads(params)

        # Extract parameters
        c = data['c']  # Objective function coefficients
        A_eq = data['A_eq']  # Equality constraint coefficients
        b_eq = data['b_eq']  # Right-hand side values
        bounds = [(0, None)] * len(c)  # Default bounds for x >= 0

        # Solve using Branch-and-Bound
        result = branch_and_bound(c, A_eq, b_eq, bounds, maximize=True)

        # Prepare response
        if 'solution' in result:
            branch_details = "\n".join([
                f"Node {branch['node']}: "
                f"x = {branch.get('x', 'Infeasible')}, "
                f"Objective = {branch.get('objective', 'N/A')}, "
                f"Bounds = {branch.get('bounds', 'N/A')}"
                for branch in result['branches']
            ])
            response = (
                f"Optimal Solution: {result['solution']}, Objective Value: {result['objective_value']}\n\n"
                f"Branch Details:\n{branch_details}"
            )
        else:
            response = f"Problem Status: {result['status']}"

    except json.JSONDecodeError:
        response = (
            "Error processing your input. Please provide a valid format like:\n"
            "solve c:[1,2] A:[[-2,7],[6,2]] and b:[14,27]"
        )
    except Exception as e:
        response = f"Error processing the input: {str(e)}"

    return jsonify({"bot_message": response})



if __name__ == "__main__":
    app.run(debug=True)
