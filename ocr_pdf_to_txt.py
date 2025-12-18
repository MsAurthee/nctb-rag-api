import os
from pdf2image import convert_from_path
import pytesseract
from pdf2image.pdf2image import pdfinfo_from_path

# =========================
# Base project directory
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =========================
# INPUT PDF (English)
# =========================
PDF_PATH = os.path.join(BASE_DIR, "data", "english", "english_grammar.pdf")

# =========================
# OUTPUT TXT
# =========================
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "txt")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_TXT = os.path.join(OUTPUT_DIR, "english_grammar.txt")

# =========================
# Paths (Windows)
# =========================
POPPLER_PATH = r"D:\AI\RAG_Project\poppler-25.12.0\Library\bin"
TESSERACT_PATH = r"D:\AI\RAG_Project\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# =========================
# OCR settings
# =========================
DPI = 200
PSM = "--psm 6"

# =========================
# Total pages
# =========================
info = pdfinfo_from_path(PDF_PATH, poppler_path=POPPLER_PATH)
total_pages = info["Pages"]
print(f"📄 Pages: {total_pages}")

# =========================
# OCR loop
# =========================
with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
    for page in range(1, total_pages + 1):
        print(f"OCR page {page}/{total_pages}")
        image = convert_from_path(
            PDF_PATH,
            dpi=DPI,
            first_page=page,
            last_page=page,
            poppler_path=POPPLER_PATH
        )[0]

        text = pytesseract.image_to_string(image, lang="eng", config=PSM)
        f.write(f"\n\n--- Page {page} ---\n{text}")

print("✅ OCR done")
print("TXT saved:", OUTPUT_TXT)
