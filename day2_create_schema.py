import psycopg2
from psycopg2 import Error


try:
    conn = psycopg2.connect(
        dbname='bookvault_dev',
        user='postgres',
        password='pass',
        host='localhost',
        port='5432'
    )
    conn.autocommit = True

    cur = conn.cursor()

    # create authors table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id          bigserial           PRIMARY KEY,
            first_name  text                NOT NULL,
            last_name   text                NOT NULL,
            bio         text,
            created_at  timestamptz         NOT NULL DEFAULT now(),
            CONSTRAINT authors_name_unique UNIQUE (first_name, last_name)
        );
    """)

    # create books table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id              bigserial           PRIMARY KEY,
            isbn            varchar(13)         UNIQUE,
            title           text                NOT NULL,
            description     text,
            year_published  integer             CHECK (year_published >= 1500 
                                                    AND year_published <= extract(year from now()) + 5),
            author_id       bigint              NOT NULL,
            created_at      timestamptz         NOT NULL DEFAULT now(),
            
            CONSTRAINT fk_book_author
                FOREIGN KEY (author_id) REFERENCES authors(id)
                ON DELETE RESTRICT
        );
    """)
        
    # insert author instance
    cur.execute("""
        INSERT INTO authors (first_name, last_name)
        VALUES (%s, %s)
        ON CONFLICT (first_name, last_name) DO NOTHING
        RETURNING id;
    """, ('George', 'Orwell'))

    author_row = cur.fetchone()
    if author_row:
        author_id = author_row[0]
    else:
        # if exists already find the id
        cur.execute(
            'SELECT id FROM authors WHERE first_name = %s AND last_name = %s',
            ('George', 'Orwell')
        )
        author_id = cur.fetchone()[0]

    # add books
    books_data = [
            ("978-045152493", "1984", "Mastreprise", 1949, author_id),
            ("978-045228423", "Animal Farm", "Revolution", 1945, author_id)
        ]

    cur.executemany("""
        INSERT INTO books (isbn, title, description, year_published, author_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (isbn) DO NOTHING;
    """, books_data)

    print("Tables created and instances submited successfully")

except Error as e:
    print('Error:', e)

finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals() and conn:
        conn.close()