from math import asin, cos, radians, sin, sqrt

import folium

clean_points = [
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


def distance_km(origin, destination):
    lat1, lon1 = map(radians, origin)
    lat2, lon2 = map(radians, destination)
    latitude_difference = lat2 - lat1
    longitude_difference = lon2 - lon1
    a = (
        sin(latitude_difference / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(longitude_difference / 2) ** 2
    )
    return 6371 * 2 * asin(sqrt(min(1, a)))


def create_map(user_location):
    folium_map = folium.Map()

    nearest_point = None
    nearest_distance = float("inf")

    for point in clean_points:
        current_distance = distance_km(user_location, point["coords"])
        if current_distance < nearest_distance:
            nearest_distance = current_distance
            nearest_point = point

    folium.PolyLine(
        locations=[user_location, nearest_point["coords"]],
        color="orange",
        weight=3,
        tooltip=f"Distancia directa: {nearest_distance:.2f} km",
    ).add_to(folium_map)

    for point in clean_points:
        is_nearest = point is nearest_point
        popup = f"{point['nombre']} - {point['direccion']}"
        if is_nearest:
            popup += f"<br>Punto más cercano: {nearest_distance:.2f} km"

        folium.Marker(
            location=point["coords"],
            popup=popup,
            tooltip=f"{point['nombre']} (más cercano)" if is_nearest else point["nombre"],
            icon=folium.Icon(color="orange" if is_nearest else "green"),
        ).add_to(folium_map)

    folium.Marker(
        location=user_location,
        popup="Tu ubicación",
        tooltip="Tu ubicación",
        icon=folium.Icon(color="blue", icon="user", prefix="fa"),
    ).add_to(folium_map)

    folium_map.fit_bounds([point["coords"] for point in clean_points] + [user_location])
    return folium_map