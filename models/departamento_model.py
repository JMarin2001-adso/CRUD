from typing import Union
from pydantic import BaseModel

from models.user_model import User


class departamento(BaseModel):
    cargo:str
    areaAsignada:str
    CodigoUsuario: Union[int,User]
    #CodigoDepartamento:













