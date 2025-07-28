import os
import fitz  # PyMuPDF
from PyPDF2 import PdfMerger

def add_image_to_pdf(pdf_path, image_path, img_size, position):
    # Open PDF
    doc = fitz.open(pdf_path)
    page = doc[0]
    page_width = page.rect.width
    img_width, img_height = img_size
    x, y = position
    rect = fitz.Rect(x, y, x + img_width, y + img_height)
    page.insert_image(rect, filename=image_path, overlay=True)
    # Save to a temporary file and return its path
    temp_path = pdf_path + "_temp.pdf"
    doc.save(temp_path)
    doc.close()
    return temp_path

def process_and_merge(input_folder, image_path, output_folder, img_size, merged_filename, position):
    os.makedirs(output_folder, exist_ok=True)
    temp_files = []
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            temp_path = add_image_to_pdf(pdf_path, image_path, img_size, position)
            temp_files.append(temp_path)
    # Merge all stamped PDFs into one
    merger = PdfMerger()
    for pdf in temp_files:
        merger.append(pdf)
    merged_path = os.path.join(output_folder, merged_filename)
    merger.write(merged_path)
    merger.close()
    # Remove temp files
    for temp in temp_files:
        os.remove(temp)
    print(f"Done! Merged PDF saved as '{merged_path}'.")

if __name__ == "__main__":
    input_folder = "VISA"           # Folder containing your input PDFs
    output_folder = "OTB"           # Folder to save output PDF
    image_path = "OTB_STAMP.png"    # Your PNG stamp
    img_size = (100, 100)           # Width and height in points (change as needed)
    position = (247.64, 550)        # Centered for A4: (595.28-100)/2=247.64, 250pt up from bottom
    merged_filename = "merged_OTB.pdf"
    process_and_merge(input_folder, image_path, output_folder, img_size, merged_filename, position)
