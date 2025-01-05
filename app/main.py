from fastapi import FastAPI, UploadFile, Form
from app.services.solver import solve_equation

app = FastAPI()

@app.post("/solve")
async def solve_equation_endpoint(equation: str = Form(...)):
    print('*'*10)
    print( equation )
    solution = solve_equation(equation)
    return {"equation": equation, "solution": solution}

@app.get("/")
def read_root():
    return {"message": "Welcome to Matt's Backend API"}