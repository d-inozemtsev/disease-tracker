import spacy
from transformers import pipeline
from config import KNOWN_DISEASES
from functools import lru_cache


@lru_cache(maxsize=None)
def load_models():
    """Загружвет модель в память"""
    nlp = spacy.load("en_core_web_sm")
    classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
    return nlp, classifier

def extract_locations(text: str, nlp_model) -> list:
    """Ищет локации с помощью переданной модели"""
    doc = nlp_model(text)
    return [ent.text for ent in doc.ents if ent.label_ == "GPE"]

def extract_diseases(text: str) -> list:
    text_lower = text.lower()
    return [d for d in KNOWN_DISEASES if d in text_lower]

def is_real_outbreak(text: str, classifier_model) -> bool:
    """Анализирует текст переданной моделью"""
    candidate_labels = ["active disease outbreak", "medical research and vaccines", "cybersecurity"]
    result = classifier_model(text, candidate_labels)
    
    best_label = result['labels'][0]
    confidence = result['scores'][0]

    return (confidence >= 0.5) and (best_label == 'active disease outbreak')

def map_diseases_to_locations(data: list) -> dict:
    locations_dict = {}
    for d in data:
        locs = d['locations'] 
        viruses = d['diseases']

        if not locs or not viruses: continue

        for loc in locs:
            if loc not in locations_dict:
                locations_dict[loc] = []
            for virus in viruses:
                if virus not in locations_dict[loc]:
                    locations_dict[loc].append(virus)
    
    return locations_dict




