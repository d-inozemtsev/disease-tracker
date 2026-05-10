import requests
from src.geocoder import calculate_distance

def get_user_location():
    """Определяет примерные координаты пользователя по IP"""
    try:
        response = requests.get("http://ip-api.com/json/").json()
        if response['status'] == 'success':
            return {
                "lat": response['lat'],
                "lon": response['lon'],
                "city": response['city']
            }
    except Exception as e:
        print(f"Ошибка получения IP: {e}")
    return None

def nearest_disease(user_coord: tuple, data: list) -> dict:
    """Вычисляет ближайшую вспышку заболеваний к пользователю"""
    min_dist = float('inf')
    best = {}
    
    for d in data:
        dist_now = calculate_distance(user_coord, (d['lat'], d['lon']))
        if dist_now < min_dist:
            min_dist = dist_now
            best = d
            best['distance_km'] = dist_now
            
    return best
