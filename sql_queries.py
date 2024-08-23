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


def delete_verified_guid(guid: str) -> None:
    execute(f'DELETE FROM codes WHERE guid = ?', (guid,))


def delete_user(user_id: str) -> None:
    user = execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    if user:
        print(f"Найден пользователь: {user}")
        execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        print("Пользователь удален.")
    else:
        print("Пользователь не найден.")


def is_in_codes(guid: str) -> list | None:
    guid_exists = execute('SELECT EXISTS(SELECT 1 FROM codes WHERE guid = ?);', (guid,))[0][0]
    if guid_exists:
        return guid_exists
    print(f'guid "{guid}" not found')


def is_in_users(message: Message) -> bool:
    user_id = str(message.from_user.id)
    command = 'SELECT EXISTS(SELECT 1 FROM users WHERE user_id = ?);'
    return bool(execute(command, (user_id,))[0][0])


def add_user(message: Message, guid: str) -> None:
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    u_name = message.from_user.username
    user_id = message.from_user.id

    command = f"""
    INSERT INTO users (first_name, last_name, username, user_id, guid)
    SELECT ?, ?, ?, ?, ?
    WHERE NOT EXISTS (SELECT 1 FROM users WHERE user_id = ?);
    """
    execute(command, (f_name, l_name, u_name, user_id, guid, user_id))


if __name__ == '__main__':
    pass
