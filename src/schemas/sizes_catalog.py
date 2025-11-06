from typing import Optional
from pydantic import BaseModel
from schemas.database import (
    SizesCatalog as SizesCatalogSchema,
    SizesCatalogBase,
)


# Schemas para SizesCatalog
class SizesCatalogCreate(SizesCatalogBase):
    """Schema para crear un nuevo tamaño de catálogo"""
    pass


class SizesCatalogUpdate(BaseModel):
    """Schema para actualizar un tamaño de catálogo"""
    name: Optional[str] = None
    income_size: Optional[float] = None
    is_active: Optional[bool] = None


class SizesCatalogResponse(SizesCatalogSchema):
    """Schema para respuestas de tamaño de catálogo"""
    pass


__all__ = [
    "SizesCatalogCreate",
    "SizesCatalogUpdate", 
    "SizesCatalogResponse"
]
