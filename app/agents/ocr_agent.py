from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import numpy as np
import cv2
import pytesseract
from PIL import Image, ImageOps
import os

# Ensure Tesseract language data path (Linux default)
os.environ.setdefault("TESSDATA_PREFIX", "/usr/share/tesseract-ocr/5/tessdata")


@dataclass
class OCRConfig:
    """Configuration for Tesseract OCR agent."""

    languages: List[str] = None
    join_paragraphs: bool = True

    def __post_init__(self):
        if self.languages is None:
            self.languages = ["eng", "pol", "spa"]


class OCRAgent:
    """Lightweight OCR agent using Tesseract only."""

    def __init__(self, config: Optional[OCRConfig] = None) -> None:
        self.config = config or OCRConfig()

    def extract_text_from_image(self, image_path: str | Path) -> str:
        """Run Tesseract OCR on the given image."""
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")

        img = Image.open(path)
        img = ImageOps.exif_transpose(img).convert("RGB")

        # Convert to OpenCV format for preprocessing
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Basic preprocessing: grayscale + contrast enhance
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 9, 75, 75)
        gray = cv2.equalizeHist(gray)

        lang_str = "+".join(self.config.languages)
        text = pytesseract.image_to_string(gray, lang=lang_str)
        return text.replace("\f", "").strip()
