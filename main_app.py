from flask import Flask, request, jsonify, render_template
import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from language_selection import get_language_options, get_language_by_code
from greetings import get_greeting
from age_group import get_age_group_options, get_age_group_by_code
from profile import create_profile, get_profiles, is_profile_full
from science_answer import answer_science_question
from science_quiz import get_topics, get_random_questions, grade_quiz, get_feedback

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
    # Check if language is set in user data
    language = user_data.get('language', 'en')
    greeting = get_greeting(language)
    return render_template("chat.html", greeting=greeting, language_options=get_language_options())


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message").lower()
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Tokenize the user message
    tokens = word_tokenize(user_message)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Handle different conversation stages based on user_data
    if 'name' not in user_data:
        # Greet user and ask for name
        greeting = get_greeting(user_data.get('language', 'en'))
        response = f"{greeting} What's your name?"
    elif 'age' not in user_data:
        # Ask for age
        response = f"Nice to meet you, {user_data['name']}! How old are you?"
    elif 'selected_option' not in user_data:
        # Ask for chat or quiz
        response = f"Hi {user_data['name']}, what would you like to do today? 1. Let's Chat or 2. Take a Science Quiz?"
    else:
        # Handle chat or quiz based on selection

        if user_data['selected_option'] == '1':
            # Use science_answer.py to answer questions
            response = answer_science_question(user_message)
            # Extend answer retrieval with NASA website (example)
            if "NASA" in user_message:
                response += f"\nYou can also visit NASA's website for more information: https://www.nasa.gov/"
        elif user_data['selected_option'] == '2':
            # Use science_quiz.py to handle quiz
            questions = get_random_questions(question_bank, 5)
            score, user_answers = grade_quiz(questions, user_message)
            feedback = get_feedback(user_answers, question_bank)
            response = f"You scored {score} out of 5! {feedback}"
            # Update user data with quiz score (optional)
            user_data['quiz_score'] = score

    # Save user data after each interaction
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

    return jsonify({"bot_message": response})


@app.route("/set_language/<language_code>")
def set_language(language_code):
    # Update user data with selected language
    user_data['language'] = language_code
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)