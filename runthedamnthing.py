import json
import os
from PyPDF2 import PdfReader, PdfWriter
parent_dir = './result'

def split_and_save_pdf(file_name, pages, output_file_name):
    reader = PdfReader(file_name)
    writer = PdfWriter()
    page_range = range(pages['from'], pages['to'] + 1)

    for page_num, page in enumerate(reader.pages, 1):
        if page_num in page_range:
            writer.add_page(page)

    with open(output_file_name, 'wb') as out:
        writer.write(out)

# Read JSON data from file
with open('data.json', 'r') as json_file:
    json_data = json.load(json_file)

# Process each PDF book
for pdf_file, lessons in json_data.items():
    # Process each lesson in the PDF book
    for lesson_name, lesson_data in lessons.items():
        path = os.path.join(parent_dir, lesson_name)

        # Check if parent_dir exists and create if not
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        # Check if path exists and create if not
        if not os.path.exists(path):
            os.makedirs(path)
            
        ans_pages = lesson_data.get('ans', {})
        key_pages = lesson_data.get('key', {})
        output_prefix = f'{pdf_file[:-4]}_{lesson_name}'  # Remove ".pdf" from file name
        split_and_save_pdf(f'./cambooks/{pdf_file}', ans_pages, f'{path}/{output_prefix}_ans.pdf')
        split_and_save_pdf(f'./cambooks/{pdf_file}', key_pages, f'{path}/{output_prefix}_key.pdf')
