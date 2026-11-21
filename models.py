from pydantic import BaseModel, Field

class recyclingReview(BaseModel):
    residuo: str = Field(
        description=(
            "Nombre o listado claro y conciso de los objetos o materiales"
            " identificados (ej: 'Impresora vieja y cajas de tetra brick')."
        )
    )
    es_reciclable: bool = Field(
        description=(
            "True si los materiales son aptos para ser recibidos en los Puntos"
            " Limpios de Tandil; False si son residuos no admitidos (orgánicos,"
            " basura común, patogénicos, etc.)."
        )
    )
    instrucciones: str = Field(
        description=(
            "Indicaciones prácticas y puntuales para acondicionar y entregar el"
            " material (ej: desarmar, limpiar, secar, quitar cables o tapas). Si"
            " no es reciclable, indicar que corresponde a la recolección"
            " domiciliaria habitual."
        )
    )