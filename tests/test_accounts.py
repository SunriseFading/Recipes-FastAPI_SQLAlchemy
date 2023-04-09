from app.utils.messages import messages
from fastapi import status
from pytest_mock import MockerFixture
from tests.settings import test_user, urls


class TestRegister:
    async def test_register_user(self, client, mocker: MockerFixture):
        response = client.post(
            urls.register,
            json={"email": test_user.email, "password": test_user.password},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("detail") == messages.USER_CREATED

    async def test_failed_repeat_register_user(self, register_user, client):
        response = client.post(
            urls.register,
            json={"email": test_user.email, "password": test_user.password},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json().get("detail") == messages.USER_ALREADY_EXISTS

    async def test_login_unregistered_user(self, client):
        response = client.post(
            urls.login, json={"email": test_user.email, "password": test_user.password}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get("detail") == messages.USER_NOT_FOUND


class TestLogin:
    async def test_login_user(self, register_user, client):
        response = client.post(
            urls.login, json={"email": test_user.email, "password": test_user.password}
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    async def test_wrong_password_login(self, register_user, client):
        response = client.post(
            urls.login,
            json={"email": test_user.email, "password": test_user.wrong_password},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get("detail") == messages.WRONG_PASSWORD


class TestLogout:
    async def test_logout_user(self, auth_client):
        response = auth_client.delete(urls.logout)
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.USER_LOGOUT
