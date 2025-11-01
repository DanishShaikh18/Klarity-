import fitz
import pdfplumber
import camelot
from PIL import Image
import io
import pytesseract

data = fitz.open(r'data/Software Unit 1.pdf')

print("Total Pages ", data.page_count)

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
        

def extract_text_from_images(pdf_path):
    doc = fitz.open(pdf_path)
    ocr_texts = []

    for page_num, page in enumerate(doc, start=1):
        images = page.get_images(full=True)

        for i , img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image['image']

            #Open image with Pillow
            image = Image.open(io.BytesIO(image_bytes))

            #Run OCR
            text = pytesseract.image_to_string(image, config='--psm 6')
            clean_text = text.strip()

            if clean_text:
                ocr_texts.append({
                    'page':page_num,
                    'image_index': i + 1,
                    'text': clean_text
                })
    return ocr_texts

ocr_results = extract_text_from_images(r'data/Chatgpt_PDF.pdf')
for result in ocr_results:
    print(f"--- OCR Text from Image {result['image_index']} on Page {result['page']} ---")
    print(result['text'])