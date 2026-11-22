import base64
from google import genai
from google.genai.errors import APIError
from models import recyclingReview

client = genai.Client()
system_instruction = """Eres el clasificador oficial de Punto Limpio Tandil. Tu tarea es clasificar si los residuos indicados por el usuario (en texto o imagen) son aptos para ser recibidos en Punto Limpio.

REGLAS DE CLASIFICACIÓN:
1. ÚNICAMENTE se consideran reciclables (is_recyclable = True) los siguientes materiales:
   - Vidrio
   - Cartón
   - Botellas de plástico
   - Latas
   - Aerosoles
   - Telgopor
   - Envases de tetra brik
   - Rezagos informáticos (electrónicos pequeños, PCs, impresoras, cables)
   - Aceite de cocina usado
   - Sachets
2. Si el usuario presenta CUALQUIER OTRO residuo (basura orgánica, restos de comida, escombros, ropa, pilas comunes, muebles, residuos patogénicos):
   - Debes marcar is_recyclable = False.
   - En instrucciones, aclara que no se recibe en Punto Limpio y que debe ir a recolección domiciliaria o al circuito correspondiente.
3. Si es reciclable, brinda instrucciones claras de acondicionamiento (ej: limpios, secos, aplastados, botellas cerradas para el aceite)."""


def classify_waste(text, image_bytes=None, mime_type="image/jpeg"):
    try:
        input_data = text
        if image_bytes is not None:
            encoded_image = base64.b64encode(image_bytes).decode("utf-8")
            input_data = [{"type": "image", "data": encoded_image, "mime_type": mime_type}]
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            system_instruction=system_instruction,
            input=input_data,
            response_format={"type": "text",
                            "mime_type": "application/json",
                            "schema": recyclingReview.model_json_schema()},
            stream=False,
        )
        return recyclingReview.model_validate_json(interaction.output_text)
    except APIError as error:
        print(f"Error de API en classify_waste: {error}")
        raise
    except Exception as error:
        print(f"Error inesperado en classify_waste: {error}")
        raise