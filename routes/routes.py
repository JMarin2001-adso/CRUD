from fastapi import APIRouter
from models.departamento_model import departamento
from services.departamento_service import DepartamentoService
from services.user_service import UserService
from models.user_model import User

routes = APIRouter(prefix="/user", tags=["users"])
routes_d = APIRouter(prefix="/departamento", tags=["departamento"])

user_service = UserService()
departamento_service = DepartamentoService()

user_model = User
departamento_model = departamento

@routes.get("/get-users/")
async def get_all_users():
    result = await user_service.get_users()
    return result

@routes.get("/users/{user_id}")
async def get_user(user_id: int):
    return await user_service.get_user_by_id(user_id)

@routes.get("/dashboard-user/{user_id}")
async def dashboard_user_info(user_id: int):
    # Conecta al departamento_service para obtener nombre y cargo
    result = await departamento_service.get_by_departamentoid(user_id)
    if result.status_code != 200 or not result.body:
        return {"success": False, "message": "Usuario o departamento no encontrado"}
    return result


@routes.post("/nombre-metodo/")
async def nombre_metodo():
    return "Nombre método"

@routes.post("/create-user/")
async def create_user(user_data: User):
    return await user_service.create_user(user_data)

@routes.patch("/change-password/")
async def change_password(user_id: int, new_Password):
    return await user_service.change_password(user_id, new_Password)

@routes.patch("/inactivate/{user_id}")
async def inactivate_user(user_id: int):
    return await user_service.inactivate_user(user_id)

@routes.patch("/change-status/{user_id}")
async def change_user_status(user_id: int):
    return await user_service.toggle_user_status(user_id)

@routes.put("/update-user/{user_id}")
async def update_user(user_id: int, user_data: User):
    return await user_service.update_user(user_id, user_data)

@routes_d.get("/get-departamento/")
async def get_all_departamento():
    result = await departamento_service.get_departamento()
    return result

@routes_d.get("/get-departamentoid/{id_departamentoid}")
async def get_departamentoid(id_departamentoid: int):
    return await departamento_service.get_by_departamentoid(id_departamentoid)

@routes_d.post("/create-departamento/")
async def create_departamento(departamento: departamento):
    return await departamento_service.create_departamento(departamento)



