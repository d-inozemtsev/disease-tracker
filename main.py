import json
from src.database import init_db, save_articles, get_unprocessed_articles, update_article_analysis, get_active_outbreaks_from_db
from src.fetcher import fetch_news
from src.analyzer import extract_locations, extract_diseases, map_diseases_to_locations, is_real_outbreak, load_models
from src.geocoder import build_geo_dataset

def update_bd():
    init_db()
    articles = fetch_news()
    if articles:
        save_articles(articles)
    else:
        print("Not found new titles")

def process_data():
    unprocessed = get_unprocessed_articles()
    if unprocessed:
        nlp_model, classifier_model = load_models()
        
        for art_id, title in unprocessed:
            if is_real_outbreak(title, classifier_model):
                locations = extract_locations(title, nlp_model)
                diseases = extract_diseases(title)
                
                if locations and diseases:
                    metadata = {"locations": locations, "diseases": diseases}
                    update_article_analysis(art_id, is_outbreak=1, metadata_json=json.dumps(metadata))
                    continue
            
            update_article_analysis(art_id, is_outbreak=0, metadata_json="")
    
    active_rows = get_active_outbreaks_from_db()
    analyzed_data = [json.loads(row) for row in active_rows]
    
    final_statistics = map_diseases_to_locations(analyzed_data)
    geo_dataset = build_geo_dataset(final_statistics)
    
    with open("outbreaks.json", "w", encoding="utf-8") as f:
        json.dump(geo_dataset, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update_bd()
    process_data()