import fitz
from PIL import Image
from pathlib import Path


SOURCE = "data/synthetic/LOAN-0001/loan_application.pdf"
OUTPUT = "data/synthetic/LOAN-0001/scanned_loan_application.pdf"


def create_scanned_pdf():

    source = fitz.open(SOURCE)

    output = fitz.open()

    for page in source:

        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        image = Image.frombytes(
            "RGB",
            [pixmap.width, pixmap.height],
            pixmap.samples,
        )

        image_path = "/tmp/scanned_page.png"
        image.save(image_path)

        new_page = output.new_page(
            width=page.rect.width,
            height=page.rect.height,
        )

        new_page.insert_image(
            new_page.rect,
            filename=image_path,
        )

    output.save(OUTPUT)

    source.close()
    output.close()

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    create_scanned_pdf()