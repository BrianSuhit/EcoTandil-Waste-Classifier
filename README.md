# ♻️ EcoTandil - Waste Classifier

>  **MVP de clasificación multimodal de residuos y geolocalización del Punto Limpio más cercano en Tandil.**

## Demostración

### Probar la aplicación
> 👉 **Demo interactiva:** [Probar la aplicación en vivo en Streamlit](https://ecotandil-waste-classifier-6hzvfigxvrrnjhjvijb44s.streamlit.app/)

### Vista Previa

| Ejemplo 1: Consulta de residuos | Ejemplo 2: Ubicación y Punto Limpio |
| :--- | :--- |
| **Entrada:** *"Tengo potes y sachets de yogurt de plástico vacío, ¿qué hago?"* | **Ubicación de prueba:** *Santamarina 165* |
| <img width="1565" height="675" alt="image" src="https://github.com/user-attachments/assets/329af3dc-e63f-4693-ba4b-730b9590d6aa" />| <img width="796" height="851" alt="image" src="https://github.com/user-attachments/assets/93bc086b-2e1e-4c0d-b3f3-f259cb7f5d52" />|


## Contexto
Diseñé este ultimo proyecto pensando directamente en el vecino y en los chicos que vienen de **ecoTips**: sirve tanto para el que ya recicla como para el que quiere empezar, o para cuando un chico pregunta: *"Quiero reciclar, ¿a dónde voy?"*.

Al consultar la web del Municipio de Tandil, noté algo muy claro: la sección de **Puntos Limpios** solo tiene una lista de direcciones en texto plano. No hay mapa ni forma de orientarse rápido; si no conocés bien la ciudad o sos de afuera, no te queda otra que copiar y pegar cada dirección a mano en Google Maps.

Pero ubicar un Punto Limpio no sirve de mucho si primero no sabés si lo que tenés en la mano te lo van a recibir. Por eso el proyecto se convirtió en una solución doble:
1.  **Clasificación multimodal asistida por IA:** Escribís en lenguaje natural qué querés reciclar o subís una foto del residuo, y el modelo te dice si el Punto Limpio lo acepta y cómo prepararlo (limpio, seco o atado).
2.  **Mapa y punto más cercano:** Marcás tu ubicación y la aplicación te muestra en un mapa todos los Puntos Limpios de Tandil, marcándote cuál te queda más cerca y a cuántos kilómetros está.

## Decisiones de Diseño y Trade-offs
Para este prototipo busqué un equilibrio entre facilidad para el vecino y rapidez de desarrollo, asumiendo los siguientes compromisos técnicos:

**Cálculo de distancia directa con Haversine (en vez de una API de mapas o base de datos geoespacial):**
-  *Pro:* Resuelve el cálculo en memoria al instante usando funciones matemáticas nativas de Python, sin dependencias pesadas ni costos de APIs externas para este MVP.
-  *Contra:* Mide la distancia en línea recta ("a vuelo de pájaro") y no el recorrido real por calles o tráfico. Para una versión en producción no alcanza: se necesitaría conectar un motor de ruteo o un servicio de GPS (como OSRM o Google Maps) que calcule el trayecto real a pie o en auto.

**Salida estructurada con Pydantic (modelo `recyclingReview`):**
-  *Pro:* Obliga al modelo a responder bajo un esquema fijo (`waste`, `is_recyclable`, `instructions`), lo que permite mostrar en Streamlit carteles claros (verde si es apto, rojo si no) y las indicaciones sin textos desordenados.
-  *Contra:* Si el vecino sube una foto con varios objetos distintos mezclados o algo ambiguo, el modelo está obligado a dar un único veredicto booleano (`True` o `False`), perdiendo el matiz de si una parte sirve y otra no.

**Modelo liviano en vez de un modelo más pesado:**
-  *Pro:* Respuesta muy rápida (pocos segundos) y costo casi cero para iterar y probar el clasificador.
-  *Contra:* En fotos con poca luz, ángulos difíciles o materiales dudosos, un modelo ligero tiene más probabilidad de equivocarse en la visión que un modelo más grande.

## Mejoras a futuro
-  **Switch dinámico de modelos en tiempo de ejecución:** Separar la carga según el tipo de consulta: usar un LLM optimizado puramente para texto cuando el vecino escribe, y derivar a un modelo multimodal especializado (como la familia nano-banana de Google) únicamente cuando se sube una foto, optimizando costos y tiempos de respuesta.
-  **Clasificación local en tiempo real con YOLO:** La evolución natural para la visión: entrenar o ajustar un modelo YOLO para detectar residuos reciclables. Esto permitiría clasificar objetos directo desde la cámara del celular, con latencia mínima y sin necesidad de enviar imágenes pesadas a una API externa.
-  **Ruteo real con GPS y navegación:** Reemplazar el cálculo en línea recta por integración con geolocalización real del dispositivo y un motor de ruteo (OSRM o Google Maps) que trace el camino exacto por calles hasta el Punto Limpio.
-  **Resolución de casos ambiguos en la salida estructurada:** Migrar a un modelo con mayor capacidad de razonamiento visual para que el esquema estructurado no fuerce un "sí o no" simplista, sino que pueda desglosar residuos compuestos (por ejemplo: *"el frasco de vidrio sí, pero sacale la tapa plástica"*).

## Stack Tecnológico
- **Lenguaje:** Python 3.14
- **Frontend / UI:** Streamlit
- **LLM:** Google Gemini (`gemini-3.5-flash-lite` vía `google-genai`)
- **Mapas y visualización geoespacial:** Folium & Streamlit-Folium
-  **Geolocalización:** Streamlit-Geolocation

## Estructura del Proyecto
```text
ecotandil-waste-classifier/
├── app.py     # Interfaz de usuario con Streamlit
├── main.py    # Servicio de clasificación multimodal con Gemini (manejo de base64 y reglas oficiales)
├── map.py     # Cálculo de distancia geodésica (Haversine) y renderizado del mapa con Folium
└── models.py  # Modelo Pydantic (contrato de salida estructurada: recyclingReview)
```

## Quickstart (Cómo correrlo en local)

### 1. Clonar el repositorio

```bash
git clone https://github.com/BrianSuhit/EcoTandil-Waste-Classifier.git
cd EcoTandil-Waste-Classifier
```

### 2. Instalar dependencias con uv

```bash
uv sync
```

### 3. Configurar variables de entorno

Creá un archivo `.env` en la raíz del proyecto (o exportá la variable en tu terminal):

```env
GEMINI_API_KEY="tu_api_key_aqui"
```

### 4. Iniciar la aplicación

```bash
uv run streamlit run app.py
```
