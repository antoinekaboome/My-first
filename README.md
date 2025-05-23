# Product Catalog API

This project contains a simple REST API built with FastAPI to manage a product catalog. It demonstrates CRUD operations, JWT authentication and includes tests with Pytest. The API uses SQLite for persistence.

## Structure

```
app/
    main.py         - FastAPI application
    database.py     - SQLite connection and table creation
    auth.py         - minimal JWT implementation
    schemas.py      - Pydantic models
    routes/
        users.py    - user registration and token routes
        products.py - CRUD routes for products
```

## Running locally

Create a virtual environment with Python 3.11 and install `fastapi` and `uvicorn`. All other modules used are from the standard library.

```bash
uvicorn app.main:app --reload
```

Create a user with `POST /users/register` passing a JSON body `{"username": "myuser", "password": "mypassword"}`.
Retrieve a JWT token via `POST /users/token` with the same JSON body and use it in the
`Authorization` header as `Bearer <token>` for all `/products` operations.

The interactive API docs will be available at `http://localhost:80/docs`.

## Docker

A simple `Dockerfile` is provided to run the API. Build and run it with:

```bash
docker build -t product-api .
docker run -p 80:80 product-api
```

`docker-compose.yml` shows how to launch the container.

## Tests

Run the tests with:

```bash
pytest
```
