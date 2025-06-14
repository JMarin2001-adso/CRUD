# auth_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.db_mysql import get_db_connection
import pymysql.cursors

auth_routes = APIRouter(prefix="/auth", tags=["auth"])

class RegistroRequest(BaseModel):
    Nombre: str
    Direccion: str
    Email: str
    Password: str

class LoginRequest(BaseModel):
    Email: str
    Password: str

@auth_routes.post("/registro")
def registrar_usuario(user: RegistroRequest):
    con = get_db_connection()
    try:
        con.ping(reconnect=True)
        with con.cursor() as cursor:
            # Verifica si el correo ya existe
            check_sql = "SELECT COUNT(*) FROM usuarios WHERE Email=%s"
            cursor.execute(check_sql, (user.Email,))
            result = cursor.fetchone()
            if result[0] > 0:
                raise HTTPException(status_code=400, detail="Correo ya registrado")
            
            # Inserta nuevo usuario
            insert_sql = """
                INSERT INTO usuarios (Nombre, Email, Password, Direccion, Estado)
                VALUES (%s, %s, %s, %s, '', 1)
            """
            cursor.execute(insert_sql, (user.Nombre, user.Email,user.Password, user.Direccion))
            con.commit()

            return {"mensaje": "Usuario registrado correctamente", "user_id": cursor.lastrowid}
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el registro: {str(e)}")

@auth_routes.post("/login")
def login(user: LoginRequest):
    con = get_db_connection()
    try:
        con.ping(reconnect=True)
        with con.cursor(pymysql.cursors.DictCursor) as cursor:
            login_sql = """
                SELECT id, Nombre FROM usuarios
                WHERE TRIM(LOWER(Email)) = TRIM(LOWER(%s)) AND Password = %s AND Estado = 1
            """
            # Normaliza el email antes de mandarlo
            email_normalizado = user.Email.strip().lower()
            cursor.execute(login_sql, (email_normalizado, user.Password))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=401, detail="Credenciales inválidas o usuario inactivo")

            return {
                "mensaje": "Login exitoso",
                "usuario": result["Nombre"],
                "usuario_id": result["id"]
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el login: {str(e)}")