import json
import random

# Load the question bank from a JSON file
with open('question_bank.json') as f:
    question_bank = json.load(f)

def run_quiz(age, num_questions=5, topic_choice=0):
    """
    Run the quiz based on the user's age and selected topic.

    :param age: The age of the user to determine difficulty level.
    :param num_questions: Number of questions to ask (default is 5).
    :param topic_choice: Index of the selected topic (0-based).
    :return: A dictionary containing the score and feedback.
    """
    # Determine the difficulty level based on age
    difficulty = "Easy" if age <= 5 else "Medium" if age <= 18 else "Difficult"
    
    # Get the topic based on the user's choice
    topics = list(question_bank.keys())
    if topic_choice < 0 or topic_choice >= len(topics):
        return {"error": "Invalid topic choice."}

    topic = topics[topic_choice]
    questions = question_bank[topic][difficulty]
    
    # Ensure the number of questions does not exceed available questions
    num_questions = min(num_questions, len(questions))
    selected_questions = random.sample(questions, num_questions)

    score = 0
    for idx, q in enumerate(selected_questions, start=1):
        # Here, we can simulate user input for testing purposes
        # In the main_app.py, you would replace this with actual user input
        print(f"\nQuestion {idx}: {q['question']}")
        for i, option in enumerate(q["options"], start=1):
            print(f"{i}. {option}")
        
        # Simulate receiving an answer (for integration, replace this with actual input)
        answer = int(input("Enter your answer (1/2/3/4): "))  # Replace with actual input method
        if q["options"][answer - 1] == q["answer"]:
            score += 1

    feedback = f"You answered {score} questions correctly in {topic}."
    if score < num_questions // 2:
        feedback += f" You might want to study more on {topic}."
    else:
        feedback += f" Great job on {topic}!"

    return {
        "score": score,
        "total_questions": num_questions,
        "feedback": feedback
    }