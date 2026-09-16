from admin import find_book, load_library, save_library


def books_in_category(books, category):
    if not category:
        return []

    cat_lower = str(category).strip().lower()
    matching_ids = []

    for book_id, details in books.items():
        if details.get("category", "").strip().lower() == cat_lower:
            matching_ids.append(book_id)

    return matching_ids


def search_by_title(books, search_text):
    if not search_text:
        return []

    text_lower = str(search_text).strip().lower()
    matching_ids = []

    for book_id, details in books.items():
        if text_lower in details.get("title", "").lower():
            matching_ids.append(book_id)

    return matching_ids


def borrow_book(books, loans, search_text, borrower):
    book_id = find_book(books, search_text)
    if not book_id:
        return "BOOK_NOT_FOUND"

    if not borrower or not str(borrower).strip():
        return "EMPTY_NAME"

    if not books[book_id].get("available", True):
        return "NOT_AVAILABLE"

    books[book_id]["available"] = False
    loans.append({"book_id": book_id, "borrower": str(borrower).strip()})
    return "OK"


def return_book(books, loans, book_title, borrower):
    book_id = find_book(books, book_title)
    if not book_id:
        return "BOOK_NOT_FOUND"

    if not borrower or not str(borrower).strip():
        return "EMPTY_NAME"

    if books[book_id].get("available", True):
        return "NOT_ON_LOAN"

    loan_to_remove = None
    for loan in loans:
        if loan.get("book_id") == book_id:
            loan_to_remove = loan
            break

    if not loan_to_remove:
        return "NOT_ON_LOAN"

    books[book_id]["available"] = True
    loans.remove(loan_to_remove)
    return "OK"


def main():
    print("LIBRARY USER SYSTEM")
    print("=" * 60)

    filename = "library.json"
    try:
        data = load_library(filename)
    except Exception:
        data = None

    if not data:
        data = {"library": {}, "categories": [], "books": {}, "loans": []}

    books = data.get("books", {})
    loans = data.get("loans", [])

    while True:
        print("\n=== LIBRARY MENU ===")
        print("1. Search books by Title")
        print("2. Search books by Category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")

        try:
            choice = input("Select an option (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if choice == "1":
            search_text = input("Enter title: ").strip()
            ids = search_by_title(books, search_text)
            if ids:
                for b_id in ids:
                    status = (
                        "AVAILABLE" if books[b_id].get("available") else "ON LOAN"
                    )
                    print(f"- [{b_id}] {books[b_id]['title']} ({status})")
            else:
                print("No matching books found.")

        elif choice == "2":
            category = input("Enter category: ").strip()
            ids = books_in_category(books, category)
            if ids:
                for b_id in ids:
                    status = (
                        "AVAILABLE" if books[b_id].get("available") else "ON LOAN"
                    )
                    print(f"- [{b_id}] {books[b_id]['title']} ({status})")
            else:
                print("No books found in this category.")

        elif choice == "3":
            search_text = input("Enter book title, author, or ID: ").strip()
            borrower = input("Enter borrower name: ").strip()
            status = borrow_book(books, loans, search_text, borrower)

            if status == "OK":
                print("Book borrowed successfully!")
            elif status == "BOOK_NOT_FOUND":
                print("Error: Book not found.")
            elif status == "EMPTY_NAME":
                print("Error: Borrower name cannot be empty.")
            elif status == "NOT_AVAILABLE":
                print("Error: Book is already on loan.")

        elif choice == "4":
            book_title = input("Enter book title, author, or ID: ").strip()
            borrower = input("Enter borrower name: ").strip()
            status = return_book(books, loans, book_title, borrower)

            if status == "OK":
                print("Book returned successfully!")
            elif status == "BOOK_NOT_FOUND":
                print("Error: Book not found.")
            elif status == "EMPTY_NAME":
                print("Error: Borrower name cannot be empty.")
            elif status == "NOT_ON_LOAN":
                print("Error: Book is not currently on loan.")

        elif choice == "5":
            try:
                save_library(data, filename)
            except Exception:
                pass
            print("Data saved. Exiting program.")
            break
        else:
            print("Invalid option. Please choose between 1 and 5.")


if __name__ == "__main__":
    main()