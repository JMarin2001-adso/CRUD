from typing import Optional
from pydantic import BaseModel



class User(BaseModel):
    Nombre:str
    Direccion:str
    Email:str
    Password:str
    Estado:Optional[int] = 1  


