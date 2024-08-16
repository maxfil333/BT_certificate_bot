import os
import uuid
import sqlite3

from config import config
from sql_queries import execute


def create_codes(db, k=1000):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    command = '''
    CREATE TABLE IF NOT EXISTS codes (
        id INTEGER PRIMARY KEY,
        guid TEXT NOT NULL
        )
    '''
    cursor.execute(command)
    for _ in range(k):
        code = uuid.uuid4().hex
        cursor.execute(f'INSERT INTO codes (guid) VALUES (?)', (code,))
    connection.commit()
    connection.close()


def create_users():
    command = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        username TEXT NOT NULL,
        guid TEXT NOT NULL
        )
    '''
    execute(command)


def main():
    DB = config['sqlite_db']
    if not os.path.exists(DB):
        create_codes(DB)
        create_users()
        print(f"Database '{DB}' has been created.")
    else:
        print(f"Using existing database '{DB}'")


if __name__ == '__main__':
    main()
