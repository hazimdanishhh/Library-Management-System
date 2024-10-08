## README: Library Management System with Stack-Based Undo/Redo

Project Title:
Library Management System (with Stack-Based Undo/Redo)

---

Overview:
This project is a scalable Library Management System designed to manage books using both static (array-based) and dynamic (linked-list-based) data structures. It also includes a stack-based Undo/Redo system for managing the addition and removal of books. The system can load and save book records from a CSV file, making it persistent between sessions.

---

Key Features:

1. Static and Dynamic Data Structures:

   - Users can choose between a static array and a dynamic linked list for managing book records.
   - The static array has a fixed capacity, while the linked list allows flexible additions and removals.

2. Book Management:

   - Add Book: Add a new book by entering its ISBN and title.
   - Search Book: Search for a book by its ISBN or title.
   - Remove Book: Remove a book from the system by ISBN or title.
   - Display Books: View all books currently stored in the system.

3. Undo/Redo System:

   - Undo: Undo the last add or remove action, using an array-based stack to store up to 10 actions.
   - Redo: Redo the last undone action, moving actions between the undo and redo stacks.

4. CSV File Integration:
   - Save to CSV: Save the current list of books to a books.csv file.
   - Load from CSV: Load books from the books.csv file into the system at startup.

---

Technologies Used:

- Programming Language: Python
- Data Structures: Array, Linked List, Stack (Array-based)
- File Handling: CSV for persistent book storage

---

Setup Instructions:

1.  Clone the Repository:

        git clone <repository_url>

2.  Install Python: Ensure Python is installed on your machine. This project is compatible with Python 3.x.

3.  Run the Program:

    - Open a terminal/command prompt.
    - Navigate to the directory containing the program file.
    - Run the following command:

      python LibraryManagementSystem.py

---

User Instructions:

1. Choosing a Data Structure:

   - When the program starts, you will be prompted to choose between a static array and a dynamic linked list for managing books. Enter 1 for the array or 2 for the linked list.

2. Main Menu Options:

   - Add Book: Enter 1 to add a new book by ISBN and title.
   - Search Book: Enter 2 to search for a book by ISBN or title.
   - Remove Book: Enter 3 to remove a book by ISBN or title.
   - Display Books: Enter 4 to view all books in the system.
   - Save to CSV: Enter 5 to save the current list of books to a CSV file.
   - Load from CSV: Enter 6 to load books from an existing CSV file.
   - Undo: Enter 7 to undo the last add/remove action.
   - Redo: Enter 8 to redo the last undone action.
   - Exit: Enter 9 to exit the program.

3. Undo/Redo Behavior:
   - The system stores up to the last 10 actions for undo/redo functionality. When an action is undone, it moves to the redo stack and can be re-applied.

---

CSV File Format:

- The program reads and writes book data in CSV format with the following structure:

        isbn,title
        123456789,The Great Gatsby
        987654321,To Kill a Mockingbird

- Make sure that the CSV file adheres to this format for the program to correctly load and save book data.

---

Example Usage:

1. Add a Book:

   - Select "Add Book" from the menu and input an ISBN and title, e.g., ISBN: 123456789, Title: Harry Potter.

2. Undo Last Action:

   - After adding the book, you can undo the action by selecting "Undo" from the menu. The system will remove the last added book.

3. Redo Last Action:

   - If you undo the addition of a book, you can redo it by selecting "Redo," and the book will be added back.

4. Save to CSV:
   - After managing books, you can save the current list of books by choosing the "Save to CSV" option. The data will be stored in books.csv.

---

Future Enhancements:
This system is designed to be scalable, allowing future additions such as:

- Queue-based Reservation System: Implementing a queue to handle book reservations.
- Heap-based Priority for Overdue Books: Implementing a heap to prioritize overdue books dynamically.
- Graphical User Interface (GUI): Adding a user-friendly GUI for easier interaction.
