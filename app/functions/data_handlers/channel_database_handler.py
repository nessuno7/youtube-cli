import sqlite3
from . import json_handler
from ..config import channel_database

#id INTEGER PRIMARY KEY,
#channel_name TEXT,
#tiktok_username TEXT,
#tiktok_password TEXT,
# db_name, TEXT

def fetch_username_by_name(ch_name):
    conn = sqlite3.connect(channel_database)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE channel_name = ?', (ch_name,))
    result = cursor.fetchone()
    username = result[2]
    conn.close()
    return username

def fetch_password_by_name(ch_name):
    conn = sqlite3.connect(channel_database)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE channel_name = ?', (ch_name,))
    result = cursor.fetchone()
    password = result[3]
    conn.close()
    return password

def save_to_channel_database(ch_name, username, password):
    conn = sqlite3.connect(channel_database)
    cursor = conn.cursor()
    db_name = ch_name.replace("@", "")
    
    cursor.execute("SELECT 1 FROM entries WHERE channel_name = ? LIMIT 1", (ch_name,))
    exists = cursor.fetchone() is not None

    if not exists:
        cursor.execute(
            "INSERT INTO entries (channel_name, tiktok_username, tiktok_password, db_name) VALUES (?, ?, ?, ?)", 
            (ch_name, username, password, db_name)
        )
    conn.commit()
    conn.close()

def modify_username(ch_name, username):
    conn = sqlite3.connect(channel_database)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE entries SET tiktok_username = ? WHERE channel_name = ?
    ''', (username, ch_name))
    conn.commit()
    conn.close()

def modify_password(ch_name, password):
    conn = sqlite3.connect(channel_database)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE entries SET tiktok_password = ? WHERE channel_name = ?
    ''', (password, ch_name))
    conn.commit()
    conn.close()


def check_channel_entry_exists(ch_name):
    conn = sqlite3.connect(channel_database)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM entries WHERE channel_name = ? LIMIT 1", (ch_name,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def print_channels_and_databases():
    conn = sqlite3.connect(channel_database)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries')
    
    for row in cursor:
        print(f"Channel name: {row[1]}  Database name: {row[4]}")
    conn.close()

def delete_entry(ch_name):
    conn = sqlite3.connect(channel_database)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries WHERE channel_name = ?", (ch_name,))
    
    conn.commit()
    conn.close()

