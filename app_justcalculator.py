from flask import Flask, render_template, request, jsonify
import math
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expression = data.get('expression')
    
    try:
        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": None}, math.__dict__)
        return jsonify(result=result)
    except Exception as e:
        return jsonify(result="Error"), 400
if __name__ == '__main__':
    app.run(debug=True)