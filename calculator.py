from flask import Flask, request, render_template
import math

app = Flask(__name__)

@app.route('/calculator')
def calculator():
    return render_template("calculator.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.form['expression']
    try:
        # Allow only certain math functions and constants
        allowed_names = {
            'sqrt': math.sqrt,
            'pow': math.pow,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'log': math.log,
            'exp': math.exp,
            'pi': math.pi,
            'e': math.e
        }
        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": None}, allowed_names)
    except Exception as e:
        result = str(e)
    return str(result)

if __name__ == '__main__':
    app.run(port=5001)  # Run on a different port to avoid conflicts