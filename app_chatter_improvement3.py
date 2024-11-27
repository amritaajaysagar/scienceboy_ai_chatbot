from flask import Flask, request, jsonify, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import nltk
import json
import logging
from datetime import datetime
import random
import re

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='chatbot_logs.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Create a chatbot instance with additional logic adapters
chatbot = ChatBot(
    'EnhancedChatBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation',
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Help',
            'output_text': 'Sure! How can I assist you today?'
        }
    ],
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    filters=["chatterbot.filters.RepetitiveResponseFilter"]
)

# Train the chatbot with the English corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Load custom training data
with open('custom_corpus.json') as f:
    custom_data = json.load(f)
    custom_conversations = custom_data['conversations']

# Restructure training data for ListTrainer
structured_data = []
for convo in custom_conversations:
    user, bot = convo
    structured_data.extend([user.strip(), bot.strip()])

# Train using ListTrainer
custom_trainer = ListTrainer(chatbot)
custom_trainer.train(structured_data)

# Fallback responses
fallback_responses = [
    "I'm sorry, I didn't quite catch that. Can you rephrase?",
    "Could you please elaborate?",
    "That's an interesting question. Let me look into it for you.",
    "I'm still learning. Could you clarify?"
]

# Function to handle context (basic context memory)
user_context = {}

def update_context(user_id, message):
    """Update user's context based on the message."""
    user_context[user_id] = message

def get_context(user_id):
    """Retrieve the last context for the user."""
    return user_context.get(user_id, "")

# Enhanced response generator
def generate_response(user_message, user_id):
    """Generate a response considering context and fallback logic."""
    context = get_context(user_id)
    if context:
        logging.info(f"Context for {user_id}: {context}")
    
    bot_response = str(chatbot.get_response(user_message))
    # Fallback if the response confidence is low
    if 'I do not know' in bot_response or len(bot_response) < 3:
        bot_response = random.choice(fallback_responses)
    
    update_context(user_id, user_message)
    return bot_response

print("Enhanced Chatbot trained successfully.")

@app.route("/")
def index():
    return render_template("chat.html")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid JSON format"}), 400

        user_data = request.json
        user_message = user_data.get("message")
        user_id = user_data.get("user_id", "anonymous")

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Get chatbot's response
        bot_response = generate_response(user_message, user_id)

        # Log user interaction
        logging.info(f"User {user_id}: {user_message} | Bot: {bot_response} | Confidence: {response.confidence}")

        return jsonify({"bot_message": bot_response})

    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}")
        return jsonify({"error": "Something went wrong on the server"}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid JSON format"}), 400

        feedback_data = request.json
        user_message = feedback_data.get("message")
        feedback_response = feedback_data.get("feedback")  # Expecting 'good' or 'bad'

        if not user_message or feedback_response not in ['good', 'bad']:
            return jsonify({"error": "Invalid feedback data"}), 400

        # Save feedback to a log file
        with open('feedback_log.txt', 'a') as f:
            f.write(f"{datetime.now()} - User Message: {user_message} | Feedback: {feedback_response}\n")

        return jsonify({"message": "Feedback received, thank you!"})

    except Exception as e:
        logging.error(f"Error in /feedback endpoint: {e}")
        return jsonify({"error": "Something went wrong on the server"}), 500


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5001)
