import uuid
import hashlib
from fastapi import APIRouter, Depends, HTTPException, status
from app import database, schemas, auth

router = APIRouter(prefix="/users", tags=["users"])

def get_user_by_username(username: str):
    db = database.get_db()
    cur = db.execute("SELECT id, username, password FROM users WHERE username=?", (username,))
    return cur.fetchone()

@router.post("/register", response_model=schemas.Token)
def register(user: schemas.UserCreate):
    db = database.get_db()
    if get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    user_id = str(uuid.uuid4())
    password_hash = hashlib.sha256(user.password.encode()).hexdigest()
    db.execute("INSERT INTO users (id, username, password) VALUES (?, ?, ?)", (user_id, user.username, password_hash))
    db.commit()
    token = auth.create_access_token({"sub": user.username})
    return schemas.Token(access_token=token)

@router.post("/token", response_model=schemas.Token)
def login(credentials: schemas.UserCreate):
    row = get_user_by_username(credentials.username)
    if not row:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    password_hash = hashlib.sha256(credentials.password.encode()).hexdigest()
    if password_hash != row[2]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = auth.create_access_token({"sub": credentials.username})
    return schemas.Token(access_token=token)


def get_current_user(token: str = Depends(auth.oauth2_scheme)):
    try:
        payload = auth.jwt_decode(token)
        username = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")
    row = get_user_by_username(username)
    if row is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return row
