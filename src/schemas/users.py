from schemas.database import User as UserSchema, UserBase
from typing import Optional


# Schemas para requests de creación y actualización
class UserCreate(UserBase):
    """Schema para crear un nuevo usuario"""
    external_id: str  # Ahora es requerido según el SQL


class UserUpdate(UserBase):
    """Schema para actualizar un usuario"""
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    surname: Optional[str] = None
    second_surname: Optional[str] = None
    phone: Optional[str] = None
    second_phone: Optional[str] = None
    role: Optional[str] = None
    job_position: Optional[str] = None
    other_job_position: Optional[str] = None
    is_active: Optional[bool] = None
    external_id: Optional[str] = None


class UserResponse(UserSchema):
    """Schema para respuestas de usuario"""
    pass
