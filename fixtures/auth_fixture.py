import pytest
from services.auth_service import AuthService

@pytest.fixture
def auth_token():
    """
    Shared login fixture
    """

    service = AuthService()
    token = service.login()

    return token