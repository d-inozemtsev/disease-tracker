import time
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from config import GEOCODER_USER_AGENT
from functools import lru_cache

geolocator = Nominatim(user_agent=GEOCODER_USER_AGENT)

@lru_cache(maxsize=None)
def to_coords(text: str) -> dict:
    try:
        time.sleep(1.1)
        location = geolocator.geocode(text)
        if location:
            return {'latitude': location.latitude, 'longitude': location.longitude}
    except Exception as e:
        print(f"⚠️ Ошибка геокодирования для {text}: {e}")
    return None

def build_geo_dataset(statistics: dict) -> list:
    """
    Принимает статистику {'Country': ['virus1']}, 
    проходит по ней и собирает финальный список с координатами.
    """

    dataset = []

    for loc, virus in statistics.items():
        coords = to_coords(loc)

        if coords:
            dataset.append(
                {
                    "location": loc,
                    "disease": virus,
                    "lat": coords['latitude'],
                    "lon": coords['longitude']
                }
            )
    return dataset


def calculate_distance(user_coords, outbreak_coords):
    """Вычисляет расстояние между двумя точками на Земле в километрах"""
    distance = geodesic(user_coords, outbreak_coords).kilometers
    return round(distance)