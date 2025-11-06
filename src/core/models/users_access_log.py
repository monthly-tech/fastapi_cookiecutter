from datetime import datetime
import uuid
from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.settings.database import Base


class UsersAccessLog(Base):
    __tablename__ = "users_access_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    latitude = Column(String)
    longitude = Column(String)
    accuracy = Column(String)
    altitude_accuracy = Column(String)
    heading = Column(String)
    speed = Column(String)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    # Relationships
    user = relationship("User", back_populates="access_logs")

    def __repr__(self):
        return f"<UsersAccessLog(id={self.id}, user_id={self.user_id}, created_at={self.created_at})>"
