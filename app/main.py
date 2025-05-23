from fastapi import FastAPI
from app.routes import users, products
from app.routes import categories, clients

app = FastAPI(title="Product Catalog API")

app.include_router(users.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(clients.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=80)
