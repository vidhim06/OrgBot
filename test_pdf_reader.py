
from src.document_processing.pdf_reader import extract_text_from_pdf

text = extract_text_from_pdf("data/sample.pdf")

print(text[:2000])
print("\n--- PDF reading test completed ---")
