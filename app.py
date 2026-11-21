import streamlit as st
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
from main import clasificar_residuo
from map import crear_mapa

st.title("EcoPunto Tandil ♻️", text_alignment="center")

tab_consulta, tab_mapa = st.tabs(["♻️ Consultar Residuo", "📍 Puntos Limpios en Tandil"])

with st.sidebar:
    st.header("Consultar un residuo")
    residuo = st.text_area("Escribí qué residuo tenés")
    imagen = st.file_uploader(
        "O subí una imagen",
        type=["jpg", "jpeg", "png", "webp"],
    )
    boton_consultar = st.button("Consultar residuo")

with tab_consulta:
    if boton_consultar:
        if not residuo and not imagen:
            st.warning("Ingresá un texto o una foto.")
        else:
            bytes_foto = imagen.getvalue() if imagen else None

            with st.spinner("Consultando a Punto Limpio..."):
                resultado = clasificar_residuo(texto=residuo, bytes_imagen=bytes_foto, tipo_mime=imagen.type if imagen else "image/jpeg")

            if resultado.es_reciclable:
                st.success(f"Es reciclable: {resultado.residuo}")
            else:
                st.error(f"No aceptado: {resultado.residuo}")

            st.info(resultado.instrucciones)
            
with tab_mapa:
    ubicacion = streamlit_geolocation()
    if ubicacion["latitude"] is not None and ubicacion["longitude"] is not None:
        user_location = [ubicacion["latitude"], ubicacion["longitude"]]
        mapa = crear_mapa(user_location)
        datos_mapa = st_folium(
            mapa,
            key="mapa",
            height=600,
            width=800,
        )
    else:
        st.info("Compartí tu ubicación para encontrar el Punto Limpio más cercano.")