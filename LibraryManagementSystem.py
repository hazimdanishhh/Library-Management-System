import csv

# ===============================================
# Base class for Book Management (abstracts common logic for both Static and Dynamic Data Structures)
# ===============================================
class BookManagerBase:
    def search_book(self, isbn=None, title=None):
        for book in self.get_books():
            if isbn and book['isbn'] == isbn:
                return book
            if title and book['title'].lower() == title.lower():
                return book
        return None

    def display_books(self):
        books = self.get_books()
        if not books:
            print("\nNo books available.")
        else:
            for book in books:
                print(f"{book['isbn']}        {book['title']}")

    def get_books(self):
        #Should return list of books. Overridden by subclasses
        raise NotImplementedError

# ===============================================
# Static Data Structure: Array (Max capacity of 100)
# ===============================================
class StaticBookArray(BookManagerBase):
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.books = []
    
    def add_book(self, isbn, title):
        if len(self.books) < self.capacity:
            self.books.append({"isbn": isbn, "title": title})
        else:
            print("\nLibrary is full.")

    def remove_book(self, isbn=None, title=None):
        book = self.search_book(isbn, title)
        if book:
            self.books.remove(book)
            return True
        return False

    def get_books(self):
        return self.books

# ===============================================
# Dynamic Data Structure: Linked List
# ===============================================
class Node:
    def __init__(self, isbn, title):
        self.isbn = isbn
        self.title = title
        self.next = None

class DynamicBookLinkedList(BookManagerBase):
    def __init__(self):
        self.head = None

    def add_book(self, isbn, title):
        new_node = Node(isbn, title)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def remove_book(self, isbn=None, title=None):
        current, prev = self.head, None
        while current:
            if (isbn and current.isbn == isbn) or (title and current.title.lower() == title.lower()):
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev, current = current, current.next
        return False

    def get_books(self):
        books = []
        current = self.head
        while current:
            books.append({"isbn": current.isbn, "title": current.title})
            current = current.next
        return books

# ===============================================
# Stack-based Undo/Redo System (Array-Based)
# ===============================================
class UndoRedoStack:
    def __init__(self, limit=10):
        self.undo_stack = []
        self.redo_stack = []
        self.limit = limit

    def push_undo(self, action):
        if len(self.undo_stack) >= self.limit:
            self.undo_stack.pop(0)  # Remove the oldest action if limit is reached
        self.undo_stack.append(action)
        self.redo_stack.clear()  # Clear redo stack whenever a new action occurs

    def push_redo(self, action):
        if len(self.redo_stack) >= self.limit:
            self.redo_stack.pop(0)
        self.redo_stack.append(action)

    def undo(self, book_manager):
        if not self.undo_stack:
            print("\nNo actions to undo.")
            return
        action = self.undo_stack.pop()
        if action['type'] == 'add':
            book_manager.remove_book(isbn=action['isbn'])
            self.push_redo(action)  # Move this action to redo stack
            print(f"\nUndo: Removed book {action['isbn']}")
        elif action['type'] == 'remove':
            book_manager.add_book(action['isbn'], action['title'])
            self.push_redo(action)
            print(f"\nUndo: Re-added book {action['isbn']}")

    def redo(self, book_manager):
        if not self.redo_stack:
            print("\nNo actions to redo.")
            return
        action = self.redo_stack.pop()
        if action['type'] == 'add':
            book_manager.add_book(action['isbn'], action['title'])
            self.push_undo(action)
            print(f"\nRedo: Re-added book {action['isbn']}")
        elif action['type'] == 'remove':
            book_manager.remove_book(isbn=action['isbn'])
            self.push_undo(action)
            print(f"\nRedo: Removed book {action['isbn']}")

# ===============================================
# CSV Manager (For Reading and Writing into CSV File)
# ===============================================
class CSVManager:
    def __init__(self, filename="books.csv"):
        self.filename = filename

    def load_books(self, book_manager):
        try:
            with open(self.filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book_manager.add_book(row['isbn'], row['title'])
            print("\nBooks loaded from CSV.")
        except FileNotFoundError:
            print("\nCSV file not found.")

    def save_books(self, book_manager):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['isbn', 'title'])
            writer.writeheader()
            writer.writerows(book_manager.get_books())
        print("\nBooks saved to CSV.")

# ===============================================
# User Interface Main Menu (with Undo/Redo options)
# ===============================================
if __name__ == "__main__":
    print("\n+-------------------------------------------+")
    print("| Welcome to The Library Management System! |")
    print("|                                           |")
    print("| Please choose a data structure:           |")
    print("| 1. Static Array                           |")
    print("| 2. Dynamic Linked List                    |")
    print("+-------------------------------------------+")

    while True:
        choice = input("> Enter 1 or 2: ").strip()
        if choice == "1":
            book_manager = StaticBookArray()
            break
        elif choice == "2":
            book_manager = DynamicBookLinkedList()
            break
        else:
            print("\nInvalid choice. Please enter 1 or 2.")

    csv_manager = CSVManager()
    undo_redo = UndoRedoStack()
    csv_manager.load_books(book_manager)

    def prompt_user(message, options):
        while True:
            response = input(message).strip().lower()
            if response in options:
                return response
            print(f"\nInvalid choice. Please enter one of {', '.join(options)}.")

    while True:
        print("\n+-------------------------------+")
        print("|           MAIN MENU           |")
        print("+-------------------------------+")
        print("| 1. Display All Books          |")
        print("| 2. Add Book                   |")
        print("| 3. Search Book                |")
        print("| 4. Remove Book                |")
        print("| 5. Save Changes to CSV        |")
        print("| 6. Undo                       |")
        print("| 7. Redo                       |")
        print("| 8. Exit                       |")
        print("+-------------------------------+")
        
        option = input("> Choose option: ").strip()

        if option == "1":
            print("\nBooks in the Library:")
            print("-------------------------------------------------------------------")
            print("ISBN       |     Title")
            print("-------------------------------------------------------------------")
            book_manager.display_books()
            print("-------------------------------------------------------------------")

        elif option == "2":
            isbn = input("\nEnter ISBN: ").strip()
            title = input("Enter Title: ").strip()
            book_manager.add_book(isbn, title)
            undo_redo.push_undo({"type": "add", "isbn": isbn, "title": title})
            print("\nBook added successfully.")

        elif option == "3":
            search_type = prompt_user("Search by ISBN or Title? (isbn/title): ", ["isbn", "title"])
            value = input(f"Enter {search_type.title()}: ").strip()
            book = book_manager.search_book(isbn=value if search_type == "isbn" else None, title=value if search_type == "title" else None)
            print(f"\nBook found: {book}" if book else "\nBook not found.")

        elif option == "4":
            remove_type = prompt_user("Remove by ISBN or Title? (isbn/title): ", ["isbn", "title"])
            value = input(f"Enter {remove_type.title()}: ").strip()
            book = book_manager.search_book(isbn=value if remove_type == "isbn" else None, title=value if remove_type == "title" else None)
            if book_manager.remove_book(isbn=value if remove_type == "isbn" else None, title=value if remove_type == "title" else None):
                undo_redo.push_undo({"type": "remove", "isbn": book['isbn'], "title": book['title']})
                print("\nBook removed.")
            else:
                print("\nBook not found.")

        elif option == "5":
            csv_manager.save_books(book_manager)

        elif option == "6":
            undo_redo.undo(book_manager)

        elif option == "7":
            undo_redo.redo(book_manager)

        elif option == "8":
            print("Exiting...")
            break

        else:
            print("\nInvalid option. Please choose a number from 1 to 8.")
