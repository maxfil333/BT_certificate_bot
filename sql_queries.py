import os
import sqlite3
from aiogram.types import Message

from config import config


# __________ queries __________

def execute(command, args=tuple()):
    connection = sqlite3.connect(config['sqlite_db'])
    cursor = connection.cursor()
    cursor.execute(command, args)
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result


def drop_table(table_name):
    execute(f'DROP TABLE IF EXISTS {table_name}')


def verify_guid(guid: str) -> list | None:
    guid_exists = execute(f'SELECT * FROM codes WHERE guid = ?', (guid,))
    if guid_exists:
        print(guid_exists)
        return guid_exists
    print(f'guid "{guid}" not found')


def delete_verified_guid(guid: str) -> None:
    execute(f'DELETE FROM codes WHERE guid = ?', (guid,))


def add_user(message: Message, guid: str) -> int:
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    u_name = message.from_user.username
    users_before = execute("SELECT COUNT(*) FROM USERS")[0][0]

    command = f"""
    INSERT INTO users (first_name, last_name, username, guid)
    SELECT ?, ?, ?, ?
    WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = ?);
    """
    execute(command, (f_name, l_name, u_name, guid, u_name))
    users_after = execute("SELECT COUNT(*) FROM USERS")[0][0]

    return users_after - users_before



