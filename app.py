import streamlit as st
import folium
import json
import streamlit.components.v1 as components
from src.user import get_user_location, nearest_disease
from streamlit_geolocation import streamlit_geolocation
from collections import Counter
import pandas as pd


st.set_page_config(page_title="Disease Tracker", page_icon="🦠", layout="wide")

st.title("🦠 Глобальный мониторинг вспышек заболеваний по всему миру")

@st.cache_data(ttl=60)
def load_data():
    try:
        with open("outbreaks.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

with st.spinner('Загружаем карту угроз...ох, много всего'):
    data = load_data()


is_nearest = False
if data:
    st.success(f"Анализ завершен. Найдено потенциальных очагов: {len(data)}")

    st.write("**Покажи свою локацию плиз, нажми 'Разрешить' и на кнопку ниже (мишень типа)**")
    
    location_gps = streamlit_geolocation()
    
    user_coords = None
    
    if location_gps and location_gps.get('latitude') is not None:
        user_coords = (location_gps['latitude'], location_gps['longitude'])
    else:
        ip_loc = get_user_location()
        
        if ip_loc and ip_loc.get('lat') is not None:
            user_coords = (ip_loc['lat'], ip_loc['lon'])

    if user_coords:
        nearest = nearest_disease(user_coords, data)
        if nearest:
            is_nearest = True
            st.warning(
                f" Рядом с тобой обнаружено ({', '.join(nearest['disease']).upper()}) "
                f"и он где-то в **{nearest['distance_km']} км** от тебя, примерно вот тут: {nearest['location']} (это где ваще?)"
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

    st.markdown("---") 
    st.subheader("Статистика по угрозам")
    
    all_diseases_extracted = [d.upper() for item in data for d in item['disease']]
    disease_counts = Counter(all_diseases_extracted)
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric(label="Всего активных очагов на карте", value=len(data))
    with metric_col2:
        most_common_disease = disease_counts.most_common(1)[0][0] if disease_counts else "Нет данных"
        st.metric(label="Говнюк недели", value=most_common_disease)

    # Сам график
    if disease_counts:
        st.write("**Топ-5 вирусов по количеству упоминаний в прессе:**")
        df_chart = pd.DataFrame(disease_counts.items(), columns=["Вирус", "Количество очагов"])
        df_chart = df_chart.sort_values(by="Количество очагов", ascending=False).head(5)
        st.bar_chart(data=df_chart, x="Вирус", y="Количество очагов", color="#ff4b4b")
    # =========================================================

else:
    st.warning("В последних новостях не найдено упоминаний болезней и локаций.")