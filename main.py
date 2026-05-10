from src.database import init_db, save_articles, get_recent_articles
from src.fetcher import fetch_news
from src.analyzer import extract_locations, extract_diseases, map_diseases_to_locations, is_real_outbreak, load_models
from src.geocoder import build_geo_dataset

def main():

    init_db()
    articles = fetch_news()
    
    if articles:
        save_articles(articles)
        recent = get_recent_articles(limit=500)
        analyzed_data = []

        nlp_model, classifier_model = load_models()
        
        for source, title in recent:
            if is_real_outbreak(title, classifier_model):
                locations = extract_locations(title, nlp_model)
                diseases = extract_diseases(title)
                
                analyzed_data.append({
                    "locations": locations,
                    "diseases": diseases
                })
                
                if locations and diseases:
                    print(f"found {', '.join(diseases).upper()} in {', '.join(locations)}")
                    print(f"news: [{source}] {title}\n")
        
        final_statistics = map_diseases_to_locations(analyzed_data)
        geo_dataset = build_geo_dataset(final_statistics)
        print(geo_dataset)
            
    else:
        print("Not found new title")

if __name__ == "__main__":
    main()