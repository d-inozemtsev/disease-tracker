from transformers import pipeline

print("Скачиваем и загружаем модель (это займет время только при первом запуске)...")
# Используем легкую модель, чтобы не взорвать твой Мак
classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

# Наши тестовые новости
news_samples = [
    "A new deadly outbreak of hantavirus has been reported in a small town in Texas.",
    "Scientists in Oxford have successfully developed a new mRNA vaccine against the virus.",
    "How to protect your computer from the latest trojan virus and malware."
]

# Категории, по которым мы хотим раскидать эти тексты
candidate_labels = ["active disease outbreak", "medical research and vaccines", "cybersecurity"]

for text in news_samples:
    print(f"\nНовость: {text}")
    # Просим нейросеть предсказать категорию
    result = classifier(text, candidate_labels)
    
    # result['labels'][0] - это самая вероятная категория
    # result['scores'][0] - вероятность от 0 до 1
    best_label = result['labels'][0]
    confidence = result['scores'][0] * 100
    
    print(f"🧠 Вердикт ИИ: {best_label} (Уверенность: {confidence:.1f}%)")