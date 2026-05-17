import requests
from src.geocoder import calculate_distance

def get_user_location():
    """Пуленепробиваемая версия (не банит VPN)"""
    try:
        response = requests.get("https://ipwhois.app/json/", timeout=5).json()
        
        if response.get('success'):
            return {
                "lat": float(response['latitude']),
                "lon": float(response['longitude']),
                "city": response.get('city', 'Unknown')
            }
        else:
            print("❌ Сервис заблокировал запрос:", response)
    except Exception as e:
        print(f"❌ Критическая ошибка получения IP: {e}")
    
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