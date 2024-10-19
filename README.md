## README: Library Management System

Project Title:
Library Management System - Assignment 1: ITWB2043 Algorithms & Data Structures

---

Overview:
This project is a scalable Library Management System designed to efficiently handle key operations such as book addition, borrowing, and management of users and overdue books. The system employs different data structures for managing book inventories, reservations, and borrowing history, ensuring scalability and efficiency.

The system supports:

- Static and Dynamic data structures.
- Stack-based Undo/Redo system for book management.
- Binary Search Tree (BST) and AVL Tree for optimized book searches based on ISBN.
- Queue-based book reservations and heap-based priority for overdue books.

---

Key Features:

1. Static and Dynamic Data Structures for Book Management:

   - Static Array (Capacity Limited): Fixed-capacity array-based system for storing books.
   - Dynamic Linked List: Flexible, dynamic system that allows additions and removals of books.

   Operations:

   - Add Book: Add a new book by ISBN and title.
   - Search Book: Search for books by ISBN or title.
   - Remove Book: Remove books by ISBN or title.
   - Display Books: View all available books.

2. Stack-Based Undo/Redo System:

   - Undo: Reverse the last action (add/remove).
   - Redo: Reapply the last undone action.
   - Uses a stack (array-based) to store up to the last 10 actions.

3. Queue-Based Reservation System:

   - Users can reserve books when they are already borrowed.
   - Reservations are managed in a first-come, first-served queue.

4. Binary Search Tree (BST) for ISBN-Based Book Management:

   - Books are organized and searchable by ISBN using a binary search tree.
   - Supports efficient insertion, deletion, and searching by ISBN only.

5. AVL Tree for Optimized ISBN-Based Book Search:

   - Self-balancing AVL Tree ensures optimized searches for large inventories.
   - Supports searching, insertion, and deletion based only on ISBN.

6. Heap-Based Priority for Overdue Books:

   - Overdue books are managed using a max-heap.
   - Prioritizes books that are overdue by the most days for return notifications.

7. CSV File Integration:

   - Save to CSV: Save the current list of books in books.csv.
   - Load from CSV: Load books from the books.csv file on startup.

---

Technologies Used:

- Programming Language: Python
- Data Structures: Array, Linked List, Stack (Array-based), Queue, Binary Search Tree, AVL Tree, Heap
- File Handling: CSV for book database

---

Setup Instructions:
```
1.  Clone the Repository:

        git clone https://github.com/hazimdanishhh/Library-Management-System.git

2.  Install Python: Ensure Python is installed on your machine. This project is compatible with Python 3.x.

3.  Install requirements module : pip install -r requirements.txt

4.  Run the Program:

    - Open a terminal/command prompt.
    - Navigate to the directory containing the program file.
    - Run the following command:

      python LibraryManagementSystem.py
```

---

Program Usage:

Main Menu Options:

- Display All Books: View all books available in the system.
- Add Book: Add a new book by entering its ISBN, title, user (if borrowed), and date.
- Search Book:
  - Static Array/Dynamic Linked List: Search by ISBN or title.
  - Binary Search Tree (BST) and AVL Tree: Search only by ISBN.
- Borrow Book: Borrow a book by ISBN or title (only if not borrowed).
- Return Book: Return a borrowed book by entering ISBN and user.
- Display Borrow Queue: View the reservation queue for books.
- Display Overdue Books: Display overdue books with priority.
- Undo/Redo: Undo or redo the last action.
- Save Changes: Save the current books to a CSV file.
- Quit: Exit the program.

Search Behavior:

- Static Array and Dynamic Linked List: Search by both ISBN and title.
- BST and AVL Tree: Search only by ISBN (as per tree structure optimization).

---

CSV File Format:

- The program reads and writes book data in CSV format with the following structure:

        isbn,title,user,date
        123456789,The Great Gatsby,James,2024-09-25
        987654321,To Kill a Mockingbird,,    #No user or date if not borrowed

- Make sure that the CSV file adheres to this format for the program to correctly load and save book data.

---

Example Usage:

1. Static Array (Array-Based Book Management)

   - Add a Book:

     Select Static Array from the menu (Option 1).
     Choose Add Book from the main menu (Option 2).
     Enter ISBN: 111111111
     Enter Title: Data Structures in Python
     Enter User (optional, if borrowed): (Leave blank)
     Enter Date (optional, if borrowed): (Leave blank)
     Result: The book is added to the static array-based inventory.

   - Search by ISBN/Title:

     Choose Search Book from the main menu (Option 3).
     Select Search by Title.
     Enter the title: Data Structures in Python.
     Result: The book details are displayed.

   - Remove a Book:

     Choose Remove Book (Option 8).
     Search by ISBN or title and remove the book.

   - Undo/Redo:

     After adding/removing a book, you can undo the action (Option Z) or redo it (Option X).

2. Dynamic Linked List (Linked List-Based Book Management)

   - Add a Book:

     Select Dynamic Linked List from the menu (Option 2).
     Choose Add Book from the main menu (Option 2).
     Enter ISBN: 222222222
     Enter Title: Introduction to Algorithms
     Enter User (optional, if borrowed): (Leave blank)
     Enter Date (optional, if borrowed): (Leave blank)
     Result: The book is dynamically added to the linked list.

   - Search by ISBN/Title:

     Choose Search Book from the main menu (Option 3).
     Select Search by ISBN or Search by Title.
     Enter the search criteria, e.g., ISBN: 222222222.
     Result: The book is found and displayed.

   - Remove a Book:

     Choose Remove Book from the main menu (Option 8).
     Remove the book using either its ISBN or title.

   - Undo/Redo:

     After adding/removing a book, use Undo (Option Z) or Redo (Option X) to reverse/restore the action.

3. Binary Search Tree (BST - ISBN-Based Management Only)

   - Add a Book:

     Select Binary Search Tree (BST) from the menu (Option 3).
     Choose Add Book (Option 2).
     Enter ISBN: 333333333
     Enter Title: The Art of Computer Programming
     Enter User (optional, if borrowed): (Leave blank)
     Enter Date (optional, if borrowed): (Leave blank)
     Result: The book is added to the BST using its ISBN as the key.

   - Search by ISBN:

     Choose Search Book from the main menu (Option 3).
     Enter ISBN: 333333333.
     Result: The book is found using the ISBN search.

   - Remove a Book by ISBN:

     Choose Remove Book from the main menu (Option 8).
     Enter ISBN: 333333333.
     Result: The book is removed from the BST.

   - Undo/Redo:

     Use Undo (Option Z) to reverse the last action or Redo (Option X) to restore it.

4. AVL Tree (Self-Balancing Tree for ISBN Search)

   - Add a Book:

     Select AVL Tree from the menu (Option 4).
     Choose Add Book (Option 2).
     Enter ISBN: 444444444
     Enter Title: Clean Code
     Enter User (optional, if borrowed): (Leave blank)
     Enter Date (optional, if borrowed): (Leave blank)
     Result: The book is added to the AVL Tree, and the tree is balanced after insertion.

   - Search by ISBN:

     Choose Search Book from the main menu (Option 3).
     Enter ISBN: 444444444.
     Result: The book is found using the ISBN.

   - Remove a Book by ISBN:

     Choose Remove Book from the main menu (Option 8).
     Enter ISBN: 444444444.
     Result: The book is removed from the AVL Tree, and the tree is rebalanced after removal.

   - Undo/Redo:

     After adding/removing a book, you can Undo (Option Z) or Redo (Option X) the last action.

---

Future Enhancements:
This system is designed to be scalable, allowing future additions such as:

- Graphical User Interface (GUI): Adding a user-friendly GUI for easier interaction.
