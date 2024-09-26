from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)  # To handle cross-origin requests

# Set up OpenAI API key
openai.api_key = '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'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_science_boy():
    question = request.json.get("question")
    
    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        # Use OpenAI's GPT API to get the response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Explain this to a 6-year-old: {question}",
            max_tokens=150,
            temperature=0.7
        )
        answer = response.choices[0].text.strip()
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
