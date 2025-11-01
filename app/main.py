# app/main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from weasyprint import HTML
from datetime import datetime
import tempfile
import os

app = FastAPI(title="Smart CV Generator")

# configuration templates & static
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# modèle de données typé
class CVData(BaseModel):
    name: str
    email: str
    skills: str
    experience: str

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/generate", response_class=FileResponse)
async def generate_pdf(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    skills: str = Form(...),
    experience: str = Form(...),
):
    data = CVData(name=name, email=email, skills=skills, experience=experience)

    # rendu du modèle HTML
    html_content = templates.get_template("cv_template.html").render(cv=data.dict(), year=datetime.now().year)


    # génération du PDF temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        HTML(string=html_content).write_pdf(tmp_pdf.name)
        pdf_path = tmp_pdf.name

    return FileResponse(pdf_path, filename=f"{data.name.replace(' ', '_')}_CV.pdf")
