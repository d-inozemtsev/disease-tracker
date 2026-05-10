from src.database import init_db, save_articles, get_recent_articles
from src.fetcher import fetch_news
from src.analyzer import extract_locations, extract_diseases, map_diseases_to_locations, is_real_outbreak
from src.geocoder import build_geo_dataset

def main():
    print("Инициализация базы данных...")
    init_db()
    
    print("Запрашиваем свежие новости...")
    articles = fetch_news()
    
    if articles:
        save_articles(articles)
        print(f"Успешно сохранено {len(articles)} новостей!\n")
        
        print("Анализируем последние записи...")
        recent = get_recent_articles(limit=500)
        # Сюда будем складывать словари с результатами анализа каждой новости
        analyzed_data = []
        
        for source, title in recent:
            if is_real_outbreak(title):
            # Ищем и страны, и болезни в одном заголовке
                locations = extract_locations(title)
                diseases = extract_diseases(title)
                
                # Сохраняем результат в виде словаря и кидаем в общий список
                analyzed_data.append({
                    "locations": locations,
                    "diseases": diseases
                })
                
                if locations and diseases:
                    print(f"🚨 Найдено совпадение! {', '.join(diseases).upper()} в {', '.join(locations)}")
                    print(f"   Новость: [{source}] {title}\n")
        
        final_statistics = map_diseases_to_locations(analyzed_data)
        geo_dataset = build_geo_dataset(final_statistics)
        
        print(geo_dataset)
            
    else:
        print("Новых статей не найдено.")

if __name__ == "__main__":
    main()