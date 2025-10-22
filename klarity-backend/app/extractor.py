import fitz

data = fitz.open(r'data/sample_two_column.pdf')

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

for page_num , page in enumerate(data):
    blocks = page.get_text("blocks")

    page_width = page.rect.width
    midpoint = page_width / 2

    left_col = [ b for b in blocks if b[0] < midpoint]
    right_col = [ b for b in blocks if b[0] >= midpoint]

    print(f"--- Page {page_num + 1} ---")

    print("Left Column:")
    for b in sorted(left_col, key=lambda x: x[1]):  # top-to-bottom order
        print(b[4].strip())
    
    print("\nRight Column:")
    for b in sorted(right_col, key=lambda x: x[1]):  # top-to-bottom order
        print(b[4].strip())


