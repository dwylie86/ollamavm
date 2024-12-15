from pathlib import Path
import ebooklib
from ebooklib import epub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
import json
import PyPDF2


def clean_html_content(content):
    """Clean HTML content from EPUB text"""
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)


def process_book(book_path):
    """Process a single book and return its chunks"""
    book_info = {
        'title': book_path.parent.name,  # Calibre folder name is usually title
        'path': str(book_path),
        'chunks': [],
        'format': book_path.suffix
    }

    try:
        if book_path.suffix.lower() == '.epub':
            book = epub.read_epub(str(book_path))
            text = ''
            for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                # Clean the HTML content
                content = item.get_content().decode('utf-8')
                text += clean_html_content(content) + '\n'

        elif book_path.suffix.lower() == '.pdf':
            with open(book_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() + '\n'

        # Create chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        book_info['chunks'] = text_splitter.split_text(text)
        return book_info

    except Exception as e:
        print(f"Error processing {book_path}: {e}")
        return None


def process_library(library_path="/home/koentrus/Calibre Library"):
    """Process entire library and save chunks"""
    processed_books = []
    path = Path(library_path)

    # Process only epub and pdf files
    for book_path in path.rglob('*'):
        if book_path.suffix.lower() in ['.epub', '.pdf']:
            print(f"Processing: {book_path.parent.name}")
            book_info = process_book(book_path)
            if book_info:
                processed_books.append(book_info)

    # Save processed data
    with open('processed_library.json', 'w') as f:
        json.dump(processed_books, f, indent=2)

    return processed_books


if __name__ == "__main__":
    # Process just the WebAssembly book
    test_path = next(Path("/home/koentrus/Calibre Library").rglob('*.epub'))
    print(f"\nTesting with book: {test_path.parent.name}")
    test_result = process_book(test_path)
    if test_result:
        print(f"Successfully processed test book!")
        print(f"Number of chunks: {len(test_result['chunks'])}")
        print(f"\nSample chunk: {test_result['chunks'][0][:200]}...")

        # Save just this book's data
        with open('webassembly_book_chunks.json', 'w') as f:
            json.dump(test_result, f, indent=2)
        print(f"Book chunks saved to webassembly_book_chunks.json")