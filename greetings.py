""" import json
import random
import os

# Load greetings from responses.json
def load_greetings():
    with open('responses.json') as f:
        data = json.load(f)
    return data.get("greetings", [])

# Load user data from user_data.json
def load_user_data():
    if os.path.exists('user_data.json'):
        with open('user_data.json') as f:
            return json.load(f)
    return []

def save_user_data(user_data):
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

def greet_and_create_profile():
    greetings = load_greetings()
    greeting = random.choice(greetings)
    
    print(greeting)  # Replace with your chat framework's method to send the message

    # Ask for user's name
    name = input("What's your name? ")  # Replace with your chat framework's method to receive input
    
    # Load existing profiles to check for duplicates
    profiles = load_user_data()
    
    # Check if the name already exists
    existing_profile = next((profile for profile in profiles if profile['name'].lower() == name.lower()), None)

    if existing_profile:
        print(f"Welcome back, {name}!")  # Replace with your chat framework's method
        return existing_profile  # Return existing profile

    # Ask for user's age
    age = input("How old are you? ")  # Replace with your chat framework's method to receive input
    try:
        age = int(age)
    except ValueError:
        print("Please enter a valid age.")  # Replace with your chat framework's method
        return None

    # Create new profile
    new_profile = {
        "name": name,
        "age": age,
        "score": 0  # Initialize score
    }

    profiles.append(new_profile)
    save_user_data(profiles)

    print(f"Profile created for {name}.")  # Replace with your chat framework's method
    return new_profile

# Example usage
if __name__ == "__main__":
    user_profile = greet_and_create_profile()
    if user_profile:
        print(user_profile)  # Output the user profile for confirmation """


import json
import random
import os

# Load greetings from responses.json
def load_greetings(language='en', default_greeting="Hello!"):
    try:
        with open('responses.json') as f:
            data = json.load(f)
        greetings = data.get("greetings", {}).get(language, [default_greeting])
        return random.choice(greetings)
    except FileNotFoundError:
        return default_greeting
    except json.JSONDecodeError:
        return default_greeting
    except Exception as e:
        print(f"An error occurred: {e}")
        return default_greeting

# Load user data from user_data.json
def load_user_data():
    if os.path.exists('user_data.json'):
        with open('user_data.json') as f:
            return json.load(f)
    return []

def save_user_data(user_data):
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

def greet_and_create_profile(name=None, age=None):
    profiles = load_user_data()
    
    # Check if the name already exists
    if name:
        existing_profile = next((profile for profile in profiles if profile['name'].lower() == name.lower()), None)
        if existing_profile:
            return existing_profile  # Return existing profile

    # If name is not provided or doesn't exist, we need to create a new profile
    if age is not None:
        try:
            age = int(age)
        except ValueError:
            return None  # Invalid age input

        # Create new profile
        new_profile = {
            "name": name,
            "age": age,
            "score": 0  # Initialize score
        }

        profiles.append(new_profile)
        save_user_data(profiles)

        return new_profile
    
    return None  # If no name or age is provided

# Example usage
if __name__ == "__main__":
    user_profile = greet_and_create_profile("Alice", 25)
    if user_profile:
        print(user_profile)  # Output the user profile for confirmation