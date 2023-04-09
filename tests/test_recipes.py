from app.utils.messages import messages
from fastapi import status
from tests.settings import (
    rating,
    test_recipe,
    total_time,
    total_time_updated,
    updated_recipe,
    urls,
)


class TestRecipe:
    async def test_not_available_without_auth(self, client):
        response = client.post(urls.create_recipe, json=test_recipe)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_recipe(self, auth_client):
        response = auth_client.post(urls.create_recipe, json=test_recipe)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("detail") == messages.RECIPE_CREATED

        response = auth_client.get(f"{urls.get_recipes}1")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result.get("name") == test_recipe.get("name")
        assert result.get("description") == test_recipe.get("description")
        assert result.get("average_rating") is None
        assert int(result.get("total_time")) == total_time

    async def test_update_recipe(self, auth_client, create_recipe):
        response = auth_client.post(f"{urls.update_recipe}1", json=updated_recipe)
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json().get("detail") == messages.RECIPE_UPDATED

        response = auth_client.get(f"{urls.get_recipes}1")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()

        response = auth_client.get(urls.get_recipes)
        assert result == response.json()[0]

        assert result.get("description") == updated_recipe.get("description")
        assert result.get("name") == updated_recipe.get("name")
        assert result.get("average_rating") is None
        assert int(result.get("total_time")) == total_time_updated

    async def test_delete_recipe(self, auth_client, create_recipe):
        response = auth_client.delete(f"{urls.delete_recipe}1")
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.RECIPE_DELETED

        response = auth_client.get(urls.get_recipes)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == None


class TestReview:
    async def test_not_available_without_auth(self, client):
        response = client.post(f"{urls.create_review}1", params=rating)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_review(self, create_recipe, auth_client):
        response = auth_client.post(f"{urls.create_review}1", params=rating)
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.REVIEW_SAVED

        response = auth_client.get(f"{urls.get_recipes}1")
        assert response.status_code == status.HTTP_200_OK
        assert float(response.json().get("average_rating")) == rating.get("rating")
