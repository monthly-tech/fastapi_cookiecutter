from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from decimal import Decimal


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    second_name: Optional[str] = None
    surname: str
    second_surname: Optional[str] = None
    phone: str
    second_phone: Optional[str] = None
    role: Optional[str] = None
    job_position: str
    other_job_position: Optional[str] = None  # Si se selecciona otro tipo de Rol aquí se guardará el string correspondiente
    is_active: bool = True


class User(UserBase):
    id: UUID
    external_id: str  # user identificator from firebase auth
    is_deleted: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        from_attributes = True


class CountryBase(BaseModel):
    name: str
    code_iso_alpha_2: str
    code_iso_alpha_3: str
    phone_code: Optional[str] = None
    monthly_use: Optional[bool] = False
    is_active: bool = True


class Country(CountryBase):
    id: UUID
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class IndustryBase(BaseModel):
    name: Optional[str] = None
    code: int
    description: Optional[str] = None
    is_active: bool = True


class Industry(IndustryBase):
    id: UUID
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SubIndustryBase(BaseModel):
    name: Optional[str] = None
    code: int
    description: Optional[str] = None
    is_active: bool = True


class SubIndustry(SubIndustryBase):
    id: UUID
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BusinessUnitBase(BaseModel):
    name: str
    is_active: bool = True


class BusinessUnit(BusinessUnitBase):
    id: UUID
    company_id: UUID
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserCompanyBase(BaseModel):
    is_active: bool = True


class UserCompany(UserCompanyBase):
    user_id: UUID
    company_id: UUID
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompanyAddressBase(BaseModel):
    is_main: Optional[bool] = None
    countries_id: Optional[UUID] = None  # País que se selecciona en si es MX, USA o LATAM va vinculado al catalogo countries
    country: Optional[str] = None  # País - Se puede extraer de la seleccion del pais a nivel catalogo (Solo informativo)
    zip_code: int  # Código postal
    state: str  # Estado
    city: str  # Ciudad
    municipality: Optional[str] = None  # Municipio
    suburb: Optional[str] = None  # Colonia
    street: str  # Del extractor CSF se extraen y concatenan los parámetros 'Entre calle y calle'
    external_number: str
    internal_number: Optional[str] = None
    is_active: bool = True


class CompanyAddress(CompanyAddressBase):
    id: UUID
    company_id: UUID
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompanyBase(BaseModel):
    external_id: int  # company identificator from master de clientes monthly
    website: Optional[str] = None
    description: Optional[str] = None
    logo_path: Optional[str] = None
    commercial_name: str
    linkedin_url: Optional[str] = None  # Este seria de tipo optional
    employees_lenght: Optional[int] = None
    annual_income: Optional[Decimal] = None
    status: Optional[str] = None  # Para manejar si la compañía ya finalizó su proceso de Onboarding
    # company_size: Optional[str] = None  # Opciones disponibles 'Xs S M L XL o XXL'
    company_size_id: Optional[UUID] = None
    fiscal_identifier: str
    identifier_type: Optional[str] = None  # Las opciones serian CSF(For MX), W9(For USA) o Manual(For LATAM)
    legal_name: str
    invoices_email: Optional[str] = None
    question_info: Optional[str] = None
    has_business_units: Optional[bool] = None
    is_active: bool = True


class Company(CompanyBase):
    id: UUID
    origin_country_id: UUID
    industry_id: Optional[UUID] = None
    sub_industry_id: Optional[UUID] = None
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SizesCatalogBase(BaseModel):
    name: str
    income_size: float
    is_active: bool = True


class SizesCatalog(SizesCatalogBase):
    id: UUID
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsersAccessLogBase(BaseModel):
    user_id: UUID
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    accuracy: Optional[str] = None
    altitude_accuracy: Optional[str] = None
    heading: Optional[str] = None
    speed: Optional[str] = None


class UsersAccessLog(UsersAccessLogBase):
    id: UUID
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
