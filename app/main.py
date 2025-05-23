from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

from app.routes import users, products, categories, clients


app = FastAPI(title="Product Catalog API", docs_url="/swagger")

app.include_router(users.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(clients.router)


@app.get("/", response_class=HTMLResponse)
def read_index():
    """Serve the main HTML page with the dynamic clock."""
    index_path = Path(__file__).resolve().parent.parent / "index.html"
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=80)
