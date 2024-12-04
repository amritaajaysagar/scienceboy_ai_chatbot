from flask import Flask, request, jsonify, render_template
import re
import tempfile
import pyttsx3

app = Flask(__name__)

# Define intents
intents = [
    {
        "intent": "greeting",
        "patterns": ["hello", "hi", "hey", "good morning", "good evening"],
        "responses": ["Hello there!", "Hi! How can I help you?", "Hey! Nice to meet you."],
    },
    {
        "intent": "goodbye",
        "patterns": ["bye", "goodbye", "see you", "take care"],
        "responses": ["Goodbye!", "See you later!", "Take care!"],
    },
    {
        "intent": "thanks",
        "patterns": ["thanks", "thank you", "I appreciate it"],
        "responses": ["You're welcome!", "No problem!", "Anytime!"],
    },
    {
        "intent": "unknown",
        "patterns": [],
        "responses": ["I'm sorry, I don't understand that.", "Can you please rephrase?"],
    },
]

# Helper function to find the best intent match
def get_intent(user_message):
    for intent in intents:
        for pattern in intent["patterns"]:
            # Check if the user message matches the pattern
            if re.search(r'\b' + re.escape(pattern) + r'\b', user_message, re.IGNORECASE):
                return intent
    # Return the "unknown" intent if no match is found
    return next(intent for intent in intents if intent["intent"] == "unknown")

# Function to convert text to speech
def hawking_voice(text):
    engine = pyttsx3.init()
    engine.setProperty("voice", "english+f4")  # Use the Stephen Hawking-like voice

    # Create a temporary file in the static directory
    temp_audio = tempfile.mktemp(suffix=".mp3", dir="static/")

    # Save the audio to the temporary file
    engine.save_to_file(text, temp_audio)
    engine.runAndWait()

    return temp_audio
    

# Route to render the voice chat page
@app.route("/")
def index():
    return render_template("hawking_chat.html")

# Route for voice chat
@app.route("/hawking_chat", methods=["POST"])
def hawking_chat():
    if request.method == "POST":
        # Get the user message from the frontend
        user_message = request.json.get("message")
        if "Hello" in user_message:
            bot_response = "Hello to you too"
            audio_file_path = hawking_voice(bot_response)

            return jsonify({"bot_message": bot_response, "audio": audio_file_path})

    return jsonify({"error": "No message received"}), 400


if __name__ == "__main__":
    app.run(debug=True)
