import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

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
]

DAYS_BACK = 7
PAGE_SIZE = 40


DB_NAME = "disease_news.db"

GEOCODER_USER_AGENT = "disease_tracker"


print(NEWS_API_KEY)