import easyocr
from fastapi import UploadFile
from PIL import Image
import io


# This function uses EasyOCR to extract text from an uploaded image file.
def extract_book_info_from_image(image_file: UploadFile) -> dict:
    # Read the image bytes
    image_bytes = image_file.file.read()
    # Open the image with PIL
    image = Image.open(io.BytesIO(image_bytes))
    # Convert image to RGB if needed
    if image.mode != "RGB":
        image = image.convert("RGB")
    # Save to bytes for EasyOCR
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    buf.seek(0)
    # Initialize EasyOCR reader (English only for now)
    reader = easyocr.Reader(["en"], gpu=False)
    # Run OCR
    result = reader.readtext(buf.getvalue(), detail=0)
    # Join all detected text lines
    raw_text = " ".join(result)
    # Simple heuristics to guess title/author (customize as needed)
    lines = [line.strip() for line in result if line.strip()]
    title = lines[0] if lines else None
    author = lines[1] if len(lines) > 1 else None
    return {"title": title, "author": author, "raw_text": raw_text}
