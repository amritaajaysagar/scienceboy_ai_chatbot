from flask import Flask, request, jsonify, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import json
import logging
import random
from science_quiz2 import run_quiz  # Import the function from science_quiz.py

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a new chatbot instance
chatbot = ChatBot(
    'MyChatBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
    ]
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

@app.route('/start_chat', methods=['POST'])
def start_chat():
    try:
        # Get name and age from user input in the chat
        name = request.json.get("name")
        age = request.json.get("age")
        
        if not name or not age:
            return jsonify({"error": "Name and age are required."}), 400
        
        user_data = {
            "name": name,
            "age": age,
            "score": 0
        }
        
        # Save user data to user_data.json
        with open("user_data.json", "w") as f:
            json.dump(user_data, f)
        
        # Respond with a greeting and options
        greeting_message = f"Hello {name}, nice to meet you! How can I assist you today?"
        options = ["Let's Just Chat", "Take a Science Quiz", "Scientific Calculator", "Let's Plot a Function", "Let's Play a Game"]

        return jsonify({
            "message": greeting_message,
            "options": options
        })
    
    except Exception as e:
        return jsonify({"error": "Something went wrong!"}), 500

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
        return jsonify({"error": "Something went wrong on the server"}), 500

@app.route('/quiz', methods=['POST'])
def quiz():
    try:
        # Get the user data (age) from the saved file
        with open("user_data.json") as f:
            user_data = json.load(f)
        
        age = user_data["age"]
        
        # Run the quiz function from science_quiz.py and return the result
        feedback_message = run_quiz(age)
        
        return jsonify({"message": feedback_message})
    
    except Exception as e:
        return jsonify({"error": "Error starting the quiz!"}), 500

@app.route('/calculator', methods=['GET'])
def calculator():
    return render_template("calculator.html")

@app.route('/game', methods=['GET'])
def game():
    return render_template("game.html")

if __name__ == "__main__":
    app.run(debug=True)
