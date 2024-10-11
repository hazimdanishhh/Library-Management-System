import csv

# ===============================================
# Base class for Book Management (abstracts common logic for both Static and Dynamic Data Structures)
# ===============================================
class BookManagerBase:
    def search_book(self, isbn=None, title=None):
        for book in self.get_books():   #Loop through each book and check if its isbn or title matches the given search criteria
            if isbn and book['isbn'] == isbn:   #If both conditions are true, it means the book with the matching ISBN was found, and returns the book.
                return book
            if title and book['title'].lower() == title.lower():    #If the title matches, it returns the book.
                return book
        return None     #If no book is found that matches either the ISBN or title, no matching book was found and returns None.

    def display_books(self):
        books = self.get_books()
        if not books:       #Checks if the books list is empty or None
            print("\nNo books available.")
        else:
            for book in books:      #Loop through each book in books list and prints each book.
                print(f"{book['isbn']}\t|\t{book['title']}")

    def get_books(self):        #Placeholder method to be overridden by subclasses that inherit from this Base class, and return list of books.
        raise NotImplementedError       #If a subclass does not override this method, it will give an error. This forces subclasses to define their own specific way of getting a list of books (Static or Dynamic)

# ===============================================
# Static Data Structure: Array (Max capacity of 100)
# ===============================================
class StaticBookArray(BookManagerBase):     #This class inherits from BookManagerBase and has access to the methods defined in its parent, such as (search_book, display_books).
    def __init__(self, capacity=100):       #Constructor method, book array with max capacity of 100 books.
        self.capacity = capacity        #Stores value of capacity in the instance variable.
        self.books = []                 #Initialize an empty list to store the books.
    
    def add_book(self, isbn, title):
        if len(self.books) < self.capacity:     #If length of array is less than capacity, append the new book to the books array.
            self.books.append({"isbn": isbn, "title": title})
        else:       #Else, the array will not accept any more books as it is full.
            print("\nLibrary is full.")

    def remove_book(self, isbn=None, title=None):
        book = self.search_book(isbn, title)        #Calls search_book method inherited from BookManagerBase and stores in book variable.
        if book:        #If book is found and not None, remove the book from the books array.
            self.books.remove(book)
            return True
        return False

    def get_books(self):        #Defined function to override base class method from BookManagerBase, and returns the list of books stored in self.books array.
        return self.books

# ===============================================
# Dynamic Data Structure: Linked List
# ===============================================
class Node:         #Defines class Node that represents a node in a linked list. Each node will store a book's details (isbn, title), and a reference (next) to the next node in the list.
    def __init__(self, isbn, title):        #Constructor method to initialize a new node with a book's isbn and title.
        self.isbn = isbn
        self.title = title
        self.next = None

class DynamicBookLinkedList(BookManagerBase):       #Class inherited from BookManagerBase, and manages the books as a linked list of Node objects.
    def __init__(self):
        self.head = None        #Initialize the linked list by setting its head (first node in the linked list) to None.

    def add_book(self, isbn, title):
        new_node = Node(isbn, title)        #Create a new_node object using the provided isbn and title.
        if not self.head:           #Check if linked list is empty
            self.head = new_node        #If the linked list is empty, the new node is set as the head of the linked list.
        else:
            current = self.head     #If the linked list is not empty, sets the variable current to point to the first node in the linked list (head).
            while current.next:     #Loop through the linked list until the last node (node with next pointer = None).
                current = current.next      #Moves variable current to next node in the linked list.
            current.next = new_node     #After loop finds the last node, sets the next pointer of that last node to the new node; adding a new book to the end of the linked list.

    def remove_book(self, isbn=None, title=None):
        current, prev = self.head, None         #Initialize two variables; current = self.head (point to first node), and prev = None (keep track of previous node in the list, initialized to None)
        while current:      #Loop through the linked list until current = None (reaches the end of the list).
            if (isbn and current.isbn == isbn) or (title and current.title.lower() == title.lower()):       #If either condition is True, remove the current node.
                if prev:        #Checks if current node is not the head node.
                    prev.next = current.next        #Removes the current node by changing the pointer of the previous node (prev) to point to the next node (current.next).
                else:
                    self.head = current.next        #Else if current node is the head, removes the current node and setting the head to point to the next node in the list.
                return True
            prev, current = current, current.next       #Traverse forward in the linked list, continue checking the next node and reiterates the above.
        return False

    def get_books(self):
        books = []          #Initialize empty books list.
        current = self.head     #Sets current to head of the list.
        while current:      #Traverse through the list until current = None,
            books.append({"isbn": current.isbn, "title": current.title})        #Appends the current node's isbn and title to the books list.
            current = current.next      #Move forward in the list.
        return books        #Return books list.

# ===============================================
# Stack-based Undo/Redo System (Array-Based) Currently only for Adding and Removing books
# ===============================================
class UndoRedoStack:
    def __init__(self, limit=10):
        self.undo_stack = []        #Initialize empty list that will store actions that can be undone.
        self.redo_stack = []        #Initialize empty list that will store actions that can be redone.
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
            book_manager.add_book(action['isbn'], action['title'])      #Calls add_book method, adds the recently removed book.
            self.push_redo(action)      #Move this action to redo stack.
            print(f"\nUndo: Re-added book {action['isbn']}")

    def redo(self, book_manager):       #This method performs the redo operation.
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
# Binary Tree-based Book Search (BST)
# ===============================================
class BSTNode:
    def __init__(self, isbn, title):
        self.isbn = isbn
        self.title = title
        self.left = None
        self.right = None

class BinarySearchTree(BookManagerBase):
    def __init__(self):
        self.root = None

    def add_book(self, isbn, title):
        self.root = self._add_recursive(self.root, isbn, title)

    def _add_recursive(self, node, isbn, title):
        if not node:
            return BSTNode(isbn, title)
        if isbn < node.isbn:
            node.left = self._add_recursive(node.left, isbn, title)
        elif isbn > node.isbn:
            node.right = self._add_recursive(node.right, isbn, title)
        else:
            print("\nBook with this ISBN already exists.")
        return node

    def remove_book(self, isbn=None, title=None):
        self.root, removed_book = self._delete_recursive(self.root, isbn, title)
        return removed_book

    def _delete_recursive(self, node, isbn=None, title=None):
        if not node:
            return node, None
        if isbn and isbn < node.isbn:
            node.left, removed_book = self._delete_recursive(node.left, isbn)
        elif isbn and isbn > node.isbn:
            node.right, removed_book = self._delete_recursive(node.right, isbn)
        elif isbn == node.isbn or title.lower() == node.title.lower():
            removed_book = {"isbn": node.isbn, "title": node.title}
            if not node.left: return node.right, removed_book
            if not node.right: return node.left, removed_book
            min_node = self._min_value_node(node.right)
            node.isbn, node.title = min_node.isbn, min_node.title
            node.right, _ = self._delete_recursive(node.right, min_node.isbn)
        elif title and title.lower() < node.title.lower():
            node.left, removed_book = self._delete_recursive(node.left, isbn, title)
        else:
            node.right, removed_book = self._delete_recursive(node.right, isbn, title)
        return node, removed_book

    def _min_value_node(self, node):
        while node.left: node = node.left
        return node

    def search_book(self, isbn=None, title=None):
        return self._search_recursive(self.root, isbn, title)

    def _search_recursive(self, node, isbn=None, title=None):
        if not node:
            return None
        if isbn == node.isbn or (title and title.lower() == node.title.lower()):
            return {"isbn": node.isbn, "title": node.title}
        if isbn and isbn < node.isbn:
            return self._search_recursive(node.left, isbn, title)
        if title and title.lower() < node.title.lower():
            return self._search_recursive(node.left, isbn, title)
        return self._search_recursive(node.right, isbn, title)

    def get_books(self):
        books = []
        self._inorder_traversal(self.root, books)
        return books

    def _inorder_traversal(self, node, books):
        if node:
            self._inorder_traversal(node.left, books)
            books.append({"isbn": node.isbn, "title": node.title})
            self._inorder_traversal(node.right, books)

# FIX AVL TREE
# PROBLEMS WITH REMOVE BY TITLE AND SEARCH BY TITLE FOR NEWLY ADDED BOOKS

# ===============================================
# AVL Tree
# =============================================== 
class AVLNode:
    def __init__(self, isbn, title):
        self.isbn = isbn
        self.title = title
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
    def add_book(self, isbn, title):
        self.root = self._add_recursive(self.root, isbn, title)

    def _add_recursive(self, node, isbn, title):
        if not node:
            return AVLNode(isbn, title)
        if isbn < node.isbn:
            node.left = self._add_recursive(node.left, isbn, title)
        elif isbn > node.isbn:
            node.right = self._add_recursive(node.right, isbn, title)
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
    def remove_book(self, isbn=None, title=None):
        self.root, removed_book = self._delete_recursive(self.root, isbn, title)
        return removed_book

    def _delete_recursive(self, node, isbn=None, title=None):
        if not node:
            return node, None

        # Traverse the tree based on ISBN or title
        if isbn and isbn < node.isbn:
            node.left, removed_book = self._delete_recursive(node.left, isbn, title)
        elif isbn and isbn > node.isbn:
            node.right, removed_book = self._delete_recursive(node.right, isbn, title)
        elif (isbn and isbn == node.isbn) or (title and title.lower() == node.title.lower()):
            removed_book = {"isbn": node.isbn, "title": node.title}
            # Node has at most one child
            if not node.left:
                return node.right, removed_book
            if not node.right:
                return node.left, removed_book
            # Node has two children, find the in-order successor (minimum in the right subtree)
            min_node = self._min_value_node(node.right)
            node.isbn, node.title = min_node.isbn, min_node.title
            node.right, _ = self._delete_recursive(node.right, min_node.isbn)

        elif title and title.lower() < node.title.lower():
            node.left, removed_book = self._delete_recursive(node.left, isbn, title)
        else:
            node.right, removed_book = self._delete_recursive(node.right, isbn, title)

        # Balance the AVL tree after deletion
        if not node:
            return node, removed_book

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Left heavy - Right rotation
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node), removed_book
        # Left-Right case - Left rotation followed by Right rotation
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node), removed_book
        # Right heavy - Left rotation
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node), removed_book
        # Right-Left case - Right rotation followed by Left rotation
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node), removed_book

        return node, removed_book

    # Helper function to find the node with the smallest value in the right subtree
    def _min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    # Function to search for a book in the AVL Tree
    def search_book(self, isbn=None, title=None):
        return self._search_recursive(self.root, isbn, title)

    def _search_recursive(self, node, isbn=None, title=None):
        if not node:
            return None
        # Match ISBN or Title (case-insensitive for title)
        if (isbn and isbn == node.isbn) or (title and title.lower() == node.title.lower()):
            return {"isbn": node.isbn, "title": node.title}
        
        # Continue traversing the tree based on ISBN or title
        if isbn and isbn < node.isbn:
            return self._search_recursive(node.left, isbn, title)
        if title and title.lower() < node.title.lower():
            return self._search_recursive(node.left, isbn, title)
        return self._search_recursive(node.right, isbn, title)

    # Inorder traversal to get a sorted list of books
    def get_books(self):
        books = []
        self._inorder_traversal(self.root, books)
        return books

    def _inorder_traversal(self, node, books):
        if node:
            self._inorder_traversal(node.left, books)
            books.append({"isbn": node.isbn, "title": node.title})
            self._inorder_traversal(node.right, books)

# ===============================================
# CSV Manager (For Reading and Writing into CSV File)
# ===============================================
class CSVManager:
    def __init__(self, filename="books.csv"):
        self.filename = filename

    def load_books(self, book_manager):
        try:        #Attempts to open and read the CSV file
            with open(self.filename, mode='r') as file:     #Opens CSV file in read mode 'r', and the with statement ensures that the file is closed after reading.
                reader = csv.DictReader(file)
                for row in reader:          #Iterates over each row in the CSV file with the corresponding isbn and title.
                    book_manager.add_book(row['isbn'], row['title'])
            print("\nBooks loaded from CSV.")
        except FileNotFoundError:       #If CSV file is not found, catch a FileNotFoundError.
            print("\nCSV file not found.")

    def save_books(self, book_manager):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['isbn', 'title'])
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
        if choice == "2":
            book_manager = DynamicBookLinkedList()
            break
        if choice == "3":
            book_manager = BinarySearchTree()
            break
        elif choice == "4":
            book_manager = AVLTree()
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, 3 or 4.")

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
            print("ISBN            |       Title")
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
