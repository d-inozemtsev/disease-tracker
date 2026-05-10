import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

# Наш арсенал: список конкретных угроз
DISEASES = [
    # Коронавирусы и ОРВИ
    "covid-19", "covid", "coronavirus", "sars-cov-2", "sars", "mers",
    "influenza", "flu", "avian flu", "swine flu", "h5n1", "h1n1", "h3n2",
    "rsv", "respiratory syncytial virus",
    
    # Геморрагические лихорадки
    "ebola", "marburg", "lassa", "lassa fever",
    "crimean-congo hemorrhagic fever", "cchf",
    "rift valley fever", "dengue", "yellow fever",
    "hantavirus", "hantavirus pulmonary syndrome",
    
    # Вирусы, передаваемые комарами/клещами
    "zika", "chikungunya", "west nile", "west nile virus",
    "tick-borne encephalitis", "tbe", "japanese encephalitis",
    "powassan", "usutu",
    
    # Оспы и сыпные инфекции
    "monkeypox", "mpox", "smallpox", "measles", "rubella",
    "chickenpox", "varicella", "shingles",
    
    # Гепатиты
    "hepatitis a", "hepatitis b", "hepatitis c", "hepatitis d", "hepatitis e",
    
    # Другие вирусные
    "polio", "poliomyelitis", "rotavirus", "norovirus",
    "nipah", "nipah virus", "hendra",
    "rabies", "hiv", "aids",
    "marburg virus", "machupo", "junin",
    
    # Бактериальные (часто в новостях)
    "cholera", "plague", "bubonic plague", "pneumonic plague",
    "tuberculosis", "tb", "diphtheria", "pertussis", "whooping cough",
    "meningitis", "meningococcal",
    "anthrax", "leptospirosis", "typhoid", "typhus",
    "lyme disease", "lyme",
    
    # Паразитарные / протозойные
    "malaria", "zika",  # zika уже был

    "virus"
]

def fetch_news(days_back=7):
    '''Получает список статей с NewsAPI по конкретным болезням за период'''
    if not API_KEY:
        raise ValueError("API ключ не найден! Проверь файл .env")

    # Вычисляем окно времени (например, за последние 7 дней)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Форматируем даты для NewsAPI (YYYY-MM-DD)
    from_param = start_date.strftime('%Y-%m-%d')
    to_param = end_date.strftime('%Y-%m-%d')

    all_articles = []
    seen_titles = set() # Множество для быстрого поиска и удаления дубликатов

    print(f"🕵️ Начинаем глобальный поиск за период с {from_param} по {to_param}...")

    # Проходимся циклом по каждой болезни
    for disease in DISEASES:
        # Умный запрос: ищем название болезни И (вспышка ИЛИ эпидемия ИЛИ случаи)
        query = f'({disease}) AND (outbreak OR epidemic OR cases)'
        
        # Заменили sortBy=publishedAt на relevancy, чтобы получать самые точные совпадения, а не просто свежие
        url = f"https://newsapi.org/v2/everything?q={query}&from={from_param}&to={to_param}&language=en&sortBy=relevancy&apiKey={API_KEY}&pageSize=40"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if data.get("status") == "ok":
                articles = data.get("articles", [])
                
                # Фильтруем дубликаты
                for article in articles:
                    title = article.get("title")
                    if title and title not in seen_titles and "[Removed]" not in title:
                        seen_titles.add(title)
                        all_articles.append(article)
                        
                print(f"✅ {disease.upper().ljust(20)}: скачано уникальных статей: {len(articles)}")
            else:
                print(f"⚠️ Ошибка API для {disease}: {data.get('message')}")
                
        except Exception as e:
            print(f"❌ Ошибка соединения при поиске {disease}: {e}")

    print(f"\n🎯 Итог: в трубу (Pipeline) отправлено {len(all_articles)} новостей!")
    return all_articles