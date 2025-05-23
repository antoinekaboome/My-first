import uuid
from fastapi import APIRouter, Depends, HTTPException
from app import database, schemas, auth

router = APIRouter(prefix="/clients", tags=["clients"], dependencies=[Depends(auth.oauth2_scheme)])


def get_client(client_id: str):
    db = database.get_db()
    cur = db.execute(
        "SELECT id, name, tel, email, address FROM clients WHERE id=?",
        (client_id,),
    )
    return cur.fetchone()


@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    client_id = str(uuid.uuid4())
    db = database.get_db()
    db.execute(
        "INSERT INTO clients (id, name, tel, email, address) VALUES (?, ?, ?, ?, ?)",
        (client_id, client.name, client.tel, client.email, client.address),
    )
    db.commit()
    return schemas.Client(id=client_id, **client.dict())


@router.get("/", response_model=list[schemas.Client])
def list_clients(token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    db = database.get_db()
    cur = db.execute("SELECT id, name, tel, email, address FROM clients")
    rows = cur.fetchall()
    return [
        schemas.Client(id=row[0], name=row[1], tel=row[2], email=row[3], address=row[4])
        for row in rows
    ]


@router.get("/{client_id}", response_model=schemas.Client)
def get_client_route(client_id: str, token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    row = get_client(client_id)
    if not row:
        raise HTTPException(status_code=404, detail="Client not found")
    return schemas.Client(id=row[0], name=row[1], tel=row[2], email=row[3], address=row[4])


@router.put("/{client_id}", response_model=schemas.Client)
def update_client(client_id: str, client: schemas.ClientCreate, token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    db = database.get_db()
    if not get_client(client_id):
        raise HTTPException(status_code=404, detail="Client not found")
    db.execute(
        "UPDATE clients SET name=?, tel=?, email=?, address=? WHERE id=?",
        (client.name, client.tel, client.email, client.address, client_id),
    )
    db.commit()
    return schemas.Client(id=client_id, **client.dict())


@router.delete("/{client_id}")
def delete_client(client_id: str, token: str = Depends(auth.oauth2_scheme)):
    auth.get_current_user_token(token)
    db = database.get_db()
    if not get_client(client_id):
        raise HTTPException(status_code=404, detail="Client not found")
    db.execute("DELETE FROM clients WHERE id=?", (client_id,))
    db.commit()
    return {"detail": "Client deleted"}
