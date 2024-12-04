from sympy import sympify, latex, Eq
import re

def convert_to_latex(equation):
    try:
        # Replace '^' with '**' for SymPy compatibility
        equation = equation.replace("^", "**")

        # Handle equations with '='
        if "=" in equation:
            lhs, rhs = map(str.strip, equation.split("="))
            if not lhs or not rhs:
                raise ValueError("Invalid equation: Both sides of '=' must be non-empty.")
            sympy_eq = Eq(sympify(lhs), sympify(rhs))
        else:
            # Handle single expressions
            sympy_eq = sympify(equation)

        # Generate LaTeX code
        latex_code = latex(sympy_eq)

        # Enhanced post-processing to fix formatting issues
        # 1. Remove `\mathtt{\text{...}}` artifacts
        latex_code = re.sub(r'\\mathtt\{\\text\{(.+?)\}\}', r'\1', latex_code)
        # 2. Replace `\textasciicircum` with `^`
        latex_code = latex_code.replace("\\textasciicircum", "^")
        # 3. Handle any lingering `\text` artifacts
        latex_code = re.sub(r'\\text\{(.+?)\}', r'\1', latex_code)

        return latex_code
    except SyntaxError:
        return "Syntax error: Please check your equation syntax."
    except ValueError as ve:
        return str(ve)
    except Exception as e:
        return f"Error: Unable to process the equation. {e}"
