from flask import Flask, request, jsonify, render_template
import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources if you haven't already
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Load responses from JSON file
with open('responses.json') as f:
    responses = json.load(f)

# Serve the HTML file
@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message").lower()
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Tokenize the user message
    tokens = word_tokenize(user_message)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Check for keywords in the user message
    if any(word in filtered_tokens for word in ['hi', 'hello', 'hey']):
        bot_response = random.choice(responses["greetings"])
    elif any(word in filtered_tokens for word in ['bye', 'goodbye']):
        bot_response = random.choice(responses["farewells"])
    elif any(word in filtered_tokens for word in ['how', 'are', 'you']):
        bot_response = random.choice(responses["how_are_you"])
    else:
        bot_response = responses["default"]

    return jsonify({"bot_message": bot_response})

if __name__ == "__main__":
    app.run(debug=True)