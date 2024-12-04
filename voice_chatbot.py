from flask import Flask, request, jsonify, render_template
from gtts import gTTS
import os
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import tempfile
import json
app = Flask(__name__)

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

# Route to render the voice chat page
@app.route("/")
def index():
    return render_template("voice_chat.html")

# Route for voice chat
@app.route("/voice_chat", methods=["POST"])
def voice_chat():
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
    return temp_audio


if __name__ == "__main__":
    app.run(debug=True)
