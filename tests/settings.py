from app.schemas.reviews import ReviewParams


class Urls:
    login = "/accounts/login/"
    register = "/accounts/register/"
    logout = "/accounts/logout/"

    create_recipe = "/recipes/create/"
    update_recipe = "/recipes/update/"
    delete_recipe = "/recipes/delete/"
    get_recipes = "/recipes/get/"
    create_review = "/reviews/create/"


class TestUser:
    email = "test@mail.ru"
    password = "TestPassword"
    wrong_password = "WrongPassword"


urls = Urls()
test_user = TestUser()


test_recipe = {
    "name": "TestRecipe",
    "description": "Description",
    "ingredients": [{"name": "onion"}, {"name": "milk"}, {"name": "tomato"}],
    "steps": [
        {"name": "prepare", "time": 2, "description": "prepare all"},
        {"name": "middle", "time": 10, "description": "cook"},
        {"name": "complete", "time": 30, "description": "complete all"},
    ],
}

updated_recipe = {
    "name": "NewTestRecipe",
    "description": test_recipe.get("description"),
    "ingredients": test_recipe.get("ingredients"),
    "steps": [
        {"name": "prepare", "time": 21, "description": "prepare all"},
        {"name": "middle", "time": 101, "description": "cook"},
        {"name": "complete", "time": 301, "description": "complete all"},
    ],
}
total_time = sum(step.get("time") for step in test_recipe.get("steps"))
total_time_updated = sum(step.get("time") for step in updated_recipe.get("steps"))

rating = {"rating": 2}
