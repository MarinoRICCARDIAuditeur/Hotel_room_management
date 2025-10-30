from pydantic import BaseModel

class ClientBase(BaseModel):
    nom: str
    email: str
    tel: str

class ClientCreate(ClientBase):
    pass

class ClientRead(ClientBase):
    id: int
    class Config:
        orm_mode = True

