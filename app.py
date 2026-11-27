import streamlit as st
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
from main import classify_waste
from map import create_map


st.title("EcoPunto Tandil ♻️", text_alignment="center")

consultation_tab, map_tab = st.tabs(["♻️ Consultar Residuo", "📍 Puntos Limpios en Tandil"])

with st.sidebar:
    st.header("Consultar un residuo")
    waste_text = st.text_area("Escribí qué residuo tenés")
    uploaded_image = st.file_uploader(
        "O subí una imagen",
        type=["jpg", "jpeg", "png", "webp"],
    )
    consult_button = st.button("Consultar residuo")

with consultation_tab:
    if consult_button:
        if not waste_text and not uploaded_image:
            st.warning("Ingresá un texto o una foto.")
        else:
            image_bytes = None
            mime_type = "image/jpeg"
            if uploaded_image:
                image_bytes = uploaded_image.getvalue()
                mime_type = uploaded_image.type

            with st.spinner("Consultando a Punto Limpio..."):
                result = classify_waste(text=waste_text,image_bytes=image_bytes,mime_type=mime_type)

            if result.is_recyclable:
                st.success(f"Es reciclable: {result.waste}")
            else:
                st.error(f"No aceptado: {result.waste}")

            st.info(result.instructions)
            
with map_tab:
    location = streamlit_geolocation()
    if location["latitude"] is not None and location["longitude"] is not None:
        user_location = [location["latitude"], location["longitude"]]
        folium_map = create_map(user_location)
        map_data = st_folium(
            folium_map,
            key="mapa",
            height=600,
            width=800,
        )
    else:
        st.info("Compartí tu ubicación para encontrar el Punto Limpio más cercano.")