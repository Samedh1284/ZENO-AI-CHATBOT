from pathlib import Path
from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = PROJECT_ROOT / "documents" / "sample.pdf"


def read_pdf():

    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"PDF not found: {PDF_PATH}"
        )

    reader = PdfReader(str(PDF_PATH))

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


if __name__ == "__main__":

    print("Reading PDF...")

    text = read_pdf()

    print("\nPDF successfully read!")

    print("\nFirst 2000 characters:\n")

    print(text[:2000])