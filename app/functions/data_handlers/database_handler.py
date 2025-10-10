import sqlite3
from . import json_handler
from ..config import database_dir

#id INTEGER PRIMARY KEY,
#link TEXT,
#title TEXT,
#views TEXT,
#heatmap TEXT,
#duration INTEGER


def fetch_link(id):
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (id,))
    result = cursor.fetchone()
    link = result[1]
    conn.close()
    return link

def fetch_title(id):
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (id,))
    result = cursor.fetchone()
    title = result[2]
    conn.close()
    return title

def fetch_views(id):
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (id,))
    result = cursor.fetchone()
    views = result[3]
    conn.close()
    return views

def fetch_heatmap(id):
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (id,))
    result = cursor.fetchone()
    heatmap = result[4]
    conn.close()
    return heatmap

def fetch_duration(id):
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (id,))
    result = cursor.fetchone()
    duration = result[5]
    conn.close()
    return duration
    


def save_to_database(link, title, views, heatmap, duration):
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM entries WHERE title = ? LIMIT 1", (title,))
    exists = cursor.fetchone() is not None

    if not exists:
        cursor.execute('''
            INSERT INTO entries (link, title, views, heatmap, duration, clip) VALUES (?, ?, ?, ?, ?, ?)
        ''', (link, title, views, heatmap, duration, False))

    conn.commit()
    conn.close()


def modify_clip(id, clip):
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE entries SET clip = ? WHERE id = ?
    ''', (clip, id))
    conn.commit()
    conn.close()


def modify_link(id, link):
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE entries SET link = ? WHERE id = ?
    ''', (link, id))
    conn.commit()
    conn.close()


def modify_title(id, title):
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE entries SET title = ? WHERE id = ?
    ''', (title, id))
    conn.commit()
    conn.close()


def modify_views(id, views):
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE entries SET views = ? WHERE id = ?
    ''', (views, id))
    conn.commit()
    conn.close()


def modify_heatmap(id, heatmap):
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE entries SET heatmap = ? WHERE id = ?
    ''', (heatmap, id))
    conn.commit()
    conn.close()


def modify_duration(id, duration):
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE entries SET duration = ? WHERE id = ?
    ''', (duration, id))
    conn.commit()
    conn.close()

def print_posted_id(control): #put true when searching posted videos, not true when searching not posted
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries')

    list = []
    for row in cursor:
        if row[6] == control:
            list.append(row[0])
    print(list)

    conn.close()

def print_all_videos():
    conn = sqlite3.connect(database_dir / f'{json_handler.fetch_database_name()}.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries')

    for row in cursor:
        print(f"Id: {row[0]}    Title: {row[2]}")
    conn.close()


