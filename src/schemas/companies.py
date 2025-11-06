from schemas.database import (
    Company as CompanySchema,
    CompanyBase,
    CompanyAddress as CompanyAddressSchema,
    CompanyAddressBase,
    BusinessUnit as BusinessUnitSchema,
    BusinessUnitBase,
    Country as CountrySchema,
    CountryBase,
    Industry as IndustrySchema,
    IndustryBase,
    SubIndustry as SubIndustrySchema,
    SubIndustryBase
)
from typing import Optional, List
from uuid import UUID
from decimal import Decimal


# Schemas para Country
class CountryCreate(CountryBase):
    """Schema para crear un nuevo país"""
    pass


class CountryResponse(CountrySchema):
    """Schema para respuestas de país"""
    pass


# Schemas para Industry
class IndustryCreate(IndustryBase):
    """Schema para crear una nueva industria"""
    pass


class IndustryResponse(IndustrySchema):
    """Schema para respuestas de industria"""
    pass


# Schemas para SubIndustry
class SubIndustryCreate(SubIndustryBase):
    """Schema para crear una nueva sub-industria"""
    pass


class SubIndustryResponse(SubIndustrySchema):
    """Schema para respuestas de sub-industria"""
    pass


# Schemas para BusinessUnit
class BusinessUnitCreate(BusinessUnitBase):
    """Schema para crear una nueva unidad de negocio"""
    pass


class BusinessUnitResponse(BusinessUnitSchema):
    """Schema para respuestas de unidad de negocio"""
    pass


# Schemas para requests de creación y actualización de direcciones
class CompanyAddressCreate(CompanyAddressBase):
    """Schema para crear una nueva dirección de empresa"""
    pass


class CompanyAddressUpdate(CompanyAddressBase):
    """Schema para actualizar una dirección de empresa"""
    is_main: Optional[bool] = None
    countries_id: Optional[UUID] = None
    country: Optional[str] = None
    zip_code: Optional[int] = None
    state: Optional[str] = None
    city: Optional[str] = None
    municipality: Optional[str] = None
    suburb: Optional[str] = None
    street: Optional[str] = None
    external_number: Optional[str] = None
    internal_number: Optional[str] = None
    is_active: Optional[bool] = None


class CompanyAddressResponse(CompanyAddressSchema):
    """Schema para respuestas de dirección de empresa"""
    pass


# Schemas para requests de creación y actualización de empresas
class CompanyCreate(CompanyBase):
    """Schema para crear una nueva empresa"""
    origin_country_id: UUID
    industry_id: Optional[UUID] = None
    sub_industry_id: Optional[UUID] = None
    user_ids: List[UUID] = []  # Lista de usuarios a asociar con la empresa
    addresses: Optional[List[CompanyAddressCreate]] = []
    business_units: Optional[List[BusinessUnitCreate]] = []


class CompanyUpdate(CompanyBase):
    """Schema para actualizar una empresa"""
    external_id: Optional[int] = None
    website: Optional[str] = None
    description: Optional[str] = None
    logo_path: Optional[str] = None
    commercial_name: Optional[str] = None
    linkedin_url: Optional[str] = None
    employees_lenght: Optional[int] = None
    annual_income: Optional[Decimal] = None
    status: Optional[str] = None
    # company_size: Optional[str] = None
    origin_country_id: Optional[UUID] = None
    fiscal_identifier: Optional[str] = None
    identifier_type: Optional[str] = None
    legal_name: Optional[str] = None
    industry_id: Optional[UUID] = None
    sub_industry_id: Optional[UUID] = None
    invoices_email: Optional[str] = None
    has_business_units: Optional[bool] = None
    is_active: Optional[bool] = None


class CompanyResponse(CompanySchema):
    """Schema para respuestas de empresa"""
    addresses: Optional[List[CompanyAddressResponse]] = []
    business_units: Optional[List[BusinessUnitResponse]] = []
    monthly_country: Optional[CountryResponse] = None
    origin_country: Optional[CountryResponse] = None
    industry: Optional[IndustryResponse] = None
    sub_industry: Optional[SubIndustryResponse] = None

    class Config:
        from_attributes = True
