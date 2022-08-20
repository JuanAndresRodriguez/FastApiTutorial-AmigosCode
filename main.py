from fastapi import FastAPI, HTTPException
from typing import List
from models import User, Gender, Role, UserUpdateRequest
from uuid import UUID, uuid4

app = FastAPI()

# Should be replaced with SQL db, will be a List for the example
db: List[User] = [
    User(
        # id=uuid4(), this line generates new id when app is restarted
        id=UUID("ed700f14-6036-4c29-9a49-bb9f7c279ad7"), # passing the uuid generated code as a string to keep the same id
        first_name="Jamila",
        last_name="Ahmed",
        gender = Gender.female,
        roles=[Role.student]
    ),
    User(
        # id=uuid4(),
        id=UUID("7e07f8c7-c434-491a-9361-8c517ca9edc9"),
        first_name="Alex",
        last_name="Jones",
        gender=Gender.male,
        roles=[Role.admin, Role.user]
    )
]


@app.get("/")
async def root():
    return {"Hello": "Mundo"}

@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
    )