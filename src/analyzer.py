import spacy
from collections import Counter
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")

def extract_locations(text: str) -> list:
    """
    Извлекает из текста названия географических объектов (GPE) с помощью spaCy
    """
    doc = nlp(text)
    
    locations = []
    for ent in doc.ents:
        if ent.label_ == "GPE":
            locations.append(ent.text)
            
    return locations


def country_count(data: list) -> dict:
    """
    Считает кол-во упоминаний каждой страны
    """
    cnt = Counter(data)
    return dict(cnt)


KNOWN_DISEASES = [
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

def extract_diseases(text: str) -> list:
    """
    Ищет известные болезни в тексте простым словарным методом
    """
    text_lower = text.lower()
    found_diseases = []
    
    for disease in KNOWN_DISEASES:
        if disease in text_lower:
            found_diseases.append(disease)
            
    return found_diseases



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






classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
def is_real_outbreak(text: str) -> bool:
    candidate_labels = ["active disease outbreak", "medical research and vaccines", "cybersecurity"]
    result = classifier(text, candidate_labels)
    best_label = result['labels'][0]
    confidence = result['scores'][0]

    if confidence < 0.5:
        return False
    if best_label == 'active disease outbreak':
        return True
    return False




