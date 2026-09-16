import json


def load_library(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_library(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def find_book(books, search_text):
    if search_text is None:
        return None

    search_clean = str(search_text).strip().lower()
    if not search_clean:
        return None

    for book_id, details in books.items():
        b_id = str(book_id).strip().lower()
        title = str(details.get("title", "")).strip().lower()
        author = str(details.get("author", "")).strip().lower()

        if search_clean in (b_id, title, author):
            return book_id

    for book_id, details in books.items():
        b_id = str(book_id).strip().lower()
        title = str(details.get("title", "")).strip().lower()
        author = str(details.get("author", "")).strip().lower()

        if search_clean in b_id or search_clean in title or search_clean in author:
            return book_id

    return None


def display_books(books):
    print("BOOK CATALOGUE")
    print("-" * 60)
    for book_id, details in books.items():
        title = details.get("title", "")
        category = details.get("category", "")
        availability = "AVAILABLE" if details.get("available", True) else "ON LOAN"
        print(f"{book_id} | {title} | {category} | {availability}")


def display_loans(loans, books):
    print("CURRENT LOANS")
    print("-" * 60)
    for loan in loans:
        book_id = loan.get("book_id", "")
        title = books.get(book_id, {}).get("title", "Unknown Title")
        borrower = loan.get("borrower", "")
        print(f"{book_id} | {title} | Borrower: {borrower}")


def library_statistics(books):
    total = len(books)
    available = sum(1 for book in books.values() if book.get("available", True))
    borrowed = total - available
    return (total, available, borrowed)


def main():
    filename = "library.json"
    try:
        data = load_library(filename)
    except Exception:
        return

    if not data:
        return

    lib = data.get("library", {})
    categories = ", ".join(data.get("categories", []))

    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    print(f"Library: {lib.get('name', '')}")
    print(f"Branch: {lib.get('branch', '')}")
    print(f"Year: {lib.get('year', '')}")
    print(f"Categories: {categories}")
    print()

    display_books(data.get("books", {}))
    print()

    display_loans(data.get("loans", []), data.get("books", {}))
    print()

    total, available, borrowed = library_statistics(data.get("books", {}))
    print("STATISTICS")
    print("-" * 60)
    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")


if __name__ == "__main__":
    main()