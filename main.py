import base64
from google import genai
from models import recyclingReview

cliente = genai.Client()
system_instruction = """Eres el clasificador oficial de Punto Limpio Tandil. Tu tarea es clasificar si los residuos indicados por el usuario (en texto o imagen) son aptos para ser recibidos en Punto Limpio.

REGLAS DE CLASIFICACIÓN:
1. ÚNICAMENTE se consideran reciclables (es_reciclable = True) los siguientes materiales:
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
   - Debes marcar es_reciclable = False.
   - En instrucciones, aclara que no se recibe en Punto Limpio y que debe ir a recolección domiciliaria o al circuito correspondiente.
3. Si es reciclable, brinda instrucciones claras de acondicionamiento (ej: limpios, secos, aplastados, botellas cerradas para el aceite)."""


def clasificar_residuo(texto, bytes_imagen=None, tipo_mime="image/jpeg"):
    entrada = texto
    if bytes_imagen is not None:
        imagen_codificada = base64.b64encode(bytes_imagen).decode("utf-8")
        entrada = [{"type": "image", "data": imagen_codificada, "mime_type": tipo_mime}]
    interaction = cliente.interactions.create(
        model="gemini-3.5-flash-lite",
        system_instruction=system_instruction,
        input=entrada,
        response_format={"type": "text", 
                        "mime_type": "application/json", 
                        "schema": recyclingReview.model_json_schema()},
        stream=False,
    )
    return recyclingReview.model_validate_json(interaction.output_text)