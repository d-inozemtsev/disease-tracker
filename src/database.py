import sqlite3
from config import DB_NAME

def init_db():
    """Создает таблицу для хранения новостей с разметкой ИИ"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                source TEXT,
                published_at TEXT,
                processed INTEGER DEFAULT 0,
                is_outbreak INTEGER DEFAULT 0,
                metadata TEXT DEFAULT ''
            )
        ''')
        conn.commit()

def save_articles(articles):
    """Сохраняет только новые уникальные статьи"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        for article in articles:
            title = article.get("title")
            source = article.get("source", {}).get("name")
            published_at = article.get("publishedAt")
            
            if not title:
                continue
                
            cursor.execute("SELECT 1 FROM news WHERE title = ?", (title,))
            if cursor.fetchone():
                continue
            
            cursor.execute('''
                INSERT INTO news (title, source, published_at)
                VALUES (?, ?, ?)
            ''', (title, source, published_at))
        conn.commit()

def get_unprocessed_articles():
    """Достает только новые, еще не обработанные ИИ статьи"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM news WHERE processed = 0")
        return cursor.fetchall()

def update_article_analysis(article_id, is_outbreak, metadata_json):
    """Обновляет статус проверки статьи нейросетью"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE news 
            SET processed = 1, is_outbreak = ?, metadata = ? 
            WHERE id = ?
        ''', (is_outbreak, metadata_json, article_id))
        conn.commit()

def get_active_outbreaks_from_db():
    """Достает размеченные вспышки строго за последние 7 дней (чтобы карта не засорялась)"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT metadata FROM news 
            WHERE is_outbreak = 1 
            AND published_at >= datetime('now', '-7 days')
        ''')
        return [row[0] for row in cursor.fetchall() if row[0]]