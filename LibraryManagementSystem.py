import csv
import heapq as hq
from datetime import datetime
# ===============================================
# Base class for Book Management (abstracts common logic for both Static and Dynamic Data Structures)
# ===============================================
class BookManagerBase:
    def search_book(self, isbn=None, title=None):
        # Loop through each book and check if its ISBN or title matches the given search criteria
        for book in self.get_books():
            if isbn and book.get('isbn', None) == isbn:  # Safely access 'isbn' with .get()
                return book
            if title and book.get('title', '').lower() == title.lower():  # Safely access 'title'
                return book
        return None  # If no matching book is found, return None

    def display_books(self):
        books = self.get_books()
        if not books:  # Checks if the books list is empty
            print("\nNo books available.")
        else:
            for book in books:  # Loop through each book and print its details
                print(f"{book.get('isbn', 'N/A')}\t|\t{book.get('title', 'N/A')}")  # Safely handle missing 'isbn' or 'title'

    def get_books(self):        # Placeholder method to be overridden by subclasses
        raise NotImplementedError   # Force subclasses to implement their own method for getting books

    def get_borrowed_books(self):
        books = self.get_books()
        # Safely access 'user' and 'date' to avoid KeyError
        return [book for book in books if book.get('user', '') != '' and book.get('date', '') != '']

    def get_user_borrowed_books(self, user=None):
        borrowed_books = self.get_borrowed_books()
        return [book for book in borrowed_books if book['user'] == user]

    def display_user_borrowed_books(self, user=None):
        user_borrowed_books = self.get_user_borrowed_books(user)
        if not user_borrowed_books:  # Check if the user has borrowed any books
            print("\nNo books available.")
        else:
            print("-------------------------------------------------------------------")
            print("ISBN            |       Title\t\t|\tDate Borrowed")
            print("-------------------------------------------------------------------")
            for book in user_borrowed_books:
                # Safely handle missing 'isbn', 'title', or 'date' to avoid KeyError
                print(f"{book.get('isbn', 'N/A')}\t|\t{book.get('title', 'N/A')}\t|\t{book.get('date', 'N/A')}")
            print("-------------------------------------------------------------------")  # Close the display with a separator

    def get_max_heap_overdue_books(self, days_due=None):
        borrowed_books = self.get_borrowed_books()
        overdue_list = []
        for book in borrowed_books:
        #Convert the date (stored as string) to datetime format for use in deltatime operations
        #Get Delta to today and compare to days due for a book. Days overdue = Delta - Days due
            if (days_delta := (datetime.today()-datetime.strptime(book['date'],'%Y-%m-%d')).days)>days_due:
                #Nest book in overdue dict in a tuple with days overdue
                overdue_list.append({tuple(book.items()): days_delta-days_due})   
        overdue_tuples_list = []    #temporary list to hold tuple pair of book-days
        # Convert each entry from dict (mutable type) to tuple (immutable type) to allow max-heap sort
        overdue_tuples_list = [(book, days_overdue) for index in overdue_list for book, days_overdue in index.items()]
        # Generate a list. Each entry contains days overdue in negative to allow using heapq as max-heap, and the nested entry from source list
        heap_transform_list = [(item[1]*-1, item) for item in overdue_tuples_list]
        hq.heapify(heap_transform_list)     # Use heapify to transform the list into a max-heap structure.
        return heap_transform_list

    def display_max_heap_overdue_books(self, days_due=None):
        heap_transform_list = self.get_max_heap_overdue_books(days_due)
        if not heap_transform_list:
            print("\nNo overdue books.")            
        else:    
            print("-----------------------------------------------------------------------------------------------------------")
            print("ISBN            |  Borrowed by\t|\tDate Borrowed\t| Days overdue\t|       Title")
            print("-----------------------------------------------------------------------------------------------------------")        
            while len(heap_transform_list) > 0:
                # Pop the entry with the largest days_overdue and rearrange the max-heap structure.
                entry = hq.heappop(heap_transform_list)[1]
                if entry:
                    isbn = entry[0][0][1]
                    title = entry[0][1][1]
                    user = entry[0][2][1]
                    date = entry[0][3][1]
                    days_overdue = entry[1]
                    print(f"{isbn}\t|\t{user}\t|\t{date}\t|\t{days_overdue}\t|\t{title}")
            print("-----------------------------------------------------------------------------------------------------------")
            print("-----------------------------------------------------------------------------------------------------------\n")
    
    def borrow_book(self, isbn=None, title=None, user=None, date=None):
        book = self.search_book(isbn, title)
        if book:
            title = book['title']
            if title in self.borrow_queue and self.borrow_queue[title]:
                self.borrow_queue[title].append({"user": user, "date": date})
                print(f"Book '{title}' is currently borrowed. {user}, you have been added to the waiting queue.")
            else:
                self.borrow_queue[title] = [{"user": user, "date": date}]
                if self.borrow_book_sub(book, user, date):   #Check if method exists
                    print(f"Book '{title}' borrowed by {user} on {date}.")                    
                else:
                    print(f"Error borrowing the book (The borrow function is not implemented for this data structure.)")
        else:
            print(f"Book '{title}' not found.")

    def borrow_book_sub(self, book=None, user=None, date=None):
        return False    #Method does not exist outside the subclasses

    def display_borrow_queue(self):
        if not self.borrow_queue:
            print("No books are currently borrowed.")
        else:
            print("Borrow Queue:")
            for title, users in self.borrow_queue.items():
                print(f"Book Title: {title}")
                for i, user_info in enumerate(users):
                    status = "Borrowed" if i == 0 else "Waiting"
                    print(f"  User: {user_info['user']}, Borrow Date: {user_info['date']}, Status: {status}")

# ===============================================
# Static Data Structure: Array (Max capacity of 100)
# ===============================================

#This class inherits from BookManagerBase and has access to the methods defined in its parent (search_book, display_books etc.)
class StaticBookArray(BookManagerBase):     
    def __init__(self, capacity=100):       #Constructor method, book array with max capacity of 100 books.       
        self.capacity = capacity        #Stores value of capacity in the instance variable.        
        self.books = []                 #Stores the books
        self.borrow_queue = {}          #Manages the borrow queue

    def add_book(self, isbn, title, user='', date=''):
        if len(self.books) < self.capacity:     #If length of array is less than capacity, append the new book to the books array.
            self.books.append({"isbn": isbn, "title": title, "user": user, "date": date})
        else:       #Else, the array will not accept any more books as it is full.
            print("\nLibrary is full.")

    def remove_book(self, isbn=None, title=None):
        book = self.search_book(isbn, title)        #Calls search_book method inherited from BookManagerBase and stores in book variable.
        if book:        #If book is found and not None, remove the book from the books array.
            self.books.remove(book)
            return True
        return False
    
    def get_books(self):    #Defined function to override base class method from BookManagerBase.        
        return self.books   #Returns the list of books stored in self.books array.

    def borrow_book_sub(self, book=None, user=None, date=None):
        borrowed_book = book
        borrowed_book['user'] = user            # Assign borrow details
        borrowed_book['date'] = date
        index = self.books.index(book)
        self.books[index] = borrowed_book       # Update the book details in the list
        return True

    def return_book(self, isbn=None, user=None):
        borrowed_book = self.search_book(isbn, None)                # Find the book using its ISBN
        if borrowed_book and borrowed_book.get('user') == user:     # Ensure the book is actually borrowed by the user
            borrowed_book['user'] = ''          # Clear the user field
            borrowed_book['date'] = ''          # Clear the date field
            books = self.get_books()            
            index = books.index(borrowed_book)      # Find the index of the borrowed book
            self.books[index] = borrowed_book       # Update the book in the self.books list
            return True
        return False

# ===============================================
# Dynamic Data Structure: Linked List
# ===============================================
class Node:                 # Defines a node in a linked list to store book details.
    def __init__(self, isbn, title, user='', date=''):
        self.isbn = isbn
        self.title = title
        self.user = user
        self.date = date
        self.next = None

class DynamicBookLinkedList(BookManagerBase):   # Manages the books as a linked list of Node objects.
    def __init__(self):
        self.head = None        # Initialize the linked list, with head as None.
        self.borrow_queue = {}

    def add_book(self, isbn, title, user='', date=''):
        new_node = Node(isbn, title, user, date)    # Create a new Node object for the book.
        if not self.head:
            self.head = new_node    # If the list is empty, set the new node as head.
        else:
            current = self.head             # Set current to point to the head
            while current.next:             # Traverse to the end of the list.
                current = current.next
            current.next = new_node         # Add the new node at the end of the list.

    def remove_book(self, isbn=None, title=None):
        current, prev = self.head, None     #current: point to first node, prev: keep track of previous node in the list
        while current:      # Traverse the list.
            if (isbn and current.isbn == isbn) or (title and current.title.lower() == title.lower()):
                if prev:        #Checks if current node is not the head node.
                    prev.next = current.next    # Remove the current node.
                else:
                    self.head = current.next    # Remove the head node.
                return True
            prev, current = current, current.next       
        return False

    def get_books(self):
        books = []
        current = self.head
        while current:          # Collect all books in a list.
            books.append({
                "isbn": current.isbn,
                "title": current.title,
                "user": current.user,
                "date": current.date
            })
            current = current.next
        return books

    def borrow_book_sub(self, book=None, user=None, date=None):
        current = self.head
        isbn = book['isbn']
        while current:
            if (isbn and current.isbn == isbn):
                current.user = user     #Assign borrow details
                current.date = date  
                break
            current = current.next
        return True

    def return_book(self, isbn=None, user=None):
        current = self.head
        while current:
            if current.isbn == isbn and current.user == user:
                current.user = ''  # Clear user in the node.
                current.date = ''  # Clear borrow date in the node.
                break
                return True
            current = current.next
        return False

# ===============================================
# Stack-based Undo/Redo System (Array-Based) Currently only for Adding and Removing books
# ===============================================
class UndoRedoStack:
    def __init__(self, limit=10):
        self.undo_stack = []        #Store actions that can be undone.
        self.redo_stack = []        #Store actions that can be redone.
        self.limit = limit          #Limit of actions that can be stored in both stacks.

    def push_undo(self, action):
        if len(self.undo_stack) >= self.limit:
            self.undo_stack.pop(0)      #Remove the oldest action if limit is reached.
        self.undo_stack.append(action)      #Append newest action to the undo_stack.
        self.redo_stack.clear()     #Clear redo stack whenever a new action occurs.

    def push_redo(self, action):
        if len(self.redo_stack) >= self.limit:
            self.redo_stack.pop(0)      #Remove the oldest action if limit is reached.
        self.redo_stack.append(action)      #Append newest undone action to the redo_stack.

    def undo(self, book_manager):       #This method performs the undo operation.
        if not self.undo_stack:
            print("\nNo actions to undo.")      #If undo_stack is empty, exit.
            return
        action = self.undo_stack.pop()      #If there is an action to undo, remove the most recent action from the undo_stack and stores in the action variable.
        if action['type'] == 'add':     #Checks if action is addition of a book.
            book_manager.remove_book(isbn=action['isbn'])       #Calls remove_book method, removes the book that was added. Uses the isbn stored in the action dictionary.
            self.push_redo(action)      #Move this action to redo stack.
            print(f"\nUndo: Removed book {action['isbn']}")
        elif action['type'] == 'remove':        #Checks if action is removal of a book.
            book_manager.add_book(action['isbn'], action['title'], user, date)      #Calls add_book method, adds the recently removed book.
            self.push_redo(action)      #Move this action to redo stack.
            print(f"\nUndo: Re-added book {action['isbn']}")

    def redo(self, book_manager):       #This method performs the redo operation.
        if not self.redo_stack:
            print("\nNo actions to redo.")
            return
        action = self.redo_stack.pop()
        if action['type'] == 'add':
            book_manager.add_book(action['isbn'], action['title'], action.get['user'], action.get['date'])
            self.push_undo(action)
            print(f"\nRedo: Re-added book {action['isbn']}")
        elif action['type'] == 'remove':
            book_manager.remove_book(isbn=action['isbn'])
            self.push_undo(action)
            print(f"\nRedo: Removed book {action['isbn']}")

# ===============================================
# Binary Tree-based Book Search (BST)
# ===============================================
class BSTNode:
    def __init__(self, isbn, title, user, date): 
        self.isbn = isbn
        self.title = title
        self.user = user
        self.date = date
        self.left = None
        self.right = None

class BinarySearchTree(BookManagerBase):
    def __init__(self):
        self.root = None

    def add_book(self, isbn, title, user, date):
        self.root = self._add_recursive(self.root, isbn, title, user, date)

    def _add_recursive(self, node, isbn, title, user, date):
        if not node:
            return BSTNode(isbn, title, user, date)
        if isbn < node.isbn:
            node.left = self._add_recursive(node.left, isbn, title, user, date)
        elif isbn > node.isbn:
            node.right = self._add_recursive(node.right, isbn, title, user, date)
        else:
            print("\nBook with this ISBN already exists.")
        return node

    def remove_book(self, isbn=None):
        self.root, removed_book = self._delete_recursive(self.root, isbn)
        return removed_book

    def _delete_recursive(self, node, isbn):
        if not node:
            return node, None
        if isbn < node.isbn:
            node.left, removed_book = self._delete_recursive(node.left, isbn)
        elif isbn > node.isbn:
            node.right, removed_book = self._delete_recursive(node.right, isbn)
        else:
            removed_book = {"isbn": node.isbn, "title": node.title, "user": node.user, "date": node.date}
            if not node.left:
                return node.right, removed_book
            if not node.right:
                return node.left, removed_book
            min_node = self._min_value_node(node.right)
            node.isbn, node.title = min_node.isbn, min_node.title
            node.right, _ = self._delete_recursive(node.right, min_node.isbn)
        return node, removed_book

    def _min_value_node(self, node):
        while node.left: node = node.left
        return node

    def search_book(self, isbn=None, title=None):
        return self._search_recursive(self.root, isbn)

    def _search_recursive(self, node, isbn=None, title=None):
        if not node:
            return None
        if isbn == node.isbn:
            return {"isbn": node.isbn, "title": node.title, "user": node.user, "date": node.date}
        elif isbn < node.isbn:
            return self._search_recursive(node.left, isbn)
        else:
            return self._search_recursive(node.right, isbn)


    def get_books(self):
        books = []
        self._inorder_traversal(self.root, books)
        return books

    def _inorder_traversal(self, node, books):
        if node:
            self._inorder_traversal(node.left, books)
            books.append({"isbn": node.isbn, "title": node.title, "user": node.user, "date": node.date})
            self._inorder_traversal(node.right, books)

# ===============================================
# AVL Tree
# =============================================== 
class AVLNode:
    def __init__(self, isbn, title, user, date): 
        self.isbn = isbn
        self.title = title
        self.user = user
        self.date = date
        self.left = None
        self.right = None
        self.height = 1   # Height property for balancing purposes

class AVLTree(BookManagerBase):
    def __init__(self):
        self.root = None

    # Utility function to get the height of the node
    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    # Utility function to get the balance factor of the node
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    # Right rotate utility to maintain AVL property
    def _right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        return x

    # Left rotate utility to maintain AVL property
    def _left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    # Function to add a book and maintain AVL balance
    def add_book(self, isbn, title, user, date):
        self.root = self._add_recursive(self.root, isbn, title, user, date)

    def _add_recursive(self, node, isbn, title, user, date):
        if not node:
            return AVLNode(isbn, title, user, date)
        if isbn < node.isbn:
            node.left = self._add_recursive(node.left, isbn, title, user, date)
        elif isbn > node.isbn:
            node.right = self._add_recursive(node.right, isbn, title, user, date)
        else:
            print("\nBook with this ISBN already exists.")
            return node

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Balance the node if necessary
        balance = self._get_balance(node)

        # Left heavy situation - Right rotation
        if balance > 1 and isbn < node.left.isbn:
            return self._right_rotate(node)

        # Right heavy situation - Left rotation
        if balance < -1 and isbn > node.right.isbn:
            return self._left_rotate(node)

        # Left-Right case - Left rotation followed by Right rotation
        if balance > 1 and isbn > node.left.isbn:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right-Left case - Right rotation followed by Left rotation
        if balance < -1 and isbn < node.right.isbn:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    # Function to remove a book and maintain AVL balance
    def remove_book(self, isbn=None):
        self.root, removed_book = self._delete_recursive(self.root, isbn)
        return removed_book

    def _delete_recursive(self, node, isbn):
        if not node:
            return node, None
        if isbn < node.isbn:
            node.left, removed_book = self._delete_recursive(node.left, isbn)
        elif isbn > node.isbn:
            node.right, removed_book = self._delete_recursive(node.right, isbn)
        else:
            removed_book = {"isbn": node.isbn, "title": node.title, "user": node.user, "date": node.date}
            if not node.left:
                return node.right, removed_book
            if not node.right:
                return node.left, removed_book
            min_node = self._min_value_node(node.right)
            node.isbn, node.title = min_node.isbn, min_node.title
            node.right, _ = self._delete_recursive(node.right, min_node.isbn)
        return node, removed_book

    # Helper function to find the node with the smallest value in the right subtree
    def _min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    # Function to search for a book in the AVL Tree
    def search_book(self, isbn=None, title=None):
        return self._search_recursive(self.root, isbn)

    def _search_recursive(self, node, isbn=None, title=None):
        if not node:
            return None
        if isbn == node.isbn:
            return {"isbn": node.isbn, "title": node.title, "user": node.user, "date": node.date}
        elif isbn < node.isbn:
            return self._search_recursive(node.left, isbn)
        else:
            return self._search_recursive(node.right, isbn)

    # Inorder traversal to get a sorted list of books
    def get_books(self):
        books = []
        self._inorder_traversal(self.root, books)
        return books

    def _inorder_traversal(self, node, books):
        if node:
            self._inorder_traversal(node.left, books)
            books.append({"isbn": node.isbn, "title": node.title, "user": node.user, "date": node.date})
            self._inorder_traversal(node.right, books)

# ===============================================
# CSV Manager (For Reading and Writing into CSV File)
# ===============================================
class CSVManager:
    def __init__(self, filename="books.csv"):
        self.filename = filename

    def load_books(self, book_manager):
        try:        #Attempts to open and read the CSV file
            with open(self.filename, mode='r') as file:     #Opens CSV file in read mode 'r'. The with statement ensures that the file is closed after reading.
                reader = csv.DictReader(file)
                for row in reader:          #Iterates over each row in the CSV file with the corresponding details.
                    book_manager.add_book(
    row['isbn'], 
    row['title'], 
    row.get('user', ''),  # If 'user' is missing, default to an empty string
    row.get('date', '')   # If 'date' is missing, default to an empty string
)
            print("\nBooks loaded from CSV.")
        except FileNotFoundError:       #If CSV file is not found, catch a FileNotFoundError.
            print("\nCSV file not found.")

    def save_books(self, book_manager):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['isbn', 'title', 'user', 'date'])
            writer.writeheader()
            writer.writerows(book_manager.get_books())
        print("\nBooks saved to CSV.")

# ===============================================
# User Interface Main Menu
# ===============================================
if __name__ == "__main__":
    print("\n+-------------------------------------------+")
    print("| Welcome to The Library Management System! |")
    print("|                                           |")
    print("| Please choose a data structure:           |")
    print("| 1. Static Array                           |")
    print("| 2. Dynamic Linked List                    |")
    print("| 3. Binary Search Tree (BST)               |")
    print("| 4. AVL Tree                               |")
    print("+-------------------------------------------+")

    while True:
        choice = input("> Enter 1, 2, 3 or 4: ").strip()
        if choice == "1":
            book_manager = StaticBookArray()
            break
        elif choice == "2":
            book_manager = DynamicBookLinkedList()
            break
        elif choice == "3":
            book_manager = BinarySearchTree()
            break
        elif choice == "4":
            book_manager = AVLTree()
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.")

    csv_manager = CSVManager()
    undo_redo = UndoRedoStack()
    csv_manager.load_books(book_manager)
    days_due = 14  # Define the number of days before a book is overdue

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
        print("| 4. Borrow Book                |")
        print("| 5. Display Borrow Queue       |")
        print("| 6. Display Overdue Books      |")        
        print("| 7. Return Book                |")
        print("| 8. Remove Book                |")
        print("| 9. Save Changes to CSV        |")
        print("| Z. Undo                       |")
        print("| X. Redo                       |")
        print("| Q. Quit                       |")
        print("+-------------------------------+")

        option = input("> Choose option: ").strip()

        if option == "1":
            print("\nBooks in the Library:")
            print("-------------------------------------------------------------------")
            print("ISBN            |       Title")
            print("-------------------------------------------------------------------")
            book_manager.display_books()
            print("-------------------------------------------------------------------")

        elif option == "2":
            isbn = input("\nEnter ISBN: ").strip()
            title = input("Enter Title: ").strip()
            user = input("Enter User (Enter if none): ").strip()
            date = input("Enter Date (YYYY-MM-DD)(Enter if none): ").strip()
            book_manager.add_book(isbn, title, user, date)
            undo_redo.push_undo({"type": "add", "isbn": isbn, "title": title, "user": user, "date": date})
            print("\nBook added successfully.")

        elif option == "3":
            # For BST or AVL Tree, search only by ISBN
            if isinstance(book_manager, BinarySearchTree) or isinstance(book_manager, AVLTree):
                isbn = input("Search by ISBN: ").strip()
                book = book_manager.search_book(isbn=isbn)
                if book:
                    print(f"\nBook found: {book['title']} (ISBN: {book['isbn']})")
                else:
                    print("\nBook not found.")
            
            # For StaticBookArray or DynamicBookLinkedList, search by ISBN or Title
            else:
                search_type = prompt_user("Search by ISBN or Title? (isbn/title): ", ["isbn", "title"])
                value = input(f"Enter {search_type.title()}: ").strip()
                book = book_manager.search_book(isbn=value if search_type == "isbn" else None, title=value if search_type == "title" else None)
                if book:
                    print(f"\nBook found: {book['title']} (ISBN: {book['isbn']})")
                else:
                    print("\nBook not found.")

        elif option == "4":
            user = input("> Enter your username: ").strip()
            search_type = prompt_user("Borrow a book. Search by ISBN or Title? (isbn/title): ", ["isbn", "title"])
            value = input(f"Enter {search_type.title()}: ").strip()
            book = book_manager.search_book(isbn=value if search_type == "isbn" else None, title=value if search_type == "title" else None)
            borrowed_books = book_manager.get_borrowed_books()
            if book:
                if book not in borrowed_books:
                    today = datetime.today()
                    today_str = today.strftime('%Y-%m-%d')
                    while True:
                        choice = input(f"\nConfirm to borrow '{book['title']}'? Y/N: ").strip().lower()
                        if choice == "y":
                            try:
                                book_manager.borrow_book(isbn=value if search_type == "isbn" else None,
                                                         title=value if search_type == "title" else None,
                                                         user=user, date=today_str)
                                print(f"\nYou have borrowed '{book['title']}'. Please make sure to return it in {days_due} days.")
                            except Exception as e:
                                if type(e).__name__ == 'AttributeError':
                                    print(f"Error in the borrow function (Implementation either has errors or does not exist for this data structure.)")
                                else:
                                    print(f"Error borrowing book: {str(e)}")                           
                            finally:
                                break
                        elif choice == "n":
                            print("\nBorrow canceled.")
                            break
                        else:
                            print("Invalid choice. Please enter Y/N.")
                else:
                    while True:
                        choice = input(f"\n'{book['title']}' is borrowed by another user. Would you like to reserve? Y/N: ").strip().lower()
                        if choice == "y":
                            try:
                                book_manager.borrow_book(isbn=value if search_type == "isbn" else None,
                                                         title=value if search_type == "title" else None,
                                                         user=user, date=today_str)
                                print(f"\nYou have reserved '{book['title']}'.")
                            except Exception as e:
                                if type(e).__name__ == 'AttributeError':
                                    print(f"Error in the reserve (borrow) function. Implementation either has errors or does not exist for this data structure.")
                                else:
                                    print(f"Error reserving book: {str(e)}")
                            finally:
                                break
                        elif choice == "n":
                            print("\nReserve canceled.")
                            break
                        else:
                            print("Invalid choice. Please enter Y/N.")
            else:
                print("\nBook not found.")

        elif option == '5':
            try:
                book_manager.display_borrow_queue()
            except Exception as e:
                if type(e).__name__ == 'AttributeError':
                    print(f"Error: The borrow queue is not implemented for this data structure.")
                else:
                    print(f"Error displaying the queue: {str(e)}")

        elif option == "6":
            print(book_manager.display_max_heap_overdue_books(days_due)) 

        elif option == "7":
            user = input("> Enter your username: ").strip()
            book_manager.display_user_borrowed_books(user)
            user_borrowed_books = book_manager.get_user_borrowed_books(user)
            if user_borrowed_books:
                value = input(f"Enter ISBN of the book to return: ").strip()
                book = book_manager.search_book(isbn=value, title=None)
                if book and book in user_borrowed_books:
                    try:
                        returned = book_manager.return_book(value, user)  # Pass user to return_book
                        if returned:
                            print(f"\nYou have returned {book['title']}.")
                        else:
                            print(f"\nError: Could not return the book. Please ensure the book was borrowed by you.")
                    except Exception as e:
                        if type(e).__name__ == 'AttributeError':
                            print(f"\nError: The return book function is not implemented or has errors for this data structure.")
                        else:
                            print(f"Error returning the book: {str(e)}")
            else:
                print("\nYou haven't borrowed any books.")

        elif option == "8":
            # If the data structure is Static Array or Dynamic Linked List, allow remove by ISBN or Title
            if isinstance(book_manager, StaticBookArray) or isinstance(book_manager, DynamicBookLinkedList):
                remove_type = prompt_user("Remove by ISBN or Title? (isbn/title): ", ["isbn", "title"])
                value = input(f"Enter {remove_type.title()}: ").strip()
                book = book_manager.search_book(isbn=value if remove_type == "isbn" else None, title=value if remove_type == "title" else None)
                if book_manager.remove_book(isbn=value if remove_type == "isbn" else None, title=value if remove_type == "title" else None):
                    undo_redo.push_undo({"type": "remove", "isbn": book['isbn'], "title": book['title']})
                    print("\nBook removed.")
                else:
                    print("\nBook not found.")
            # If the data structure is Binary Search Tree or AVL Tree, only allow remove by ISBN
            elif isinstance(book_manager, BinarySearchTree) or isinstance(book_manager, AVLTree):
                isbn = input("Enter ISBN to remove: ").strip()
                book = book_manager.search_book(isbn=isbn)
                if book_manager.remove_book(isbn=isbn):
                    undo_redo.push_undo({"type": "remove", "isbn": book['isbn'], "title": book['title']})
                    print("\nBook removed.")
                else:
                    print("\nBook not found.")

        elif option == "9":
            csv_manager.save_books(book_manager)

        elif option.lower() == "z":
            undo_redo.undo(book_manager)

        elif option.lower() == "x":
            undo_redo.redo(book_manager)

        elif option.lower() == "q":
            print("Exiting...")
            break

        elif option.lower() == "g":     #hidden function, to show max-heap structure of overdue books.
            print(book_manager.get_max_heap_overdue_books(days_due)) 
            
        else:
            print("\nInvalid option. Please choose a valid option from the menu.")
