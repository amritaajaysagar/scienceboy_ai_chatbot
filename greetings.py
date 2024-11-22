import json
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
        print(user_profile)  # Output the user profile for confirmation