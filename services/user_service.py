from fastapi.responses import JSONResponse
import pymysql
import pymysql.cursors
from db.db_mysql import get_db_connection
from models.user_model import User


class UserService:
    def __init__(self):
        self.con=get_db_connection()
        if self.con is None:
            raise Exception("no se pudo establecer conexion")


    async def get_users(self):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:#siempre es importante el parentesis por que si no genera error de sintaxis y objetos en blanco
                cursor.execute("SELECT * FROM usuarios")
                users=cursor.fetchall()

                return JSONResponse(
                    status_code=200,
                    content={
                        "succes": True, "message":"usuarios obtenidps exitosamente", "data": users if users else[]
                        }
                )
        except Exception as e:
            print("error en get_users", str(e))#lo muestra en consula
            return JSONResponse(
                status_code=500,
                content={
                    "succes": False, "message": f"error al obtener los usuarios {str(e)}", "data":None
                }
            )

    async def get_user_by_id(self,user_id: int):
        """Consulta un usuario por id y devuelve uan respuesta"""
        try:
            self.con.ping(reconnect=True)#reconectar la conexion. terminos de seguridad 
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:# se crea cursor, con esta estructura para traer datos,diccionarios o informacion"(pymysl.cursor.DictCursor)".
              #siempre es importante el parentesis en cursor por que si no genera error de sintaxis y objetos en blanco
              sql="SELECT * FROM usuarios WHERE id= %s"
              cursor.execute(sql,(user_id))
              user=cursor.fetchone() #fetchone devuelve un solo resultado
            
              if user:
                  return JSONResponse(
                      status_code=200,
                      content={
                          "succes": True,
                          "message":"usuario encontrado",#sentencia exitosa
                          "data": user
                      }
                  )
              else:
                  return JSONResponse(
                      status_code=404,
                      content={
                          "succes": False,
                          "message":"usuario no encontrado", #error de usuario
                          "data": None
                      }
                      
                  )
        
        except Exception as e:
            return JSONResponse(
                      status_code=500,
                      content={
                          "succes": False,
                          "message":f"error al consultar el usuario:{str(e)}", #error del sistema
                          "data": None
                      }
                      
                  )
        finally:#cerrar conexion terminos de seguridad
            self.close_connection()
        
    async def create_user(self,user_data:User):
        try:
            self.con.ping(reconnect=True)#reconectar la conexion. terminos de seguridad 
            with self.con.cursor() as cursor:#a diferencia del otro cursor este es para mandar un regustro y no buscar 
               #siempre es importante el parentesis en cursor porque si no genera error de sintaxis y objetos en blanco
               check_sql="SELECT COUNT(*) FROM usuarios WHERE Email=%s" #se usa este tipo de consulta para saber que no hayan usuarios repetidos en diferentes usuarios
               cursor.execute(check_sql,(user_data.Email))
               result=cursor.fetchone()

               if result[0] > 0:
                   return JSONResponse(
                      status_code=200,
                      content={
                          "succes": True,
                          "message":"usuario no esta duplicado", #error de usuario
                          "data": None
                      }
                      
                  )
               
               sql="INSERT INTO usuarios(Nombre,Direccion,Email,Password,Estado) VALUES (%s,%s,%s,%s,%s)" #comodin %s, es para llamar los datos escritos, es decir, nombre equivale a %s
               cursor.execute(sql,(user_data.Nombre,user_data.Direccion,user_data.Email,user_data.Password,user_data.Estado))#todos los datos tienen que ir en orden como los hayamos colocado 
               self.con.commit()

               if cursor.lastrowid:#cuando tenemos una tabala con un dato autonumerico como id el se va rellenando solo, y inserta el numero usuario y devyelve la ultima fila que quedo con un nuevo id
                     return JSONResponse(
                      status_code=201,
                      content={
                          "succes": True,
                          "message":"usuario creado exitosamente",#sentencia exitosa
                          "data": {"user_id":cursor.lastrowid}#muestra el id con el que fue creado el usuario
                      }
                  )
               else:
                    return JSONResponse(
                      status_code=400,
                      content={
                          "succes": False,
                          "message":"usuario no pudo ser creado",#sentencia con error de usuario
                          "data": None
                      }
                  )



        except Exception as e:
            return JSONResponse(
                      status_code=500,
                      content={
                          "succes": False,
                          "message":f"error al crear el usuario:{str(e)}", #error del sistema
                          "data": None
                      }
                      
                  )
        finally:#cerrar conexion terminos de seguridad
            self.close_connection()
    
    async def change_password(self,user_id:int,new_Password:str): #otro metodo, pero es ,mejor trabajar con JSONRESPONSES
         """Actualizar la contraseña de un usuario y retonar JSONResponse"""
         try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:#verifica si existe el usuario
                Check_sql="SELECT COUNT(*) FROM usuarios WHERE id=%s"
                cursor.execute(Check_sql,(user_id))
                result=cursor.fetchone()


                if result[0] == 0:
                   return JSONResponse(
                      status_code=400,
                      content={
                          "succes": False,
                          "message":"usuario no existe", #error de usuario
                          "data": None
                      }
                      
                  )
                
           
                sql="UPDATE usuarios SET Password=%s WHERE id=%s"
                cursor.execute(sql,(new_Password,user_id))
                self.con.commit()

                if cursor.rowcount > 0: #rowcount nos ayuda a generar la cantidad de filas qu ese vieron afectadas, en este caso solo se va afectar una fila.

                    return JSONResponse(content={"success": True, "message": "Contraseña actualizada exitosamente."}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "No se realizaron cambios."}, status_code=409)
        
         except Exception as e:
             self.con.rollback()
             return JSONResponse(content={"success": False, "message": f"Error al actualizar la contraseña: {str(e)}"}, status_code=500)
         finally:#cerrar conexion terminos de seguridad
            self.close_connection() 

    async def inactivate_user(self, user_id: int):
        """Inactiva un usuario cambiando su estado a 0 y retorna JSONResponse."""
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                # Verificar si el usuario existe
                check_sql = "SELECT COUNT(*) FROM usuarios WHERE id=%s"
                cursor.execute(check_sql, (user_id,))
                result = cursor.fetchone()
                
                if result[0] == 0:  # Si el usuario no existe
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                # Inactivar usuario
                sql = "UPDATE usuarios SET estado=0 WHERE id=%s"
                cursor.execute(sql, (user_id,))
                self.con.commit()  # Confirmar la transacción

                if cursor.rowcount > 0:
                    return JSONResponse(content={"success": True, "message": "Usuario inactivado exitosamente."}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "No se realizaron cambios."}, status_code=400)
        except Exception as e:
            self.con.rollback()  # Deshacer la transacción
            return JSONResponse(content={"success": False, "message": f"Error al inactivar usuario: {str(e)}"}, status_code=500)
        finally:
            self.close_connection()
            
            
    async def toggle_user_status(self, user_id: int):#toggle_user_status
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                # Obtener estado actual
                get_estado_sql = "SELECT estado FROM usuarios WHERE id=%s"
                cursor.execute(get_estado_sql, (user_id,))
                result = cursor.fetchone()

                if not result:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                EstadoActual = result[0]
                nuevo_Estado = 0 if EstadoActual == 1 else 1

                update_sql = "UPDATE usuarios SET Estado=%s WHERE id=%s"
                cursor.execute(update_sql, (nuevo_Estado, user_id))
                self.con.commit()

                return JSONResponse(content={"success": True, "message": "Estado actualizado correctamente."}, status_code=200)
        except Exception as e:
            self.con.rollback()
            return JSONResponse(content={"success": False, "message": f"Error al cambiar estado: {str(e)}"}, status_code=500)
        finally:
            self.close_connection()
    
    async def update_user(self, user_id: int, user_data: User):
        """
        Actualiza los datos de un usuario excepto el campo 'estado'.
        """
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                # Verificar si el usuario existe
                check_sql = "SELECT COUNT(*) FROM usuarios WHERE id=%s"
                cursor.execute(check_sql, (user_id,))
                result = cursor.fetchone()

                if result[0] == 0:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                # Actualizar campos (excepto estado)
                update_sql = """
                    UPDATE usuarios
                    SET Nombre=%s, Direccion=%s, Email=%s, Password=%s
                    WHERE id=%s
                """
                cursor.execute(update_sql, (
                    user_data.Nombre,
                    user_data.Direccion,
                    user_data.Email,
                    user_data.Password,
                    user_id
                ))
                self.con.commit()

                if cursor.rowcount > 0:
                    return JSONResponse(content={"success": True, "message": "Usuario actualizado correctamente."}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "No se realizaron cambios."}, status_code=409)

        except Exception as e:
            self.con.rollback()
            return JSONResponse(content={"success": False, "message": f"Error al actualizar usuario: {str(e)}"}, status_code=500)
        finally:
            self.close_connection()
    
    def close_connection(self):
        """llama el cierre de la conexion de la base de datos"""
        if self.con:
            self.con.close()

    

                
            
            





