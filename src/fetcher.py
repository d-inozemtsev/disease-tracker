import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from config import KNOWN_DISEASES, DAYS_BACK, NEWS_API_KEY

API_KEY = NEWS_API_KEY

def fetch_news(DAYS_BACK=7):
    '''Получает список статей с NewsAPI по конкретным болезням за период'''
    if not API_KEY:
        raise ValueError("API ключ не найден! Проверь файл .env")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=DAYS_BACK)

    from_param = start_date.strftime('%Y-%m-%d')
    to_param = end_date.strftime('%Y-%m-%d')

    all_articles = []
    seen_titles = set()

    for disease in KNOWN_DISEASES:
        query = f'({disease}) AND (outbreak OR epidemic OR cases)'
        
        url = f"https://newsapi.org/v2/everything?q={query}&from={from_param}&to={to_param}&language=en&sortBy=relevancy&apiKey={API_KEY}&pageSize=40"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if data.get("status") == "ok":
                articles = data.get("articles", [])
                
                for article in articles:
                    title = article.get("title")
                    if title and title not in seen_titles and "[Removed]" not in title:
                        seen_titles.add(title)
                        all_articles.append(article)
                        
                print(f"{disease.upper().ljust(20)}: download {len(articles)}")
            else:
                print(f"error API for {disease}: {data.get('message')}")
                
        except Exception as e:
            print(f"Connection error {disease}: {e}")

    print(f"Succesfully send {len(all_articles)} news")
    return all_articles