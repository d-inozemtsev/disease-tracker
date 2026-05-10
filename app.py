import streamlit as st
import folium
import streamlit.components.v1 as components
from src.database import get_recent_articles
from src.analyzer import extract_locations, extract_diseases, map_diseases_to_locations, is_real_outbreak
from src.geocoder import build_geo_dataset
from src.user import get_user_location, nearest_disease
from streamlit_geolocation import streamlit_geolocation


st.set_page_config(page_title="Disease Tracker", page_icon="🦠", layout="wide")

st.title("🦠 Глобальный мониторинг вспышек заболеваний по всему миру")

user_info = get_user_location()

@st.cache_data(ttl=300)
def load_data():

    recent = get_recent_articles(limit=500)
    analyzed_data = []
    for source, title in recent:
        if is_real_outbreak(title):
            locs = extract_locations(title)
            dis = extract_diseases(title)
            analyzed_data.append({"locations": locs, "diseases": dis})

    stats = map_diseases_to_locations(analyzed_data)
    geo_data = build_geo_dataset(stats)
    return geo_data


with st.spinner('Анализируем новостные сводки...'):
    data = load_data()

is_nearest = False
if data:
    st.success(f"Анализ завершен. Найдено потенциальных очагов: {len(data)}")

    st.write("**Покажи свою локацию плиз, нажми 'Разрешить' и на кнопку ниже (мишень типа)**")
    location = streamlit_geolocation()
    
    if location['latitude'] is not None and location['longitude'] is not None:
        user_coords = (location['latitude'], location['longitude'])
        nearest = nearest_disease(user_coords, data)

        if nearest:
            is_nearest = True
            st.warning(
                f" Рядом с тобой обнаружено ({', '.join(nearest['disease']).upper()}) "
                f"и он где-то в **{nearest['distance_km']} км** от тебя, примерно вот тут: ({nearest['location']})."
            )
    else:
        st.info("Разреши доступ к гео и узнаешь, как далеко от тебя угроза!")
    
    m = folium.Map(location=[30.0, -20.0], zoom_start=2)

    if is_nearest:
        folium.Marker(
            location=user_coords,
            popup="<b>Это ТЫ, а не вирус!! ха-ха</b>",
            tooltip="Твоя локация",
            icon=folium.Icon(color="blue", icon="user", prefix="fa")
        ).add_to(m)

    for item in data:
        folium.CircleMarker(
            location=[item['lat'], item['lon']],
            radius=10,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.6,
            popup=f"<b>{item['location']}</b><br>Вирусы: {', '.join(item['disease'])}"
        ).add_to(m)
        
    components.html(m._repr_html_(), height=600)
    if st.button("🔄 обновить данные"):
        st.cache_data.clear()

else:
    st.warning("В последних новостях не найдено упоминаний болезней и локаций.")