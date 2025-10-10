import sqlite3
from ..config import database_dir, data_dir

def create_database(name):
    conn = sqlite3.connect(database_dir / f"{name}.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT,
            title TEXT,
            views TEXT,
            heatmap TEXT,
            duration INTEGER,
            clip BOOL
        )
    ''')

    conn.commit()
    conn.close()

def create_channels_database():
    conn = sqlite3.connect(data_dir / "channels.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_name TEXT,
            tiktok_username TEXT,
            tiktok_password TEXT,
            db_name TEXT
        )
    ''')

    conn.commit()
    conn.close()
