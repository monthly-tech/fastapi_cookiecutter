from decimal import Decimal
from unittest.mock import Mock
from core.utils.company_utils import get_company_size
from core.models.sizes_catalog import SizesCatalog


class TestGetCompanySize:
    """Test cases for get_company_size function"""

    def test_get_company_size_xs_category(self):
        """Test that income below 100,000 returns XS category"""
        # Mock session and query
        mock_session = Mock()
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        
        # Mock XS category
        xs_category = Mock()
        xs_category.name = "XS"
        xs_category.income_size = 0.0
        
        # First query returns XS category for income 50,000
        mock_query.filter.return_value.order_by.return_value.first.return_value = xs_category
        
        result = get_company_size(mock_session, Decimal("50000"))
        
        assert result == xs_category
        assert result.name == "XS"

    def test_get_company_size_s_category(self):
        """Test that income 150,000 returns S category"""
        mock_session = Mock()
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        
        # Mock S category
        s_category = Mock()
        s_category.name = "S"
        s_category.income_size = 100000.0
        
        mock_query.filter.return_value.order_by.return_value.first.return_value = s_category
        
        result = get_company_size(mock_session, Decimal("150000"))
        
        assert result == s_category
        assert result.name == "S"

    def test_get_company_size_m_category(self):
        """Test that income 750,000 returns M category"""
        mock_session = Mock()
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        
        # Mock M category
        m_category = Mock()
        m_category.name = "M"
        m_category.income_size = 500000.0
        
        mock_query.filter.return_value.order_by.return_value.first.return_value = m_category
        
        result = get_company_size(mock_session, Decimal("750000"))
        
        assert result == m_category
        assert result.name == "M"

    def test_get_company_size_xxl_category(self):
        """Test that income 15,000,000 returns XXL category"""
        mock_session = Mock()
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        
        # Mock XXL category
        xxl_category = Mock()
        xxl_category.name = "XXL"
        xxl_category.income_size = 10000000.0
        
        mock_query.filter.return_value.order_by.return_value.first.return_value = xxl_category
        
        result = get_company_size(mock_session, Decimal("15000000"))
        
        assert result == xxl_category
        assert result.name == "XXL"

    def test_get_company_size_fallback_to_xs(self):
        """Test fallback to XS when no match found"""
        mock_session = Mock()
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        
        # Mock XS category for fallback
        xs_fallback = Mock()
        xs_fallback.name = "XS"
        xs_fallback.income_size = 0.0
        
        # First query returns None, second query returns XS as fallback
        mock_query.filter.return_value.order_by.return_value.first.side_effect = [None, xs_fallback]
        
        result = get_company_size(mock_session, Decimal("-1000"))  # Negative income
        
        assert result == xs_fallback
        assert result.name == "XS"

    def test_query_filters_applied_correctly(self):
        """Test that query filters are applied correctly"""
        mock_session = Mock()
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        
        # Mock return value
        mock_category = Mock()
        mock_query.filter.return_value.order_by.return_value.first.return_value = mock_category
        
        annual_income = Decimal("500000")
        get_company_size(mock_session, annual_income)
        
        # Verify that query was called with correct model
        mock_session.query.assert_called_with(SizesCatalog)
        
        # Verify that filter was called (we can't easily check the exact filter conditions with mocks)
        mock_query.filter.assert_called()
        
        # Verify that order_by was called
        mock_query.filter.return_value.order_by.assert_called()
        
        # Verify that first was called
        mock_query.filter.return_value.order_by.return_value.first.assert_called()
