from flask import Flask, request, jsonify, render_template
from transformers import pipeline

# Initialize Flask and Hugging Face pipeline
app = Flask(__name__)
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("message")
    context = (
        "Gravity is a force of attraction between objects with mass. "
        "It keeps planets in orbit around the sun and makes objects fall to the ground."
    )
    if not question:
        return jsonify({"error": "Message is required."}), 400

    try:
        answer = qa_pipeline(question=question, context=context)["answer"]
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
