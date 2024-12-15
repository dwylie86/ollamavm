import PyPDF2
import ebooklib
from ebooklib import epub
import textract


def extract_book_text(book_path):
    if book_path.endswith('.pdf'):
        with open(book_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ' '.join([page.extract_text() for page in reader.pages])
    elif book_path.endswith('.epub'):
        book = epub.read_epub(book_path)
        text = ' '.join([chapter.get_content() for chapter in book.get_items_of_type(ebooklib.ITEM_DOCUMENT)])
    else:
        # For other formats
        text = textract.process(book_path).decode('utf-8')

    return text