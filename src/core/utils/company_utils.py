

from decimal import Decimal

from sqlalchemy.orm import Session
from core.models.sizes_catalog import SizesCatalog


def get_company_size(session: Session, annual_income: Decimal) -> SizesCatalog:
    """
    Determine company size based on annual income.

    Args:
        annual_income (Decimal): The annual income of the company.

    Returns:
        SizesCatalog: The size category of the company.
    """
    # Filter active and non-deleted records where annual_income is >= income_size
    # Order by income_size descending to get the highest applicable tier
    data = (
        session.query(SizesCatalog)
        .filter(
            SizesCatalog.is_active,
            ~SizesCatalog.is_deleted
        )
        .order_by(SizesCatalog.income_size.asc())
        .all()
    )
    
    size = data[0]  # Default to the largest size if no match found
    for s in data:
        if annual_income >= Decimal(s.income_size):
            size = s
    return size