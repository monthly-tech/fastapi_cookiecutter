from schemas.database import UsersAccessLog as UsersAccessLogSchema, UsersAccessLogBase
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


# Schemas para requests de creación y actualización
class UsersAccessLogCreate(UsersAccessLogBase):
    """Schema para crear un nuevo log de acceso de usuario"""
    pass


class UsersAccessLogUpdate(BaseModel):
    """Schema para actualizar un log de acceso de usuario"""
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    accuracy: Optional[str] = None
    altitude_accuracy: Optional[str] = None
    heading: Optional[str] = None
    speed: Optional[str] = None


class UsersAccessLogResponse(UsersAccessLogSchema):
    """Schema para respuestas de log de acceso de usuario"""
    pass


class UsersAccessLogFilter(BaseModel):
    """Schema para filtros de búsqueda"""
    user_id: Optional[UUID] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
