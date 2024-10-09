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
                print(f"{book['isbn']}        {book['title']}")

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
# Implement the binary search tree 
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
        if not self.root:
            self.root = BSTNode(isbn, title)
        else:
            self._add(self.root, isbn, title)

    def _add(self, node, isbn, title):
        if isbn < node.isbn:
            if node.left:
                self._add(node.left, isbn, title)
            else:
                node.left = BSTNode(isbn, title)
        else:
            if node.right:
                self._add(node.right, isbn, title)
            else:
                node.right = BSTNode(isbn, title)

    def insert(self, isbn, title):
        if self.root is None:
            self.root = BSTNode(isbn, title)
        else:
            self._insert_recursive(self.root, isbn, title)

    def _insert_recursive(self, node, isbn, title):
        if isbn < node.isbn:
            if node.left is None:
                node.left = BSTNode(isbn, title)
            else:
                self._insert_recursive(node.left, isbn, title)
        elif isbn > node.isbn:
            if node.right is None:
                node.right = BSTNode(isbn, title)
            else:
                self._insert_recursive(node.right, isbn, title)

    def search_book(self, isbn=None, title=None):
        if isbn:
            return self._search_recursive(self.root, isbn)
        return None

    def _search_recursive(self, node, isbn):
        if node is None or node.isbn == isbn:
            return node
        if isbn < node.isbn:
            return self._search_recursive(node.left, isbn)
        return self._search_recursive(node.right, isbn)

    def delete(self, isbn):
        self.root = self._delete_recursive(self.root, isbn)

    def _delete_recursive(self, node, isbn):
        if node is None:
            return node
        if isbn < node.isbn:
            node.left = self._delete_recursive(node.left, isbn)
        elif isbn > node.isbn:
            node.right = self._delete_recursive(node.right, isbn)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._find_min(node.right)
            node.isbn, node.title = temp.isbn, temp.title
            node.right = self._delete_recursive(node.right, temp.isbn)
        return node

    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

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
# Implement the AVL tree
# =============================================== 
class AVLNode:
    def __init__(self, isbn, title):
        self.isbn = isbn
        self.title = title
        self.left = None
        self.right = None
        self.height = 1

class AVLTree(BookManagerBase):
    def __init__(self):
        self.root = None

    def add_book(self, isbn, title):
        self.root = self._add(self.root, isbn, title)

    def _add(self, node, isbn, title):
        if not node:
            return AVLNode(isbn, title)
        elif isbn < node.isbn:
            node.left = self._add(node.left, isbn, title)
        else:
            node.right = self._add(node.right, isbn, title)

        # Update the height of the ancestor node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Get the balance factor
        balance = self.get_balance(node)

        # Perform rotations to balance the tree
        if balance > 1 and isbn < node.left.isbn:
            return self.right_rotate(node)

        if balance < -1 and isbn > node.right.isbn:
            return self.left_rotate(node)

        if balance > 1 and isbn > node.left.isbn:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        if balance < -1 and isbn < node.right.isbn:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # Helper functions for rotation and balance checks
    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def insert(self, isbn, title):
        self.root = self._insert(self.root, isbn, title)

    def _insert(self, node, isbn, title):
        if not node:
            return AVLNode(isbn, title)
        if isbn < node.isbn:
            node.left = self._insert(node.left, isbn, title)
        elif isbn > node.isbn:
            node.right = self._insert(node.right, isbn, title)
        else:
            return node

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and isbn < node.left.isbn:
            return self._rotate_right(node)

        # Right Right Case
        if balance < -1 and isbn > node.right.isbn:
            return self._rotate_left(node)

        # Left Right Case
        if balance > 1 and isbn > node.left.isbn:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Left Case
        if balance < -1 and isbn < node.right.isbn:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def search_book(self, isbn=None, title=None):
        if isbn:
            return self._search(self.root, isbn)
        return None

    def _search(self, node, isbn):
        if not node or node.isbn == isbn:
            return node
        if isbn < node.isbn:
            return self._search(node.left, isbn)
        return self._search(node.right, isbn)

    def delete(self, isbn):
        self.root = self._delete(self.root, isbn)

    def _delete(self, node, isbn):
        if not node:
            return node

        if isbn < node.isbn:
            node.left = self._delete(node.left, isbn)
        elif isbn > node.isbn:
            node.right = self._delete(node.right, isbn)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            temp = self._get_min_value_node(node.right)
            node.isbn, node.title = temp.isbn, temp.title
            node.right = self._delete(node.right, temp.isbn)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

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
            book_manager = BinarySearchTree()
            break
        elif choice == "2":
            book_manager = AVLTree()
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
