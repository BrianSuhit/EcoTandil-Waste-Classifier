from math import asin, cos, radians, sin, sqrt

import folium

puntos_limpios = [
    {
        "nombre": "Centro",
        "direccion": "Av. Rivadaavia 250",
        "coords": [-37.33383832611302, -59.142425431038795],
    },
    {
        "nombre": "Norte",
        "direccion": "Darragueira y Jurado",
        "coords": [-37.30691363888284, -59.115659734493846],
    },
    {
        "nombre": "Punto Limpio estacion Oeste",
        "direccion": "Reynoso al 2030",
        "coords": [-37.29455099576207, -59.15962946811658],
    },
    {
        "nombre": "Villa Italia Norte",
        "direccion": "Pasteur 1150",
        "coords": [-37.299335389653955, -59.13543359571474],
    },
    {
        "nombre": "Juan B. Justo",
        "direccion": "Av. Juan B. Justo 238",
        "coords": [-37.31749406960154, -59.15625831789002],
    },
    {
        "nombre": "Cerro Leones ( plaza Democracia )",
        "direccion": "Maderni y Lamberto",
        "coords": [-37.31621262864179, -59.20370497452548],
    },
    {
        "nombre": "Vela",
        "direccion": "Corralón Municipal",
        "coords": [-37.39917894590941, -59.506234676840876],
    },
    {
        "nombre": "Gardey",
        "direccion": "Corralón Municipal",
        "coords": [-37.28030460387253, -59.36089373309871],
    },
]


def distancia_km(origen, destino):
    lat1, lon1 = map(radians, origen)
    lat2, lon2 = map(radians, destino)
    diferencia_lat = lat2 - lat1
    diferencia_lon = lon2 - lon1
    a = (
        sin(diferencia_lat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(diferencia_lon / 2) ** 2
    )
    return 6371 * 2 * asin(sqrt(min(1, a)))


def crear_mapa(user_location):
    mapa = folium.Map()
    punto_mas_cercano = min(puntos_limpios, key=lambda p: distancia_km(user_location, p["coords"]))
    distancia_cercana = distancia_km(user_location, punto_mas_cercano["coords"])

    folium.PolyLine(
        locations=[user_location, punto_mas_cercano["coords"]],
        color="orange",
        weight=3,
        tooltip=f"Distancia directa: {distancia_cercana:.2f} km",
    ).add_to(mapa)

    for p in puntos_limpios:
        es_mas_cercano = p is punto_mas_cercano
        popup = f"{p['nombre']} - {p['direccion']}"
        if es_mas_cercano:
            popup += f"<br>Punto más cercano: {distancia_cercana:.2f} km"

        folium.Marker(
            location=p["coords"],
            popup=popup,
            tooltip=f"{p['nombre']} (más cercano)" if es_mas_cercano else p["nombre"],
            icon=folium.Icon(color="orange" if es_mas_cercano else "green"),
        ).add_to(mapa)

    folium.Marker(
        location=user_location,
        popup="Tu ubicación",
        tooltip="Tu ubicación",
        icon=folium.Icon(color="blue", icon="user", prefix="fa"),
    ).add_to(mapa)

    mapa.fit_bounds([p["coords"] for p in puntos_limpios] + [user_location])
    return mapa