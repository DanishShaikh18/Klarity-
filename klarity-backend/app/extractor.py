import fitz
import pdfplumber
import camelot

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


# with pdfplumber.open(r'data/Software Unit 1.pdf') as pdf:
#     for i , page in enumerate(pdf.pages):
#         tables = page.extract_tables()
#         for table in tables:
#             for row in table:
#                 print(row)

# tables = camelot.read_pdf(r'data/Software Unit 1.pdf', flavor='stream' )
# for table in tables:
#     print(table.df)

def extract_only_tables(pdf_path):
    tables_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages,start=1):
            tables = page.extract_tables()

            for table in tables:
                #Filter must have atleast two rows and two columns 
                if len(table) >= 2 and any(len(row) > 1 for row in table):
                    #Optional: ignore table-like text with single long lines
                    avg_cols = sum(len(row) for row in table) / len(table)
                    if avg_cols > 1.5:
                        tables_data.append({
                            'page': page_num,
                            'table': table
                        })
    return tables_data

tables = extract_only_tables(r'data/Software Unit 1.pdf')
for t in tables:
    print(f"--- Table on Page {t['page']} ---")
    for row in t['table']:
        print(row)
        
            