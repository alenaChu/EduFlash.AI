import pytest
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from app.agents.ocr_agent import OCRAgent, OCRConfig

SAMPLES_DIR = Path("samples")
SAMPLES_DIR.mkdir(exist_ok=True)


def _create_test_image(path: Path) -> Path:
    """Create a simple image with English, Polish and Spanish text."""
    img = Image.new("RGB", (600, 250), color="white")
    draw = ImageDraw.Draw(img)

    # Use a basic system font with visible size
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
    except OSError:
        font = ImageFont.load_default()

    draw.text((20, 30), "Hello world!", font=font, fill="black")
    draw.text((20, 100), "Cześć świecie!", font=font, fill="black")
    draw.text((20, 170), "¡Hola mundo!", font=font, fill="black")

    img.save(path)
    return path


def test_ocr_extracts_text(tmp_path):
    """Ensure OCRAgent extracts non-empty text from an image."""
    img_path = _create_test_image(tmp_path / "ocr_test.png")
    agent = OCRAgent(OCRConfig(languages=["eng", "pol", "spa"]))
    text = agent.extract_text_from_image(img_path)
    assert isinstance(text, str)
    assert len(text) > 10, f"OCR returned too short text: {text!r}"


def test_ocr_handles_missing_file():
    """Ensure OCRAgent raises error for missing file."""
    agent = OCRAgent()
    with pytest.raises(FileNotFoundError):
        agent.extract_text_from_image("samples/does_not_exist.jpg")
