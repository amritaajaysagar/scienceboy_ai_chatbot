from flask import Flask, render_template, request, jsonify
from chatbot_functions import greet_user, choose_age_group, answer_science_question, create_profile, science_quiz, get_eclipse_info, simulate_physics, calculator, speech_to_text, impersonate_scientist

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/greet', methods=['POST'])
def greet():
    return jsonify(greet_user())

@app.route('/choose_age', methods=['POST'])
def choose_age():
    age_group = request.json.get('age_group')
    return jsonify(choose_age_group(age_group))

@app.route('/ask_question', methods=['POST'])
def ask_question():
    question = request.json.get('question')
    return jsonify(answer_science_question(question))

@app.route('/create_profile', methods=['POST'])
def create_user_profile():
    user_data = request.json
    return jsonify(create_profile(user_data))

@app.route('/quiz', methods=['POST'])
def quiz():
    topic = request.json.get('topic')
    num_questions = request.json.get('num_questions')
    return jsonify(science_quiz(topic, num_questions))

@app.route('/eclipse_info', methods=['GET'])
def eclipse_info():
    return jsonify(get_eclipse_info())

@app.route('/simulate', methods=['POST'])
def simulate():
    topic = request.json.get('topic')
    return jsonify(simulate_physics(topic))

@app.route('/calculator', methods=['POST'])
def calculate():
    expression = request.json.get('expression')
    return jsonify(calculator(expression))

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text_route():
    audio_file = request.files['audio']
    return jsonify(speech_to_text(audio_file))

@app.route('/impersonate', methods=['POST'])
def impersonate():
    scientist = request.json.get('scientist')
    return jsonify(impersonate_scientist(scientist))

if __name__ == '__main__':
    app.run(debug=True)