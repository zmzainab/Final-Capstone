# Practice working with database - Program to be used by a bookstore clerk

from tabulate import tabulate  # Importing 'tabulate' to display a list of books
import sqlite3  # Importing sqlite3 to create and manipulate database

# Creating 'ebookstore' database under 'db' variable
# Creating a cursor object to execute SQL statements
db = sqlite3.connect('ebookstore')
cursor = db.cursor()


# Creates a table called 'books', Using 'COUNT(*)' to check if table is empty, and populating it with book data
def create_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, 
        title, author, quantity)
    ''')
    cursor.execute('''SELECT COUNT(*) FROM books''')
    row_qty = cursor.fetchall()[0][0]

    if row_qty == 0:
        cursor.execute('''INSERT INTO books
            VALUES(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
            (3002, 'Harry Potter and the Philosophers Stone', 'J.K. Rowling', 40),
            (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
            (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
            (3005, 'Alice in Wonderland', 'Lewis Caroll', 12);
        ''')


# Creates a new entry inside 'books' table
# 'try/except' to check for correct int entry. Checking if title already exists.
def enter_book():
    while True:
        entry_exists = False
        max_id = cursor.execute('''SELECT MAX(id) FROM books''')
        new_id = max_id.fetchone()[0] + 1
        new_author = input("Please enter the Authors Name: ")
        new_title = input("Please enter the Book Title: ")

        try:
            new_qty = int(input("Please enter the quantity of books (numbers only):"))
        except ValueError:
            print("Incorrect entry, please try again - Remember numbers only.")
            break

        # Checking if entry already exists
        for row in cursor.execute('''SELECT title FROM books'''):
            if row[0] == new_title:
                entry_exists = True

        if entry_exists:
            print("There's already a book with such title, Please try again.")
            break
        else:
            cursor.execute(f'''INSERT INTO books
                VALUES({new_id}, '{new_title}', '{new_author}', {new_qty});
            ''')
            db.commit()
            break


# Function to choose a book from the list of ids, 'try/except' to catch incorrect value error.
def choose_book():
    view_all()
    try:
        edit_id = int(input("\nPlease enter book's id (numbers only): "))
        cursor.execute(f'''SELECT id FROM books WHERE id = {edit_id}''')
        id_check = cursor.fetchone()
        return id_check
    except ValueError:
        print("\nPlease try again - Remember ID should be a number.\n")


# Function to display book you would like to update from the store and request inputs depending on user's choice.
def edit_book(book_id):
    while True:
        user_choice = int(input("""\nPlease choose what you would like to update:
1\t-\tTitle
2\t-\tAuthor
3\t-\tQuantity
0\t-\tExit
: """))
        if user_choice == 1:
            new_title = input("Please enter the updated new book title: ")
            cursor.execute(f'''UPDATE books SET title = "{new_title}" WHERE id = {book_id}''')

        elif user_choice == 2:
            new_auth = input("Please enter the updated authors name: ")
            cursor.execute(f'''UPDATE books SET author = "{new_auth}" WHERE id = {book_id}''')

        elif user_choice == 3:
            try:
                new_qty = int(input("Please enter the new quantity (numbers only): "))
                cursor.execute(f'''UPDATE books SET quantity = {new_qty} WHERE id = {book_id}''')
            except ValueError:
                print("Incorrect entry, please try again - Remember numbers only.")
                break

        elif user_choice == 0:
            db.commit()
            break


# Updates a book by verifying if the book already exists - with the book id - Using function choose_book
# If book doesn't exist - then it begins the update with the edit_book function.
def update_book():
    id_check = choose_book()
    if id_check is not None:
        edit_book(id_check[0])
    else:
        print("Incorrect entry, Please check ID properly and try again.")


# Deletes a book from the database
def delete_book():
    id_check = choose_book()
    if id_check is not None:
        cursor.execute(f'''SELECT title FROM books WHERE id = {id_check[0]}''')
        book_title = cursor.fetchone()
        cursor.execute(f'''DELETE FROM books WHERE id = {id_check[0]}''')
        print(f"\nBook called \'{book_title[0]}\' has been deleted from the database.")
    else:
        print("There's no such book, Please check ID properly and try again.")


# Function to find a book by 'author' or 'title'.
def search_book():
    while True:
        user_choice = int(input("""\nHow would you like to search for the book you are looking for:
1\t-\tTitle
2\t-\tAuthor
0\t-\tExit
: """))
        if user_choice == 1:
            search_title = input("Please enter a books title: ")
            search_results('title', search_title)

        elif user_choice == 2:
            search_auth = input("Please enter an books author: ")
            search_results('author', search_auth)

        elif user_choice == 0:
            db.commit()
            break


# Function to find results in the table and print them using tabulate.
def search_results(search_option, search_entry):
    print("\nThese are results:\n")
    cursor.execute(f'''SELECT * FROM books WHERE {search_option} = "{search_entry}"''')
    book_results = cursor.fetchall()
    print_table(book_results)


# Function to print all table content using 'tabulate'
def view_all():
    cursor.execute('''SELECT * FROM books''')
    book_list = cursor.fetchall()
    print_table(book_list)


# Function to use tabulate to print a table that is passed as an argument
def print_table(print_item):
    print(tabulate(
        print_item, headers=['ID', 'Title', 'Author', 'Qty'],
        tablefmt="fancy_grid"))


# Function to display main menu and request user's input and close database if user chooses to 'exit'
def main_menu():
    while True:
        try:

            user_choice = int(input("""\nWelcome to the online HyperionDev-Bookstore
1\t-\tEnter new book
2\t-\tUpdate book
3\t-\tDelete book
4\t-\tSearch book
5\t-\tView all books available
0\t-\tExit
Please enter appropriate task: """))
            if user_choice == 1:
                enter_book()

            elif user_choice == 2:
                update_book()

            elif user_choice == 3:
                delete_book()

            elif user_choice == 4:
                search_book()

            elif user_choice == 5:
                view_all()

            elif user_choice == 0:
                db.commit()
                db.close()
                print("\nThank you Goodbye")
                break
            else:
                print("Oops Wrong Choice, Pls Try again...")
        except ValueError:
            print("\nPlease try again - Remember Entry should be a number from the menu options.\n")


create_db()
main_menu()