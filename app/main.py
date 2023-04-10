import uvicorn
from app.routers import recipes, reviews, steps, users
from app.routers.auth import app
from fastapi_pagination import add_pagination

app.include_router(users.router)
app.include_router(recipes.router)
app.include_router(steps.router)
app.include_router(reviews.router)
add_pagination(app)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
