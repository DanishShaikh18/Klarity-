import fitz
import pdfplumber
import camelot
from PIL import Image
import io
import pytesseract

# data = fitz.open(r'data/Software Unit 1.pdf')

# print("Total Pages ", data.page_count)

# pages = data[0]

# blocks = pages.get_text("blocks")

# blocks.sort(key=lambda b: (b[1], b[0]))

# for b in blocks:
#     print(b[4])

# text = ""
# for page in data:
#     text += page.get_text()
# print(text)

# for page_num , page in enumerate(data):
#     blocks = page.get_text("blocks")

#     page_width = page.rect.width
#     midpoint = page_width / 2

#     left_col = [ b for b in blocks if b[0] < midpoint]
#     right_col = [ b for b in blocks if b[0] >= midpoint]

#     print(f"--- Page {page_num + 1} ---")

#     print("Left Column:")
#     for b in sorted(left_col, key=lambda x: x[1]):  # top-to-bottom order
#         print(b[4].strip())
    
#     print("\nRight Column:")
#     for b in sorted(right_col, key=lambda x: x[1]):  # top-to-bottom order
#         print(b[4].strip())




# def extract_only_tables(pdf_path):
#     tables_data = []

#     with pdfplumber.open(pdf_path) as pdf:
#         for page_num, page in enumerate(pdf.pages,start=1):
#             tables = page.extract_tables()

#             for table in tables:
#                 #Filter must have atleast two rows and two columns 
#                 if len(table) >= 2 and any(len(row) > 1 for row in table):
#                     #Optional: ignore table-like text with single long lines
#                     avg_cols = sum(len(row) for row in table) / len(table)
#                     if avg_cols > 1.5:
#                         tables_data.append({
#                             'page': page_num,
#                             'table': table
#                         })
#     return tables_data

# tables = extract_only_tables(r'data/Software Unit 1.pdf')
# for t in tables:
#     print(f"--- Table on Page {t['page']} ---")
#     for row in t['table']:
#         print(row)
        

# def extract_text_from_images(pdf_path):
#     doc = fitz.open(pdf_path)
#     ocr_texts = []

#     for page_num, page in enumerate(doc, start=1):
#         images = page.get_images(full=True)

#         for i , img in enumerate(images):
#             xref = img[0]
#             base_image = doc.extract_image(xref)
#             image_bytes = base_image['image']

#             #Open image with Pillow
#             image = Image.open(io.BytesIO(image_bytes))

#             #Run OCR
#             text = pytesseract.image_to_string(image, config='--psm 6')
#             clean_text = text.strip()

#             if clean_text:
#                 ocr_texts.append({
#                     'page':page_num,
#                     'image_index': i + 1,
#                     'text': clean_text
#                 })
#     return ocr_texts

# ocr_results = extract_text_from_images(r'data/Chatgpt_PDF.pdf')
# for result in ocr_results:
#     print(f"--- OCR Text from Image {result['image_index']} on Page {result['page']} ---")
#     print(result['text'])

# def extract_from_image(path):
#     import google.generativeai as genai
#     genai.configure(api_key="AIzaSyDGLo8r6NuHPkGFxpYHX56aGw6VKlD1ZnM")

#     img = Image.open(path)

#     model = genai.GenerativeModel("gemini-1.5-flash")
#     response = model.generate_content([
#         img,
#         "Extract all text from this image."
#     ])

#     return response.text

# result = extract_from_image(r'data/image.png')
# print(result)



# def extract_text_easyocr(image_path):
#     import easyocr

#     reader = easyocr.Reader(['en'])
#     result = reader.readtext(image_path,detail=0)
#     return '\n'.join(result)
# text = extract_text_easyocr(r'data/image.png')
# print(text)

from pdf2image import convert_from_path
import easyocr
import os

# def extract_text_from_scanned_pdf_easyocr(pdf_path, output_folder="temp_images"):
#     os.makedirs(output_folder, exist_ok=True)
#     pages = convert_from_path(pdf_path)
#     reader = easyocr.Reader(['en'])
#     full_text = []

#     for i, page in enumerate(pages):
#         image_path = f"{output_folder}/page_{i+1}.png"
#         page.save(image_path, 'PNG')
#         text = reader.readtext(image_path, detail=0)
#         full_text.append("\n".join(text))
#         print(f"✅ Processed page {i+1}/{len(pages)}")

#     return "\n\n".join(full_text)

# # Example usage
# pdf_text = extract_text_from_scanned_pdf_easyocr("data/Chatgpt_PDF.pdf")
# print(pdf_text[:1000])

from docx import Document
from pptx import Presentation

# 📘 Extract text from Word (.docx)
def extract_text_from_word(docx_path):
    doc = Document(docx_path)
    text = []
    for para in doc.paragraphs:
        if para.text.strip():
            text.append(para.text.strip())
    for table in doc.tables:
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells if cell.text.strip()]
            if row_data:
                text.append(" | ".join(row_data))
    return "\n".join(text)

# 📊 Extract text from PowerPoint (.pptx)
def extract_text_from_ppt(pptx_path):
    prs = Presentation(pptx_path)
    text = []
    for slide_num, slide in enumerate(prs.slides, start=1):
        text.append(f"\n--- Slide {slide_num} ---")
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text.strip():
                text.append(shape.text.strip())
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text.strip()
            if notes:
                text.append(f"Notes: {notes}")
    return "\n".join(text)


# 🧪 Example usage
if __name__ == "__main__":
    # word_text = extract_text_from_word("data/sample.docx")
    ppt_text = extract_text_from_ppt("data/Team_Bharati[1].pptx")
    
    # print("\n\nWord Output:\n", word_text[:500])
    print("\n\nPPT Output:\n", ppt_text[:500])

