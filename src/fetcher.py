import requests
from datetime import datetime, timedelta
from config import NEWS_API_KEY

API_KEY = NEWS_API_KEY

BROAD_QUERIES = [
    "outbreak AND (virus OR disease OR infection)",
    "epidemic OR pandemic",
    '"new cases" AND (virus OR infection)',
    "quarantine OR health emergency"
]

def fetch_news(DAYS_BACK=7):
    '''Получает список статей с NewsAPI по общим медицинским запросам за период'''
    if not API_KEY:
        raise ValueError("API ключ не найден! Проверь файл .env")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=DAYS_BACK)

    from_param = start_date.strftime('%Y-%m-%d')
    to_param = end_date.strftime('%Y-%m-%d')

    all_articles = []
    seen_titles = set()

    for query in BROAD_QUERIES:
        url = f"https://newsapi.org/v2/everything?q={query}&from={from_param}&to={to_param}&language=en&sortBy=relevancy&apiKey={API_KEY}&pageSize=100"
        
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
                        
                print(f"Request '{query[:25]}...': download {len(articles)} titles")
            else:
                print(f"Ошибка API для запроса '{query}': {data.get('message')}")
                
        except Exception as e:
            print(f"Error connection '{query}': {e}")
    return all_articles