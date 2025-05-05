from fastapi.responses import JSONResponse
import pymysql
import pymysql.cursors
from db.db_mysql import get_db_connection
from models.departamento_model import departamento
from typing import Optional, List


class DepartamentoService:

    def __init__(self):
        self.con=get_db_connection()
        if self.con is None:
            raise Exception("no se pudo establecer conexion")

    async def get_departamento(self):
        """Inicializa la conexion"""
        try:
            self.con.ping(reconnect=True)#siempre hay que abrir por que es un proceso diferente
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql="""SELECT d.id, designacion, u.Nombre,u.Direccion, u.Email  
                       FROM departamento d 
                       JOIN usuarios u ON CodigoUsuario=u.id"""
                
                cursor.execute(sql)
                departamento= cursor.fetchall()

                return JSONResponse(content={
                    "success":True,
                    "data":departamento,
                    "message":"reguistros encontrados"},
                    status_code =200,
                )
          
        except Exception as e:
             return JSONResponse(content={
                    "success":False,
                    "message":f"problema al realizar la consulta:{str(e)}"},
                    status_code=500,
                )

    async def get_departamentoid (self, user_id: int):
        """Consulta el departamento de un usuario específico."""
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """SELECT designacion, u.Nombre, u.Direccion, u.Email 
                         FROM departamento id 
                         JOIN usuarios u ON CodigoUsuario = u.id 
                         WHERE u.id = %s"""
                cursor.execute(sql, (user_id,))
                departamento = cursor.fetchone()

            if  departamento:

                return JSONResponse(content={
                    "success":True,
                    "data":departamento,
                    "message":"reguistro encontrado"},
                    status_code=200,
                )
            else:
                  return JSONResponse(content={
                    "success":False,
                    "message":"no hay reguistros para mostrar"},
                    status_code=400,
                )
        except Exception as e:
             return JSONResponse(content={
                    "success":False,
                    "message":f"problema al realizar la consulta:{str(e)}"},
                    status_code=500,
                )
        
    async def create_departamento(self,departamento_data:departamento):
          try:
            self.con.ping(reconnect=True)#siempre hay que abrir por que es un proceso diferente
            with self.con.cursor() as cursor:
                 
             sql="INSERT INTO departamento(cargo,designacion,CodigoUsuario) VALUES(%s,%s,%s)" #comodin %s, es para llamar los datos escritos, es decir, nombre equivale a %s
             cursor.execute(sql,(departamento_data.cargo,departamento_data.designacion,departamento_data.CodigoUsuario))#todos los datos tienen que ir en orden como los hayamos colocado 
            
            self.con.commit()
                
            if cursor.lastrowid:
                      return JSONResponse(content={
                    "success":True,
                    "data":cursor.lastrowid,
                    "message":"registro creado exitosamento"},
                    status_code=200,
                )
            else:
                  return JSONResponse(content={
                    "success":False,
                    "message":"no se pudo crear registro"},
                    status_code=400,
                )

          except Exception as e:
                return JSONResponse(content={
                    "success":False,
                    "message":f"problema al insertar registro:{str(e)}"},
                    status_code=500,
                )
          
    def close_connection(self):
        """Cierra la conexión con la base de datos."""
        if self.con:
            self.con.close()

           





