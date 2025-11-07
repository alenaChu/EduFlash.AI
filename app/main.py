from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.routes import ocr_ui

app = FastAPI(title="EduFlash.AI OCR Demo")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(ocr_ui.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    # redirect root URL to the OCR form
    return RedirectResponse(url="/ocr")
