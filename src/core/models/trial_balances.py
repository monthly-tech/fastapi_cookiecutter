from datetime import datetime
import uuid
from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, NUMERIC
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.settings.database import Base


class TrialBalancesRawFormat(Base):
    __tablename__ = "trial_balances_raw_format"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.id'))
    period_month = Column(String)
    period_year = Column(String)
    source_file_name = Column(String)
    upload_date = Column(TIMESTAMP)
    provider_id = Column(UUID(as_uuid=True))
    account_number = Column(String)
    account_name = Column(String)
    initial_debit_balance = Column(NUMERIC)
    initial_credit_balance = Column(NUMERIC)
    debit_movements = Column(NUMERIC)
    credit_movements = Column(NUMERIC)
    current_debit_balance = Column(NUMERIC)
    current_credit_balance = Column(NUMERIC)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    # Relationships
    company = relationship("Company", back_populates="trial_balances_raw")


class TrialBalancesMonthlyFormat(Base):
    __tablename__ = "trial_balances_monthly_format"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.id'))
    period_month = Column(String)
    period_year = Column(String)
    source_file_name = Column(String)
    upload_date = Column(TIMESTAMP)
    provider_id = Column(UUID(as_uuid=True))
    account_number = Column(String)
    account_name = Column(String)
    initial_debit_balance = Column(NUMERIC)
    initial_credit_balance = Column(NUMERIC)
    debit_movements = Column(NUMERIC)
    credit_movements = Column(NUMERIC)
    current_debit_balance = Column(NUMERIC)
    current_credit_balance = Column(NUMERIC)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    # Relationships
    company = relationship("Company", back_populates="trial_balances_monthly")
