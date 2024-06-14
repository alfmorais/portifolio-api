import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from tests._factories.users import UserFactory

register(UserFactory, "user")


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="session")
def api_client_logged() -> APIClient:
    """
    TODO: Fazer uma fixture de usuário para criar a autenticação
    """
    return APIClient()
