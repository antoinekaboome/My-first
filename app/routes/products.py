import uuid
from fastapi import APIRouter, Depends, HTTPException
from app import database, schemas, auth

router = APIRouter(prefix="/products", tags=["products"], dependencies=[Depends(auth.oauth2_scheme)])


def get_db_product(product_id: str):
    db = database.get_db()
    cur = db.execute(
        "SELECT id, name, description, price, in_stock, category_id FROM products WHERE id=?",
        (product_id,),
    )
    return cur.fetchone()


@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    product_id = str(uuid.uuid4())
    db = database.get_db()
    # ensure category exists
    cur = db.execute("SELECT id FROM categories WHERE id=?", (product.category_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Category not found")
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
def list_products(token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    db = database.get_db()
    cur = db.execute("SELECT id, name, description, price, in_stock, category_id FROM products")
    rows = cur.fetchall()
    return [
        schemas.Product(
            id=row[0],
            name=row[1],
            description=row[2],
            price=row[3],
            in_stock=bool(row[4]),
            category_id=row[5],
        )
        for row in rows
    ]


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: str, token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    row = get_db_product(product_id)
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.Product(
        id=row[0],
        name=row[1],
        description=row[2],
        price=row[3],
        in_stock=bool(row[4]),
        category_id=row[5],
    )


@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: str, product: schemas.ProductCreate, token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    db = database.get_db()
    if not get_db_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    if not db.execute("SELECT id FROM categories WHERE id=?", (product.category_id,)).fetchone():
        raise HTTPException(status_code=404, detail="Category not found")
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
def delete_product(product_id: str, token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    db = database.get_db()
    if not get_db_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    db.execute("DELETE FROM products WHERE id=?", (product_id,))
    db.commit()
    return {"detail": "Product deleted"}
