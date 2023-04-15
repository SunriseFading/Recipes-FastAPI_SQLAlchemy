# Launch guide
1. In the root directory, rename the file '.env.example' to '.env', unzip the database:
```
sudo tar xvzf postgres_data.tar.gz
```
2. In the terminal execute the command:
```
docker compose up --build
```
3. To run the tests, run the following command:
```
docker exec fastapi pytest
```
4. Swagger is located at localhost:8000/docs#/

# Features:
- Creating a new recipe (name, description, ingredients, steps of preparation)
- Database filled with 100 recipes
- Getting a list of all recipes
- Getting information about specific recipe by ID
- Edit recipe by ID
- Removal of recipe by ID
- User authentication and authorization. Only authorized users can create, edit, and delete recipes
- Filter and sorting by total cooking time.
- Ability to add assessment. Users can rate recipes on a scale from 1 to 5. Filter and sort the list by rating.
- Filter on the list of ingredients.
- Ability to upload photos for recipe and cooking steps, realize loading and recoil images.
- Code covered with tests
