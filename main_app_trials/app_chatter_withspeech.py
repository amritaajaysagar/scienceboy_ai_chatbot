from flask import Flask, request, jsonify, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import nltk
import json
import logging

# Download NLTK resources if you haven't already
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a new chatbot instance
chatbot = ChatBot(
    'MyChatBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=['chatterbot.logic.BestMatch'],
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

print("Chatbot trained successfully.")

@app.route("/")
def index():
    return render_template("chat.html")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid JSON format"}), 400
        
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Get chatbot's response
        bot_response = chatbot.get_response(user_message)
        
        # Log user interaction
        logging.info(f"User: {user_message} | Bot: {bot_response}")
        
        return jsonify({"bot_message": str(bot_response)})
    
    except Exception as e:
        logging.error(f"Error in chat route: {e}")
        return jsonify({"error": "Something went wrong on the server"}), 500

if __name__ == "__main__":
    app.run(debug=True)
