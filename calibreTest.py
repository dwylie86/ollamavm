from pathlib import Path
import json


def scan_calibre_library(library_path="/home/koentrus/Calibre Library"):
    library_info = {
        'total_books': 0,
        'formats': {},
        'errors': []
    }

    path = Path(library_path)

    # Scan all files recursively
    for book_file in path.rglob('*'):
        if book_file.is_file():
            extension = book_file.suffix.lower()
            if extension:
                # Count file formats
                library_info['formats'][extension] = library_info['formats'].get(extension, 0) + 1
                if extension in ['.pdf', '.epub', '.mobi']:
                    library_info['total_books'] += 1

    return library_info


# Run the scan
library_info = scan_calibre_library()
print("\nLibrary Analysis:")
print(f"Total books found: {library_info['total_books']}")
print("\nFile formats found:")
for fmt, count in library_info['formats'].items():
    print(f"{fmt}: {count} files")