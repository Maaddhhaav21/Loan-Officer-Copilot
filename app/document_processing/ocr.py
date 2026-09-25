import fitz
import pytesseract
from PIL import Image


def extract_text_with_ocr(file_path: str) -> str:
    document = fitz.open(file_path)

    text = ""

    for page in document:
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        image = Image.frombytes(
            "RGB",
            [pixmap.width, pixmap.height],
            pixmap.samples,
        )

        page_text = pytesseract.image_to_string(image)

        text += page_text + "\n"

    document.close()

    return text.strip()