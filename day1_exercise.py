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
    conn.autocommit = True  # for easy DDL commands
    cur = conn.cursor()

    # create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS test_table(
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL
                );
    """)

    # insert data
    cur.execute(
        "INSERT INTO test_table (message) VALUES (%s);",
        ("Hello PostgreSQL Day 1!",)
    )

    # read
    cur.execute("SELECT * FROM test_table;")
    rows = cur.fetchall()

    print('Content of test_table:')
    for row in rows:
        print(f'ID: {row[0]} | message: {row[1]}')

except Error as e:
    print(f'Error: {e}')

finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()