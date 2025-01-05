import io
import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageFilter
from fastapi.responses import JSONResponse
from app.services.solver import solve_equation
from fastapi import FastAPI, UploadFile, File, Form

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

@app.post("/upload-equation/")
async def upload_equation(file: UploadFile = File(...)):
    # Leer la imagen del archivo subido
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes))
    
    # Preprocesar la imagen
    # Convertir a escala de grises
    gray_image = img.convert('L')
    
    # Aplicar un filtro de suavizado para reducir el ruido (Gaussian Blur)
    smooth_image = gray_image.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Binarizar la imagen (umbralización adaptativa para mejorar el contraste)
    threshold_image = smooth_image.point(lambda p: p > 180 and 255)
    
    # Convertir la imagen binarizada a un formato compatible con OpenCV (para transformación)
    open_cv_image = np.array(threshold_image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_GRAY2BGR)
    
    # Usar un filtro de Canny para detectar bordes y limpiar la imagen (opcional)
    edges = cv2.Canny(open_cv_image, 100, 200)
    
    # Detectar los contornos de la página (puedes omitir esto si no hay distorsión)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Suponiendo que el contorno más grande es la página, puedes corregir la perspectiva si lo necesitas
        # Este paso es opcional, dependiendo de si tus imágenes tienen distorsión
        pass
    
    # Usar Pytesseract para extraer el texto
    custom_config = r'--psm 6'  # Modo de segmentación de página recomendado para texto en línea
    extracted_text = pytesseract.image_to_string(threshold_image, config=custom_config)

    # Si no se extrae texto, devolver un mensaje de error
    if not extracted_text.strip():
        return JSONResponse(status_code=400, content={"message": "No se pudo extraer ninguna ecuación."})

    # Limpiar y devolver la ecuación extraída
    extracted_equation = extracted_text.strip()
    return {"extracted_equation": extracted_equation}

@app.post("/resolve-equation/")
async def resolve_equation(file: UploadFile = File(...)):
    # Leer la imagen del archivo subido
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes))
    
    # Preprocesar la imagen
    # Convertir a escala de grises
    gray_image = img.convert('L')
    
    # Aplicar un filtro de suavizado para reducir el ruido (Gaussian Blur)
    smooth_image = gray_image.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Binarizar la imagen (umbralización adaptativa para mejorar el contraste)
    threshold_image = smooth_image.point(lambda p: p > 180 and 255)
    
    # Convertir la imagen binarizada a un formato compatible con OpenCV (para transformación)
    open_cv_image = np.array(threshold_image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_GRAY2BGR)
    
    # Usar un filtro de Canny para detectar bordes y limpiar la imagen (opcional)
    edges = cv2.Canny(open_cv_image, 100, 200)
    
    # Detectar los contornos de la página (puedes omitir esto si no hay distorsión)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Suponiendo que el contorno más grande es la página, puedes corregir la perspectiva si lo necesitas
        # Este paso es opcional, dependiendo de si tus imágenes tienen distorsión
        pass
    
    # Usar Pytesseract para extraer el texto
    custom_config = r'--psm 6'  # Modo de segmentación de página recomendado para texto en línea
    extracted_text = pytesseract.image_to_string(threshold_image, config=custom_config)

    # Si no se extrae texto, devolver un mensaje de error
    if not extracted_text.strip():
        return JSONResponse(status_code=400, content={"message": "No se pudo extraer ninguna ecuación."})

    # Limpiar y devolver la ecuación extraída
    print('llega hasta aca'*11)
    extracted_equation = extracted_text.strip()
    solution = solve_equation(extracted_equation)
    return {"equation": extracted_equation, "solution": solution}
    



