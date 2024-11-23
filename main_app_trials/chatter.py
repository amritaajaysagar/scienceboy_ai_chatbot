from flask import Flask, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources if you haven't already
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Create a new chatbot instance
chatbot = ChatBot(
    'MyChatBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ]
)

# Train the chatbot with the English corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

""" @app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    bot_response = chatbot.get_response(user_message)
    return jsonify({"bot_message": str(bot_response)})

 """


@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Check if the request contains JSON data
        if not request.is_json:
            return jsonify({"error": "Invalid JSON format"}), 400
        
        # Get the user message from JSON
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Get chatbot's response
        bot_response = chatbot.get_response(user_message)
        return jsonify({"bot_message": str(bot_response)})
    
    except Exception as e:
        # Print the full traceback for debugging purposes
        import traceback
        traceback.print_exc()

        # Return a generic error message to the client
        return jsonify({"error": "Something went wrong on the server"}), 500

if __name__ == "__main__":
    app.run(debug=True)