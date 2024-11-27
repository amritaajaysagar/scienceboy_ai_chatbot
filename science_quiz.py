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
    selected_topics = []  # Keep track of the topics from which questions are selected
    for subject, question_list in question_bank[difficulty].items():
        questions.extend(question_list)

    # Randomly select questions
    selected_questions = random.sample(questions, min(num_questions, len(questions)))

    score = 0
    feedback = {}
    
    # Collect scores per topic that are actually selected for this quiz
    topic_scores = {}

    for q in selected_questions:
        print(q['question'])  # Display the question
        print("Options:", ", ".join(q['options']))  # Display options
        user_answer = input("Your answer: ")  # Get user's answer

        # Identify the topic for the current question
        question_topic = [topic for topic in question_bank[difficulty] if q in question_bank[difficulty][topic]][0]

        # Track the topic for feedback
        selected_topics.append(question_topic)

        # Check if the answer is correct
        if user_answer.strip().lower() == q['answer'].lower():
            score += 1
            if question_topic not in topic_scores:
                topic_scores[question_topic] = 0
            topic_scores[question_topic] += 1  # Increment score for the specific topic
            feedback_message = f"Correct! The answer is {q['answer']} in {question_topic}."
        else:
            feedback_message = f"Wrong! The correct answer was {q['answer']} in {question_topic}."
        
        feedback[question_topic] = feedback_message  # Store feedback for each topic

    # Construct the final feedback
    feedback_message = f"You answered {score} questions correctly."

    # Provide personalized feedback based on the selected topics
    for topic in set(selected_topics):  # Only iterate through topics that were part of the quiz
        if topic_scores.get(topic, 0) == 0:
            feedback_message += f" You can improve on {topic}."
        else:
            feedback_message += f" Great job on {topic}!"

    return {
        "score": score,
        "total_questions": num_questions,
        "feedback": feedback_message
    }
