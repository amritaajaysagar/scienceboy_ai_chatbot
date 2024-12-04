import json
import random
import os
import re
from flask import redirect, url_for,request
from flask import render_template
from app_integrated2 import app_integrated2  


USER_DATA_FILE = "user_data.json"
# Load user data from user_data.json
def load_user_data():
    if os.path.exists('user_data.json'):
        with open('user_data.json') as f:
            return json.load(f)
    return []

def save_user_data(user_data):
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

def get_user_data(user_message):
    """Retrieve user data from a file, greet user, and manage profiles."""
    try:
        # Attempt to load existing user data from file
        with open(USER_DATA_FILE, 'r') as f:
            user_data = json.load(f)
    except FileNotFoundError:
        # If file doesn't exist, initialize an empty user data dictionary
        user_data = {}

    # Check if greeting message was received
    greetings_list = ["hello", "hi", "hi there", "hey there", "greetings","hey bot"]
    if any(greeting in user_message.lower() for greeting in greetings_list):
        
        #response = ""
        response = f"Hello to you too, May I know your name?"

        #user_message = request.json.get("message").strip().lower()

    # Check if name and age exist
    if "name" in user_message.lower():
        # Save the name
        name = user_message.strip()
        user_data["name"] = name
        response = f"Nice to meet you, {name}! How old are you?"
        return response

    if "age" in user_message.lower():
        # Save the age
        age = user_message.strip()
        user_data["age"] = age
        # Save the user data to the file
        save_user_data(user_data)
        response = f"Thank you for providing your details, {user_data['name']}! You can now start chatting with me."                    
    
        # If user data exists, check for the name and age
        # if user_data:
        #     name = user_data.get("name")
        #     if name:
        #         age = user_data.get("age")
        #         response = f"Welcome back, {name}! How have you been? What would you like to do today?"
        #         # Proceed to chat after welcoming back
        #         return response  # Proceed to main chat after greeting
        #     else:
        #         # If name is not found in user data, prompt for the name
        #         response = "Please provide your name to continue."

        # else:
        #     # If no user data exists, ask for the name and age
        #     response = "Hello! I don't have your profile yet. Please provide your name."

        # return response  # Return greeting response for now



        # Proceed to main chat after saving user details
        return response  # This will return back to the main chat now

 

   

