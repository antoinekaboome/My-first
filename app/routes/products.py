import uuid
from fastapi import APIRouter, Depends, HTTPException
from app import database, schemas, auth

router = APIRouter(prefix="/products", tags=["products"], dependencies=[Depends(auth.get_current_user_token)])


def get_product_row(product_id: str):
    db = database.get_db()
    cur = db.execute(
        "SELECT id, name, description, price, in_stock, category_id FROM products WHERE id=?",
        (product_id,),
    )
    return cur.fetchone()


def category_exists(category_id: str) -> bool:
    db = database.get_db()
    cur = db.execute("SELECT 1 FROM categories WHERE id=?", (category_id,))
    return cur.fetchone() is not None


@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate):
    if not category_exists(product.category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    db = database.get_db()
    product_id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO products (id, name, description, price, in_stock, category_id) VALUES (?, ?, ?, ?, ?, ?)",
        (
            product_id,
            product.name,
            product.description,
            product.price,
            int(product.in_stock),
            product.category_id,
        ),
    )
    db.commit()
    return schemas.Product(id=product_id, **product.dict())


@router.get("/", response_model=list[schemas.Product])
def list_products():
    db = database.get_db()
    cur = db.execute("SELECT id, name, description, price, in_stock, category_id FROM products")
    rows = cur.fetchall()
    return [
        schemas.Product(id=r[0], name=r[1], description=r[2], price=r[3], in_stock=bool(r[4]), category_id=r[5])
        for r in rows
    ]


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: str):
    row = get_product_row(product_id)
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.Product(id=row[0], name=row[1], description=row[2], price=row[3], in_stock=bool(row[4]), category_id=row[5])


@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: str, product: schemas.ProductCreate):
    if not get_product_row(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    if not category_exists(product.category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    db = database.get_db()
    db.execute(
        "UPDATE products SET name=?, description=?, price=?, in_stock=?, category_id=? WHERE id=?",
        (
            product.name,
            product.description,
            product.price,
            int(product.in_stock),
            product.category_id,
            product_id,
        ),
    )
    db.commit()
    return schemas.Product(id=product_id, **product.dict())


@router.delete("/{product_id}")
def delete_product(product_id: str):
    db = database.get_db()
    if not get_product_row(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    db.execute("DELETE FROM products WHERE id=?", (product_id,))
    db.commit()
    return {"detail": "Product deleted"}
