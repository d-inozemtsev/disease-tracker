import json
from src.database import init_db, save_articles, get_recent_articles
from src.fetcher import fetch_news
from src.analyzer import extract_locations, extract_diseases, map_diseases_to_locations, is_real_outbreak, load_models
from src.geocoder import build_geo_dataset

def update_bd():
    init_db()
    articles = fetch_news()
    if articles:
        save_articles(articles)
    else:
        print("Not found new title")

def process_data():
    recent = get_recent_articles(limit=1000)
    analyzed_data = []

    nlp_model, classifier_model = load_models()
        
    for source, title in recent:
        if is_real_outbreak(title, classifier_model):
            locations = extract_locations(title, nlp_model)
            diseases = extract_diseases(title)
                
            if locations and diseases:
                analyzed_data.append({
                    "locations": locations,
                    "diseases": diseases
                })
    
    final_statistics = map_diseases_to_locations(analyzed_data)
    geo_dataset = build_geo_dataset(final_statistics)
    
    with open("outbreaks.json", "w", encoding="utf-8") as f:
        json.dump(geo_dataset, f, ensure_ascii=False, indent=4)
        
    print(f"data saved in outbreaks.json")

if __name__ == "__main__":
    update_bd()
    process_data()