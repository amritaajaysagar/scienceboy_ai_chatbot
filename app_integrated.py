from flask import Flask, request, jsonify, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import json
import logging
from science_quiz2 import run_quiz , load_question_bank # Import the function from science_quiz.py
import nltk
# Download NLTK resources if you haven't already
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

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
    return render_template("chat_integrated.html")

@app.route("/greet", methods=["POST"])
def greet():
    name = request.json.get("name")
    age = request.json.get("age")
    if not name or not age:
        return jsonify({"error": "Name and age are required."}), 400
    user_data = {"name": name, "age": int(age)}
    save_user_data(user_data)
    return jsonify({"message": f"Hello {name}! We've saved your age as {age}."})

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
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Something went wrong on the server"}), 500





""" @app.route('/quiz', methods=['POST'])
def quiz():
    try:
        # Get the user data (age) from the saved file
        with open("user_data.json") as f:
            user_data = json.load(f)
        
        age = user_data["age"]
        
        # Load the question bank and generate the quiz
        question_bank = load_question_bank()

        # Determine difficulty level based on age
        if age <= 10:
            difficulty = "VeryEasy"
        elif 11 <= age <= 15:
            difficulty = "Medium"
        else:
            difficulty = "Difficult"
        
        # If it's the first request (fetching questions)
        if request.json.get("action") == "start":
            # Get the questions for the selected difficulty
            questions = []
            for subject, question_list in question_bank[difficulty].items():
                questions.extend(question_list)

            # Randomly select questions
            selected_questions = random.sample(questions, min(5, len(questions)))

            # Prepare the quiz data to send to the front-end
            quiz_data = []
            for q in selected_questions:
                question_data = {
                    'question': q['question'],
                    'options': q['options'],
                    'correct_answer': q['answer']  # We won't send the correct answer to the user
                }
                quiz_data.append(question_data)

            return jsonify({"action": "start", "questions": quiz_data})

        # If it's the second request (submitting answers)
        elif request.json.get("action") == "submit":
            user_answers = request.json.get("answers")  # Expecting a list of answers from the front-end
            
            # Get the questions again to check answers
            questions = []
            for subject, question_list in question_bank[difficulty].items():
                questions.extend(question_list)

            # Randomly select questions again
            selected_questions = random.sample(questions, min(5, len(questions)))

            score = 0
            feedback = []

            for idx, q in enumerate(selected_questions):
                correct_answer = q['answer']
                user_answer = user_answers[idx].strip().lower()
                
                if user_answer == correct_answer.lower():
                    score += 1
                    feedback.append(f"Question {idx+1}: Correct!")
                else:
                    feedback.append(f"Question {idx+1}: Incorrect! The correct answer was {correct_answer}.")
            
            feedback_message = f"You answered {score} out of {len(selected_questions)} questions correctly."
            
            return jsonify({
                "action": "submit",
                "score": score,
                "feedback": feedback_message,
                "detailed_feedback": feedback
            })

    except Exception as e:
        return jsonify({"error": "Error processing the quiz!"}), 500 """



@app.route('/calculator', methods=['GET'])
def calculator():
    return render_template("calculator.html")

@app.route('/game', methods=['GET'])
def game():
    return render_template("game.html")


@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid JSON format"}), 400
        
        user_message = request.json.get("message")
        feedback_response = request.json.get("feedback")  # Expecting 'good' or 'bad'
        
        if not user_message or feedback_response not in ['good', 'bad']:
            return jsonify({"error": "Invalid feedback data"}), 400
        
        # You can save this feedback to a database or a file for further analysis
        with open('feedback_log.txt', 'a') as f:
            f.write(f"User: {user_message} | Feedback: {feedback_response}\n")
        
        return jsonify({"message": "Feedback received, thank you!"})
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Something went wrong on the server"}), 500

@app.route("/hawking", methods=["POST"])
def hawking_chat():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Text is required for voice synthesis."}), 400
    audio_file = synthesize_voice(text)
    return jsonify({"audio": audio_file})

@app.route("/solve_image", methods=["POST"])
def solve_image():
    if "image" not in request.files:
        return jsonify({"error": "Image file is required."}), 400

    image_file = request.files["image"]
    image_path = f"static/{image_file.filename}"
    image_file.save(image_path)
    text = extract_text_from_image(image_path)
    return jsonify({"extracted_text": text})

@app.route("/latex", methods=["POST"])
def latex_route():
    equation = request.json.get("equation")
    if not equation:
        return jsonify({"error": "Equation is required for LaTeX conversion."}), 400
    latex_code = convert_to_latex(equation)
    return jsonify({"latex": latex_code})


@app.route("/quiz", methods=["POST"])
def quiz():
    user_data = get_user_data()
    if not user_data:
        return jsonify({"error": "User data not found. Please provide your name and age first."}), 400

    age = user_data.get("age")
    action = request.json.get("action")

    if action == "start":
        questions = generate_quiz(age)
        return jsonify({"questions": questions})
    elif action == "submit":
        user_answers = request.json.get("answers")
        if not user_answers:
            return jsonify({"error": "Answers are required to evaluate the quiz."}), 400

        score, feedback = evaluate_answers(age, user_answers)
        return jsonify({"score": score, "feedback": feedback})
    else:
        return jsonify({"error": "Invalid action."}), 400

if __name__ == "__main__":
    app.run(debug=True)
