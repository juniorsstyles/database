import sqlite3

# Connect to SQLite database (it will create it if it doesn't exist)
conn = sqlite3.connect('ebookstore.db')
c = conn.cursor()

# Create the book table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS book (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    qty INTEGER NOT NULL
)
''')

# Function to populate the table with initial data
def populate_initial_data():
    initial_books = [
        (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
        (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
        (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
    ]
    # Insert initial data
    c.executemany('INSERT OR IGNORE INTO book VALUES (?, ?, ?, ?)', initial_books)
    conn.commit()

# Function to add a new book
def add_book():
    title = input("Enter the book title: ")
    author = input("Enter the author: ")
    qty = int(input("Enter the quantity: "))
    c.execute('INSERT INTO book (title, author, qty) VALUES (?, ?, ?)', (title, author, qty))
    conn.commit()
    print("Book added successfully!")

# Function to update a book's information
def update_book():
    id = int(input("Enter the book ID to update: "))
    title = input("Enter the new title (or press Enter to keep current): ")
    author = input("Enter the new author (or press Enter to keep current): ")
    qty = input("Enter the new quantity (or press Enter to keep current): ")
    if title:
        c.execute('UPDATE book SET title = ? WHERE id = ?', (title, id))
    if author:
        c.execute('UPDATE book SET author = ? WHERE id = ?', (author, id))
    if qty:
        c.execute('UPDATE book SET qty = ? WHERE id = ?', (qty, id))
    conn.commit()
    print("Book updated successfully!")

# Function to delete a book
def delete_book():
    id = int(input("Enter the book ID to delete: "))
    c.execute('DELETE FROM book WHERE id = ?', (id,))
    conn.commit()
    print("Book deleted successfully!")

# Function to search for a book
def search_books():
    keyword = input("Enter a keyword to search for (title/author): ")
    c.execute("SELECT * FROM book WHERE title LIKE ? OR author LIKE ?", ('%' + keyword + '%', '%' + keyword + '%'))
    results = c.fetchall()
    if results:
        for row in results:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Quantity: {row[3]}")
    else:
        print("No books found.")

# Function to display the menu
def display_menu():
    print("\nMenu:")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit")

# Function to handle user's menu choice
def handle_choice(choice):
    if choice == '1':
        add_book()
    elif choice == '2':
        update_book()
    elif choice == '3':
        delete_book()
    elif choice == '4':
        search_books()
    elif choice == '0':
        print("Goodbye!")
        return False
    else:
        print("Invalid choice! Please select a valid option.")
    return True

# Main program loop
def main():
    populate_initial_data()
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if not handle_choice(choice):
            break

if __name__ == "__main__":
    main()

# Close the connection when done
conn.close()
