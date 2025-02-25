"""Test cases for Permissions Check component."""

from unittest.mock import AsyncMock, patch

import pytest
from langflow.schema.message import Message

from components.permissions_check import PermissionsCheckComponent


@pytest.fixture
def component():
    return PermissionsCheckComponent()


@pytest.mark.asyncio
async def test_initialization(component):
    assert component.display_name == "Permissions Check"

@pytest.mark.asyncio
async def test_allowed_result():
    component.user_id = "test-user"
    component.action = "book"
    component.resource = "flight"
    component.pdp_url = "https://cloudpdp.api.permit.io"
    component.api_key = "test-key"

    with patch("permit.Permit") as mock_permit:
        mock_permit.return_value.check = AsyncMock(return_value=True)
        await component.validate_auth()  # Sets self.status
        result = component.allowed_result()
        assert isinstance(result, Message)
        assert result.content == "Permission granted for test-user to book on flight"

        mock_permit.return_value.check = AsyncMock(return_value=False)
        await component.validate_auth()
        result = component.allowed_result()
        assert isinstance(result, Message)
        assert result.content == ""


@pytest.mark.asyncio
async def test_denied_result():
    component.user_id = "test-user"
    component.action = "book"
    component.resource = "flight"
    component.pdp_url = "https://cloudpdp.api.permit.io"
    component.api_key = "test-key"

    with patch("permit.Permit") as mock_permit:
        mock_permit.return_value.check = AsyncMock(return_value=False)
        await component.validate_auth()
        result = component.denied_result()
        assert isinstance(result, Message)
        assert result.content == "Permission denied for test-user to book on flight"

        mock_permit.return_value.check = AsyncMock(return_value=True)
        await component.validate_auth()
        result = component.denied_result()
        assert isinstance(result, Message)
        assert result.content == ""


@pytest.mark.asyncio
async def test_validate_auth_with_tenant():
    component.user_id = "test-user"
    component.action = "book"
    component.resource = "flight"
    component.tenant = "tenant-1"
    component.pdp_url = "https://cloudpdp.api.permit.io"
    component.api_key = "test-key"

    with patch("permit.Permit") as mock_permit:
        mock_permit.return_value.check = AsyncMock(return_value=True)
        result = await component.validate_auth()
        assert result is True
        mock_permit.return_value.check.assert_awaited_with(
            "test-user", "book", "flight", context={"tenant": "tenant-1"}
        )
