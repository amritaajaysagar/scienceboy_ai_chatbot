from flask import Flask, request, jsonify, render_template
import json
import random

app = Flask(__name__)

# Load questions from the question bank
with open('question_bank.json') as f:
    question_bank = json.load(f)

# Load user data
def load_user_data():
    try:
        with open('user_data.json') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"name": "", "age": 0, "scores": {"easy": 0, "medium": 0, "difficult": 0}}

def save_user_data(user_data):
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message").lower()
    user_data = load_user_data()

    if user_message in ["hi", "hello", "hey"]:
        return jsonify({"bot_message": "Hi there! What's your name?"})

    if user_data["name"] == "":
        user_data["name"] = user_message
        save_user_data(user_data)
        return jsonify({"bot_message": f"Nice to meet you, {user_data['name']}! How old are you?"})

    if user_data["age"] == 0:
        try:
            user_data["age"] = int(user_message)
            save_user_data(user_data)
            difficulty = "easy" if user_data["age"] < 5 else "medium" if user_data["age"] < 18 else "difficult"
            return jsonify({"bot_message": f"Great! You are {user_data['age']} years old. Would you like to: 1. Let's Chat 2. Quiz?"})
        except ValueError:
            return jsonify({"bot_message": "Please enter a valid age."})

    if user_message == "1":
        return jsonify({"bot_message": "Let's chat! Ask me anything about science or type 'bye' to exit."})

    if user_message == "2":
        return start_quiz(user_data)

    return jsonify({"bot_message": "Sorry, I don't understand that."})

def start_quiz(user_data):
    difficulty = "easy" if user_data["age"] < 5 else "medium" if user_data["age"] < 18 else "difficult"
    questions = random.sample(question_bank[difficulty], 5)  # Select 5 random questions
    user_data = load_user_data()
    user_data["scores"][difficulty] = 0  # Initialize score for the selected difficulty
    save_user_data(user_data)

    quiz_questions = []
    for question in questions:
        quiz_questions.append({
            "question": question["question"],
            "options": question["options"],
            "field": question["field"]
        })

    return jsonify({"bot_message": "Here are your quiz questions:", "questions": quiz_questions})

@app.route("/submit_answers", methods=["POST"])
def submit_answers():
    user_data = load_user_data()
    answers = request.json.get("answers")
    score = 0
    feedback = {}

    for question in answers:
        field = question["field"]
        user_answer = question["answer"]
        correct_answer = next(q["answer"] for q in question_bank[question["difficulty"]] if q["question"] == question["question"])

        if user_answer == correct_answer:
            score += 1
            user_data["scores"][question["difficulty"]] += 1
        else:
            feedback[field] = feedback.get(field, 0) + 1

    save_user_data(user_data)

    feedback_message = "You did great!"
    if feedback:
        feedback_message += " However, you might want to work on: " + ", ".join(f"{field} (missed {count})" for field, count in feedback.items())

    return jsonify({"bot_message": f"You scored {score} out of 5. {feedback_message}"})

if __name__ == "__main__":
    app.run(debug=True)