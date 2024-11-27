from sympy import sympify, latex

def convert_to_latex(equation):
    try:
        sympy_eq = sympify(equation)
        return latex(sympy_eq)
    except Exception as e:
        return str(e)
