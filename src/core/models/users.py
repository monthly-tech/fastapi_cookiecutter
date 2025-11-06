from datetime import datetime
import uuid
from sqlalchemy import Column, String, Boolean, TIMESTAMP, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.settings.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String, nullable=False)  # user identificator from firebase auth
    username = Column(String)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String)
    surname = Column(String, nullable=False)
    second_surname = Column(String)
    phone = Column(String, nullable=False)
    second_phone = Column(String)
    role = Column(String, nullable=False)
    job_position = Column(String, nullable=False)
    other_job_position = Column(String)  # Si se selecciona otro tipo de Rol aquí se guardará el string correspondiente
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    # Relationships
    user_companies = relationship("UserCompany", back_populates="user", cascade="all, delete-orphan")
    access_logs = relationship("UsersAccessLog", back_populates="user", cascade="all, delete-orphan")
