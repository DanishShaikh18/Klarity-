import pdfplumber
import fitz



file_path = r'data/BasicConceptualQuestions-Python.pdf'


with pdfplumber.open(file_path) as pdf:
    for page in pdf.pages:
        print(page.extract_text())
    

    