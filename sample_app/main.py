from fastapi import FastAPI
from typing import List         #importing list from typing module, used to represent a list of elements
from uuid import uuid4          #generates universally unique identifiers(uuids)
from models import Gender, Role, User, UpdateUser   #importing classes from models.py
from uuid import UUID 
from fastapi import HTTPException


app = FastAPI()
db: List[User] = [
    User(
        id = uuid4(),       #generate a unique id
        first_name="Jack",
        last_name="Doe",
        gender=Gender.male,
        roles=[Role.user],
    ),
    User(
        id=uuid4(),
        first_name="Jeel",
        last_name="Doe",
        gender=Gender.female,
        roles=[Role.user],
    ),
        User(
        id=uuid4(),
        first_name="James",
        last_name="Gabriel",
        gender=Gender.male,
        roles=[Role.user],
    ),
        User(                             #admin dono role use karega
        id=uuid4(),
        first_name="ITS",
        last_name="ADMIN",
        gender=Gender.male,
        roles=[Role.admin, Role.user],
    ),       
]

@app.get("/")
async def root():
    return{"Helo":"World",}

@app.get("/api/v1/users")
async def get_users():
    return db

@app.post("/api/v1/users")
async def create_user(user: User):
    db.append(user)
    return{"id": user}

@app.delete("/api/v1/user/{id}")
async def delete_user(id: UUID):
    for user in db:
        if user.id == id:
            db.remove(user)
            return
        raise HTTPException(
            status_code=404, detail=f"Delete user failed, id {id} not found."
        )
        
@app.put("/api/v1/users{id}")
async def update_user(user_update: UpdateUser, id: UUID):
    for user in db:
        if user.id == id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
                return user.id
            raise HTTPException(status_code=404, detail =  "Could not find user with id:{id}")