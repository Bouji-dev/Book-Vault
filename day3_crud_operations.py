import psycopg2
from psycopg2 import Error


DB_CONFIG = {
    'dbname': 'bookvault_dev',
    'user': 'postgres',
    'password': 'pass',
    'host': 'localhost',
    'port': '5432'
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# ────────────────────────────────────────────────
# Add Author
# ────────────────────────────────────────────────
def add_author(first_name, last_name, bio=None):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO authors (first_name, last_name, bio)
            VALUES (%s, %s, %s)
            ON CONFLICT (first_name, last_name)
            DO UPDATE SET bio = EXCLUDED.bio
            RETURNING id;
        """, (first_name, last_name, bio))

        author_id = cur.fetchone()[0]
        conn.commit()
        return author_id
    except Error as e:
        if conn:
            conn.rollback()
            print(f'Error adding author: {e}')
            return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# ────────────────────────────────────────────────
# Add Book
# ────────────────────────────────────────────────
def add_book(isbn, title, description, year_published, author_id):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO books (isbn, title, description, year_published, author_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (isbn, title, description, year_published, author_id))

        book_id = cur.fetchone()[0]
        conn.commit()
        return book_id
    except Error as e:
        if conn:
            conn.rollback()
            print(f'Error adding book: {e}')
            return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# ────────────────────────────────────────────────
# Get all books with author name
# ────────────────────────────────────────────────
def get_all_books_with_author():
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                b.id, b.isbn, b.title, b.year_published, b.description,
                a.first_name || ' ' || a.last_name AS author
            FROM books b
            JOIN authors a ON b.author_id = a.id
            ORDER BY b.year_published DESC;
        """)
        
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        
        return [dict(zip(columns, row)) for row in rows]
        
    except Error as e:
        print(f"Error fetching books: {e}")
        return []
    finally:
        if cur: cur.close()
        if conn: conn.close()

# ────────────────────────────────────────────────
# Update book description
# ────────────────────────────────────────────────
def update_book_description(book_id, new_description):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE books 
            SET description = %s,
                created_at = now()
            WHERE id = %s
            RETURNING id;
        """, (new_description, book_id))
        
        updated = cur.fetchone()
        conn.commit()
        return bool(updated)
        
    except Error as e:
        if conn: conn.rollback()
        print(f"Error updating book: {e}")
        return False
    finally:
        if cur: cur.close()
        if conn: conn.close()

# ────────────────────────────────────────────────
# Delete book
# ────────────────────────────────────────────────
def delete_book(book_id):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM books WHERE id = %s RETURNING id;", (book_id,))
        deleted = cur.fetchone()
        conn.commit()
        return bool(deleted)
        
    except Error as e:
        if conn: conn.rollback()
        print(f"Error deleting book: {e}")
        return False
    finally:
        if cur: cur.close()
        if conn: conn.close()

# ────────────────────────────────────────────────
# test
# ────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== CRUD test day 3 ===\n")
    
    #  add new author
    author_id = add_author("Sadegh", "Hedayat", "Well-Known")
    print(f" author added → ID: {author_id}")
    
    # add book
    book_id = add_book(
        "964-448-057-7",
        "Blind owl",
        "Popular from Sadegh Hedayat",
        1937,
        author_id
    )
    print(f"book added → ID: {book_id}")
    
    # show all books
    books = get_all_books_with_author()
    print("\n exists books :")
    for b in books:
        print(f"  • {b['title']} ({b['year_published']}) - {b['author']}")
    
    # description update
    updated = update_book_description(book_id, "Sadegh Hedayat book")
    print(f"\n description of book updated: {updated}")
    
    # delete book
    deleted = delete_book(book_id)
    print(f" book deleted: {deleted}")