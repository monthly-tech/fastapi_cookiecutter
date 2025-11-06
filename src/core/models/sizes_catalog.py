from datetime import datetime
import uuid
from sqlalchemy import Column, String, Boolean, TIMESTAMP, Float
from sqlalchemy.dialects.postgresql import UUID
from core.settings.database import Base


class SizesCatalog(Base):
    __tablename__ = "sizes_catalog"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)  # XS, S, M, L, XL, XXL
    income_size = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    def __repr__(self):
        return f"<SizesCatalog(id={self.id}, name='{self.name}', income_size={self.income_size})>"
