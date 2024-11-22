from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from language_selection import get_language_options, get_language_by_code
from greetings import load_greetings, load_user_data, greet_and_create_profile, save_user_data
from science_answers import answer_science_question
from science_quiz import run_quiz

# Download NLTK resources if you haven't already
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Load responses from JSON file
with open('responses.json') as f:
    responses = json.load(f)

# Load question bank from JSON file
with open('question_bank.json') as f:
    question_bank = json.load(f)

# Load user data from JSON file (optional)
user_data = {}
try:
    with open('user_data.json') as f:
        user_data = json.load(f)
except FileNotFoundError:
    pass

@app.route("/")
def index():
    language = user_data.get('language', 'en')
    greeting = load_greetings(language)
    return render_template("chat.html", greeting=greeting, language_options=get_language_options())

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message").lower()
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    tokens = word_tokenize(user_message)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    if 'name' not in user_data:
        greeting = load_greetings(user_data.get('language', 'en'))
        response = f"{greeting} What's your name?"
        user_data['name'] = user_message
    elif 'age' not in user_data:
        response = f"Nice to meet you, {user_data['name']}! How old are you?"
        user_data['age'] = int(user_message)
    elif 'selected_option' not in user_data:
        response = f"Hi {user_data['name']}, what would you like to do today? 1. Let's Chat, 2. Take a Science Quiz, or 3. Use the Scientific Calculator?"
        user_data['selected_option'] = user_message
    else:
        if user_data['selected_option'] == '1':
            response = answer_science_question(user_message)
        elif user_data['selected_option'] == '2':
            try:
                num_questions = 5
                score_data = run_quiz(user_data['age'], num_questions)
                response = f"You scored {score_data['score']} out of {score_data['total_questions']}! {score_data['feedback']}"
                user_data['quiz_score'] = score_data['score']
            except Exception as e:
                response = f"An error occurred while running the quiz: {str(e )}"
        elif user_data['selected_option'] == '3':
            return redirect("http://localhost:5001/calculator")  # Redirect to the calculator app

    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

    return jsonify({"bot_message": response})

@app.route("/set_language/<language_code>")
def set_language(language_code):
    user_data['language'] = language_code
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

if __name__ == "__main__":
    app.run(debug=True)