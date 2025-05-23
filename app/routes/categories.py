import uuid
from fastapi import APIRouter, Depends, HTTPException
from app import database, schemas, auth

router = APIRouter(prefix="/categories", tags=["categories"], dependencies=[Depends(auth.oauth2_scheme)])


def get_category(category_id: str):
    db = database.get_db()
    cur = db.execute("SELECT id, name FROM categories WHERE id=?", (category_id,))
    return cur.fetchone()


@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    category_id = str(uuid.uuid4())
    db = database.get_db()
    db.execute("INSERT INTO categories (id, name) VALUES (?, ?)", (category_id, category.name))
    db.commit()
    return schemas.Category(id=category_id, **category.dict())


@router.get("/", response_model=list[schemas.Category])
def list_categories(token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    db = database.get_db()
    cur = db.execute("SELECT id, name FROM categories")
    rows = cur.fetchall()
    return [schemas.Category(id=row[0], name=row[1]) for row in rows]


@router.get("/{category_id}", response_model=schemas.Category)
def get_category_route(category_id: str, token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    row = get_category(category_id)
    if not row:
        raise HTTPException(status_code=404, detail="Category not found")
    return schemas.Category(id=row[0], name=row[1])


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: str, category: schemas.CategoryCreate, token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    db = database.get_db()
    if not get_category(category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    db.execute("UPDATE categories SET name=? WHERE id=?", (category.name, category_id))
    db.commit()
    return schemas.Category(id=category_id, **category.dict())


@router.delete("/{category_id}")
def delete_category(category_id: str, token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    db = database.get_db()
    if not get_category(category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    db.execute("DELETE FROM categories WHERE id=?", (category_id,))
    db.commit()
    return {"detail": "Category deleted"}
