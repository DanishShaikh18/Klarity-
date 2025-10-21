import fitz

data = fitz.open(r'data/5thPractical.pdf')

print("Total Pages ", data.page_count)

for i , page in enumerate(data):
    image_list = page.get_images(full=True)
    print(f"Page {i+1} has {len(image_list)} images")

    for img_index , img in enumerate(image_list):
        xref = img[0]
        base_image = data.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        with open(f"image {i+1}_{img_index+1}.{image_ext}", "wb") as img_file:
            img_file.write(image_bytes)
