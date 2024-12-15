import calibre
import os
import json


def extract_calibre_metadata():
    books = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.epub') or file.endswith('.pdf'):
                book_path = os.path.join(root, file)
                try:
                    # Extract metadata
                    metadata = calibre.metadata_from_format_with_cache(book_path)
                    book_info = {
                        'title': metadata.title,
                        'authors': metadata.authors,
                        'tags': metadata.tags,
                        'series': metadata.series,
                        'languages': metadata.languages,
                        'path': book_path
                    }
                    books.append(book_info)
                except Exception as e:
                    print(f"Could not process {file}: {e}")

    return books


# Save metadata to a JSON file
book_metadata = extract_calibre_metadata()
with open('calibre_library_metadata.json', 'w') as f:
    json.dump(book_metadata, f, indent=2)