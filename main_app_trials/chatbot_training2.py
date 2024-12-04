import os
import json
import logging
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from sklearn.metrics import accuracy_score
from transformers import pipeline

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize pre-trained QA pipeline
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Initialize the chatbot
def initialize_chatbot():
    chatbot = ChatBot(
        'AdvancedChatBot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            'chatterbot.logic.BestMatch',
        ],
        read_only=False
    )
    return chatbot

# Train the chatbot
def train_chatbot(chatbot, custom_corpus_path='custom_corpus.json'):
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train('chatterbot.corpus.english')
    logging.info("Trained with ChatterBot's default English corpus.")

    # Train with custom corpus if available
    if os.path.exists(custom_corpus_path):
        with open(custom_corpus_path) as f:
            custom_data = json.load(f)
            custom_conversations = custom_data['conversations']
            structured_data = [item for convo in custom_conversations for item in convo]
            custom_trainer = ListTrainer(chatbot)
            custom_trainer.train(structured_data)
        logging.info(f"Trained with custom corpus from {custom_corpus_path}.")
    else:
        logging.warning(f"Custom corpus file {custom_corpus_path} not found. Skipping custom training.")

# Use pre-trained model for fallback responses
def use_pretrained_model(query, context=""):
    try:
        result = qa_pipeline(question=query, context=context)
        return result['answer']
    except Exception as e:
        logging.error(f"Error using pre-trained model: {e}")
        return "I'm not sure about that. Let me look it up for you!"

# Evaluate the chatbot
def evaluate_chatbot(chatbot, test_data_path='test_data.json'):
    if not os.path.exists(test_data_path):
        logging.warning(f"Test data file {test_data_path} not found. Skipping evaluation.")
        return

    with open(test_data_path) as f:
        test_data = json.load(f)

    true_responses = []
    predicted_responses = []

    for query, expected_response in test_data.items():
        predicted_response = chatbot.get_response(query).text
        true_responses.append(expected_response)
        predicted_responses.append(predicted_response)

    # Example metric: Accuracy (you can enhance this with more advanced NLP metrics)
    accuracy = accuracy_score(true_responses, predicted_responses)
    logging.info(f"Evaluation complete. Accuracy: {accuracy * 100:.2f}%.")

# Chatbot response handler with pre-trained model fallback
def get_response(chatbot, query, context=""):
    # First, try the chatbot
    chatbot_response = chatbot.get_response(query)

    # Use pre-trained model if confidence is low
    if float(chatbot_response.confidence) < 0.6:
        logging.info("Using pre-trained model for better response.")
        return use_pretrained_model(query, context)
    
    return chatbot_response.text

# Save chatbot as callable function
def setup_chatbot(custom_corpus_path='custom_corpus.json', test_data_path='test_data.json'):
    chatbot = initialize_chatbot()
    train_chatbot(chatbot, custom_corpus_path)
    evaluate_chatbot(chatbot, test_data_path)
    return chatbot

if __name__ == "__main__":
    chatbot_instance = setup_chatbot()

    # Example usage
    user_query = "What is gravity?"
    context_info = ("Gravity is a force of attraction between objects with mass. "
                    "It keeps planets in orbit and makes objects fall to the ground.")
    response = get_response(chatbot_instance, user_query, context=context_info)
    logging.info(f"Response: {response}")
