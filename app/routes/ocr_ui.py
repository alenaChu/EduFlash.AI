from pathlib import Path
from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil

from app.agents.ocr_agent import OCRAgent, OCRConfig

router = APIRouter(tags=["OCR"])
templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIR = Path("app/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/ocr", response_class=HTMLResponse)
async def ocr_form(request: Request):
    return templates.TemplateResponse(
        "ocr_form.html", {"request": request, "text": None}
    )


@router.post("/ocr", response_class=HTMLResponse)
async def ocr_submit(
    request: Request,
    file: UploadFile = File(...),
):
    """Handle OCR form submission."""
    temp_path = UPLOAD_DIR / file.filename
    with temp_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # запускаем агент
    cfg = OCRConfig(languages=["pol", "eng", "spa"])
    agent = OCRAgent(cfg)
    text = agent.extract_text_from_image(str(temp_path))

    return templates.TemplateResponse(
        "ocr_form.html",
        {
            "request": request,
            "text": text,
            "image_url": f"/static/uploads/{file.filename}",
            "backend": "tesseract",
        },
    )
