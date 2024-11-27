from flask import Flask, request, jsonify
from greet_and_user_data import greet_user, save_user_data
from science_chat import get_science_response
from quiz import get_questions_by_age, calculate_score
from calculator import calculate
from voice_chat import synthesize_voice
from image_solver import solve_equation_from_image

app = Flask(__name__)

@app.route("/greet", methods=["POST"])
def greet():
    data = request.json
    name = data.get("name")
    age = data.get("age")
    if name and age:
        return jsonify({"response": save_user_data(name, age)})
    return jsonify({"response": greet_user()})

@app.route("/science", methods=["POST"])
def science():
    query = request.json.get("query")
    response, link = get_science_response(query)
    return jsonify({"response": response, "link": link})

@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.json
    age = data.get("age")
    answers = data.get("answers", [])
    questions = get_questions_by_age(age)
    correct_answers = [q["answer"] for q in questions]
    score, feedback = calculate_score(answers, correct_answers)
    return jsonify({"score": score, "feedback": feedback})

@app.route("/calculator", methods=["POST"])
def calculator():
    expression = request.json.get("expression")
    return jsonify({"response": calculate(expression)})

@app.route("/voice", methods=["POST"])
def voice():
    text = request.json.get("text")
    audio_path = synthesize_voice(text)
    return jsonify({"audio": audio_path})

@app.route("/image", methods=["POST"])
def image():
    image_file = request.files["image"]
    if image_file:
        image_path = f"./uploads/{image_file.filename}"
        image_file.save(image_path)
        latex = solve_equation_from_image(image_path)
        return jsonify({"latex": latex})
    return jsonify({"error": "No image uploaded."})

if __name__ == "__main__":
    app.run(debug=True)
