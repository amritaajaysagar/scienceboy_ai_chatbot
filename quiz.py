import random
import json

QUESTION_BANK_FILE = "question_bank.json"

def load_question_bank():
    with open(QUESTION_BANK_FILE, "r") as f:
        return json.load(f)

def generate_quiz(age):
    question_bank = load_question_bank()
    if age <= 10:
        level = "VeryEasy"
    elif 11 <= age <= 15:
        level = "Medium"
    else:
        level = "Difficult"

    questions = question_bank.get(level, [])
    return random.sample(questions, min(5, len(questions)))

def evaluate_answers(age, user_answers):
    question_bank = load_question_bank()
    if age <= 10:
        level = "VeryEasy"
    elif 11 <= age <= 15:
        level = "Medium"
    else:
        level = "Difficult"

    questions = question_bank.get(level, [])
    correct_answers = [q["answer"] for q in questions]
    score = sum(1 for u, c in zip(user_answers, correct_answers) if u.strip().lower() == c.strip().lower())

    feedback = [f"Q{i+1}: {'Correct' if u.strip().lower() == c.strip().lower() else 'Incorrect'}" for i, (u, c) in enumerate(zip(user_answers, correct_answers))]
    return score, feedback
