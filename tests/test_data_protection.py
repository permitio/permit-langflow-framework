"""Test cases for Data Protection component."""

from unittest.mock import AsyncMock, patch

import pytest
from components.data_protection import DataProtectionComponent


@pytest.fixture
def mock_permit_client():
    """Create a mock Permit client."""
    return AsyncMock()


@pytest.fixture
def component():
    """Create a component instance."""
    return DataProtectionComponent()


@pytest.mark.asyncio
async def test_initialization(component):
    """Test Data Protection initialization."""
    assert component.display_name == "Data Protection"

@pytest.mark.asyncio
async def test_get_all_permissions(component, mock_permit_client):
    """Test retrieving all permissions."""
    mock_permissions = [
        AsyncMock(resource_id="flight-001", resource="flight", action="book"),
        AsyncMock(resource_id="flight-002", resource="flight", action="book"),
        AsyncMock(resource_id="flight-003", resource="flight", action="view"),
    ]

    with patch("permit.Permit") as mock_permit:
        mock_permit.return_value.get_user_permissions = AsyncMock(return_value=mock_permissions)
        component.user_id = "test-user"
        component.action = "book"
        component.resource_type = "flight"
        component.pdp_url = "https://cloudpdp.api.permit.io"
        component.api_key = "test-key"

        result = await component.validate_auth()
        assert isinstance(result, list)
        assert len(result) == 2
        assert "flight-001" in result
        assert "flight-002" in result
        assert "flight-003" not in result
