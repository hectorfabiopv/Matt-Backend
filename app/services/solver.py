import re
from sympy import symbols, diff, integrate, Eq, solve
from sympy.parsing.sympy_parser import parse_expr

def sanitize_equation(equation: str) -> str:
    # Reemplaza múltiples espacios por un solo espacio
    equation = re.sub(r'\s+', ' ', equation)
    # Corrige los operadores ausentes (si es necesario)
    equation = equation.replace(' ', '+')  # Esto es básico, adapta según necesidades reales
    return equation

def solve_equation(equation: str):
    try:
        equation = sanitize_equation(equation)  # Limpieza antes del procesamiento
        x = symbols('x')
        parsed_equation = parse_expr(equation)
        derivative = diff(parsed_equation, x)
        integral = integrate(parsed_equation, x)
        return {
            "derivative": str(derivative),
            "integral": str(integral)
        }
    except Exception as e:
        return {"error": str(e)}



