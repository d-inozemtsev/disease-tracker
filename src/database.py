import sqlite3
from config import DB_NAME

def init_db():
    """Создает таблицу, если её нет """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                source TEXT,
                published_at TEXT
            )
        ''')
        conn.commit()

def save_articles(articles):
    """Сохраняет список новостей в базу"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        for article in articles:
            title = article.get("title")
            source = article.get("source", {}).get("name")
            published_at = article.get("publishedAt")
            
            cursor.execute('''
                INSERT INTO news (title, source, published_at)
                VALUES (?, ?, ?)
            ''', (title, source, published_at))
        conn.commit()

def get_recent_articles(limit):
    """Достает последние новости"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT source, title FROM news ORDER BY id DESC LIMIT ?", (limit,))
        return cursor.fetchall()