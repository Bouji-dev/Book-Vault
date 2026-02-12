import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(
        dbname='bookvault_dev',
        user='postgres',
        password='pass',
        host='localhost',
        port='5432'
    )
    print('Connection established successfuly')

    cursor = connection.cursor()

    cursor.execute('SELECT version();')
    db_version = cursor.fetchone()
    print(f'PostgreSQL version: {db_version[0]}')

    cursor.execute('SELECT current_database();')
    current_db = cursor.fetchone()
    print(f'Current database: {current_db[0]}')

except Error as e:
    print(f'Error in connection or execution: {e}')

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
        print('Connection closed')            