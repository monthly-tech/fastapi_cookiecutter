from datetime import datetime
import uuid
from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.settings.database import Base


class SuscriptionsType(Base):
    __tablename__ = "suscriptions_type"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)  # small, medium, large
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    # Relationships
    subscriptions = relationship("CompanyPaymentSuscription", back_populates="suscription_type")


class CompanyPaymentSuscription(Base):
    __tablename__ = "company_payment_suscription"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String)
    phone = Column(String, nullable=False)
    aux_phone = Column(String)
    init_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    is_trial = Column(Boolean)  # Nos indica si la suscription es del periodo de prueba
    suscription_upgrade = Column(Boolean)  # Nos indica si el cliente ya pago durante su periodo de prueba
    suscription_type_id = Column(UUID(as_uuid=True), ForeignKey('suscriptions_type.id'))
    external_id = Column(String)  # Referencia al metodo de pago registrado en Quentli
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.id'))
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    # Relationships
    company = relationship("Company", back_populates="payment_subscriptions")
    suscription_type = relationship("SuscriptionsType", back_populates="subscriptions")
    cards = relationship("CompanyCards", back_populates="subscription", cascade="all, delete-orphan")


class CompanyCards(Base):
    __tablename__ = "company_cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('company_payment_suscription.id'))  # Referencia según el DBML
    external_id = Column(String)  # Referencia al metodo de pago registrado en Quentli
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    # Relationships
    subscription = relationship("CompanyPaymentSuscription", back_populates="cards")
