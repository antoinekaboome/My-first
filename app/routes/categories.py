import uuid
from fastapi import APIRouter, Depends, HTTPException
from app import database, schemas, auth

router = APIRouter(prefix="/categories", tags=["categories"], dependencies=[Depends(auth.get_current_user_token)])


def get_category_row(category_id: str):
    db = database.get_db()
    cur = db.execute("SELECT id, name FROM categories WHERE id=?", (category_id,))
    return cur.fetchone()


@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate):
    db = database.get_db()
    category_id = str(uuid.uuid4())
    db.execute("INSERT INTO categories (id, name) VALUES (?, ?)", (category_id, category.name))
    db.commit()
    return schemas.Category(id=category_id, name=category.name)


@router.get("/", response_model=list[schemas.Category])
def list_categories():
    db = database.get_db()
    cur = db.execute("SELECT id, name FROM categories")
    rows = cur.fetchall()
    return [schemas.Category(id=r[0], name=r[1]) for r in rows]


@router.get("/{category_id}", response_model=schemas.Category)
def get_category(category_id: str):
    row = get_category_row(category_id)
    if not row:
        raise HTTPException(status_code=404, detail="Category not found")
    return schemas.Category(id=row[0], name=row[1])


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: str, category: schemas.CategoryCreate):
    db = database.get_db()
    if not get_category_row(category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    db.execute("UPDATE categories SET name=? WHERE id=?", (category.name, category_id))
    db.commit()
    return schemas.Category(id=category_id, name=category.name)


@router.delete("/{category_id}")
def delete_category(category_id: str):
    db = database.get_db()
    if not get_category_row(category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    db.execute("DELETE FROM categories WHERE id=?", (category_id,))
    db.commit()
    return {"detail": "Category deleted"}
