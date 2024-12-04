import json
import random

# Load question bank from the JSON file
def load_question_bank():
    with open('question_bank.json') as f:
        return json.load(f)

# Function to generate quiz based on user's age
def generate_quiz(age, num_questions=5):
    question_bank = load_question_bank()
    
    # Determine difficulty based on age
    if age <= 10:
        difficulty = "VeryEasy"
    elif 11 <= age <= 15:
        difficulty = "Medium"
    else:
        difficulty = "Difficult"
    
    questions = question_bank.get(difficulty, [])
    selected_questions = random.sample(questions, min(num_questions, len(questions)))

    return selected_questions

# Function to evaluate answers
def evaluate_answers(user_answers, correct_answers):
    score = 0
    feedback = {}

    # Compare each answer
    for i, (user_answer, correct_answer) in enumerate(zip(user_answers, correct_answers)):
        if user_answer.strip().lower() == correct_answer.strip().lower():
            score += 1
            feedback[f"Q{i+1}"] = "Correct"
        else:
            feedback[f"Q{i+1}"] = f"Wrong! The correct answer is {correct_answer}"

    return score, feedback
