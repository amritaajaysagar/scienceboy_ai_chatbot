import json
import random

def load_question_bank():
    with open('question_bank.json') as f:
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

    score = 0
    feedback = []
    topic = difficulty  # Set the topic based on difficulty level

    for q in selected_questions:
        print(q['question'])  # Display the question
        print("Options:", ", ".join(q['options']))  # Display options
        user_answer = input("Your answer: ")  # Get user's answer (replace with your chat framework's method)

        if user_answer.strip().lower() == q['answer'].lower():
            score += 1
            feedback.append(f"Correct! The answer is {q['answer']}.")
        else:
            feedback.append(f"Wrong! The correct answer was {q['answer']}.")

    # Provide feedback based on the score
    feedback_message = f"You answered {score} questions correctly in {topic}."
    if score < num_questions // 2:
        feedback_message += f" You might want to study more on {topic}."
    else:
        feedback_message += f" Great job on {topic}!"

    return {
        "score": score,
        "total_questions": num_questions,
        "feedback": feedback_message
    }