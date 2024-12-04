import json
import random

def load_question_bank():
    with open(r'C:\Users\Sarat\OneDrive - Thompson Rivers University\School\Semester 3\ADSC3710_01 - Artificial Intelligence\scienceboy_ai_chatbot\question_bank.json') as f:
        return json.load(f)

def run_quiz(age, num_questions=5):
    question_bank = load_question_bank()
    
    # Determine difficulty level based on age
    if age <= 10:
        difficulty = "VeryEasy"
    elif 11 <= age <= 15:
        difficulty = "Medium"
    else:
        difficulty = "Difficult"
    
    # Get the questions for the selected difficulty
    questions = []
    for subject, question_list in question_bank[difficulty].items():
        questions.extend(question_list)

    # Randomly select questions
    selected_questions = random.sample(questions, min(num_questions, len(questions)))

    quiz_data = []
    for q in selected_questions:
        question_data = {
            'question': q['question'],
            'options': q['options'],
            'correct_answer': q['answer']
        }
        quiz_data.append(question_data)

    return quiz_data  # Return the quiz questions to the front-end for user input

def check_answers(user_answers, correct_answers):
    score = 0
    feedback = []
    
    for i, user_answer in enumerate(user_answers):
        if user_answer.strip().lower() == correct_answers[i].lower():
            score += 1
            feedback.append(f"Question {i+1}: Correct!")
        else:
            feedback.append(f"Question {i+1}: Incorrect! The correct answer was {correct_answers[i]}.")

    return score, feedback
