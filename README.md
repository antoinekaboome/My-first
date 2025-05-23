# Product Catalog API

This project provides a small REST API built with **FastAPI** to manage products, categories and clients. It uses SQLite for storage and secures write operations with a minimal JWT based authentication.

## Structure

```
app/
    main.py          - FastAPI application entry point
    database.py      - SQLite connection and table creation
    auth.py          - JWT helpers
    schemas.py       - Pydantic models
    routes/
        users.py     - user registration and token routes
        categories.py- CRUD routes for categories
        products.py  - CRUD routes for products
        clients.py   - CRUD routes for clients
```

## Running locally

Install dependencies and start the server:

```bash
uvicorn app.main:app --reload --port 80
```

Obtain a token by registering a user at `POST /users/register` then requesting `POST /users/token`. Use this token in the `Authorization` header as `Bearer <token>` for all secured routes.

Swagger UI is available at `http://localhost/swagger`.

## Docker

Build and run the API in Docker:

```bash
docker build -t product-api .
docker run -p 80:80 product-api
```

`docker-compose.yml` provides a compose configuration that exposes port 80.

## Tests

Run the automated tests with:

```bash
pytest -q
```
