from datetime import datetime
import uuid
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, NUMERIC
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.settings.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)  # México, Argentina, Panamá, Peru, Chile, Colombia, Estados Unidos
    code_iso_alpha_2 = Column(String, nullable=False)
    code_iso_alpha_3 = Column(String, nullable=False)
    phone_code = Column(String)
    monthly_use = Column(Boolean, default=False)  # Indica si el país es de uso para monthly
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)


class Industry(Base):
    __tablename__ = "industry"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    code = Column(Integer, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    # Relationships
    companies = relationship("Company", back_populates="industry")


class SubIndustry(Base):
    __tablename__ = "sub_industry"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    code = Column(Integer, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    # Relationships
    companies = relationship("Company", back_populates="sub_industry")


class Company(Base):
    __tablename__ = "company"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(Integer, nullable=False)  # company identificator from master de clientes monthly
    website = Column(String)
    description = Column(String)
    logo_path = Column(String)
    commercial_name = Column(String, nullable=False)
    linkedin_url = Column(String)  # Este seria de tipo optional
    employees_lenght = Column(Integer)
    annual_income = Column(NUMERIC)
    status = Column(String)  # Para manejar si la compañía ya finalizó su proceso de Onboarding
    company_size_id = Column(String)  # Opciones disponibles 'Xs S M L XL o XXL'
    origin_country_id = Column(UUID(as_uuid=True), ForeignKey('countries.id'))
    fiscal_identifier = Column(String, nullable=False)
    identifier_type = Column(String)  # Las opciones serian CSF(For MX), W9(For USA) o Manual(For LATAM)
    legal_name = Column(String, nullable=False)
    industry_id = Column(UUID(as_uuid=True), ForeignKey('industry.id'))
    sub_industry_id = Column(UUID(as_uuid=True), ForeignKey('sub_industry.id'))
    invoices_email = Column(String)
    question_info = Column(String)
    has_business_units = Column(Boolean)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    # Relationships
    origin_country = relationship("Country", foreign_keys=[origin_country_id])
    industry = relationship("Industry", back_populates="companies")
    sub_industry = relationship("SubIndustry", back_populates="companies")
    addresses = relationship("CompanyAddress", back_populates="company", cascade="all, delete-orphan")
    business_units = relationship("BusinessUnit", back_populates="company", cascade="all, delete-orphan")
    user_companies = relationship("UserCompany", back_populates="company", cascade="all, delete-orphan")
    providers_tokens = relationship("ProvidersTokens", back_populates="company", cascade="all, delete-orphan")
    trial_balances_raw = relationship("TrialBalancesRawFormat", back_populates="company", cascade="all, delete-orphan")
    trial_balances_monthly = relationship("TrialBalancesMonthlyFormat", back_populates="company", cascade="all, delete-orphan")
    payment_subscriptions = relationship("CompanyPaymentSuscription", back_populates="company", cascade="all, delete-orphan")


class BusinessUnit(Base):
    __tablename__ = "business_units"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.id'), nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    # Relationships
    company = relationship("Company", back_populates="business_units")


class UserCompany(Base):
    __tablename__ = "user_company"

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.id'), primary_key=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    # Relationships
    user = relationship("User", back_populates="user_companies")
    company = relationship("Company", back_populates="user_companies")


class CompanyAddress(Base):
    __tablename__ = "company_address"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.id'), nullable=False)
    is_main = Column(Boolean)
    countries_id = Column(UUID(as_uuid=True), ForeignKey('countries.id'))  # País que se selecciona en si es MX, USA o LATAM va vinculado al catalogo countries
    country = Column(String)  # País - Se puede extraer de la seleccion del pais a nivel catalogo (Solo informativo)
    zip_code = Column(Integer, nullable=False)  # Código postal
    state = Column(String, nullable=False)  # Estado
    city = Column(String, nullable=False)  # Ciudad
    municipality = Column(String)  # Municipio
    suburb = Column(String)  # Colonia
    street = Column(String, nullable=False)  # Del extractor CSF se extraen y concatenan los parámetros 'Entre calle y calle'
    external_number = Column(String, nullable=False)
    internal_number = Column(String)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    # Relationships
    company = relationship("Company", back_populates="addresses")
    country_catalog = relationship("Country", foreign_keys=[countries_id])
