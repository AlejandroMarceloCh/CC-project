from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas

app = FastAPI()

host_name = "database-2.cbekimjprojv.us-east-1.rds.amazonaws.com"
port_number = "3306"
user_name = "admin2"
password_db = "CC-utec_2024-s3"
database_name = "bd_api_usuario"  

# Obtener todos los usuarios
@app.get("/usuarios")
def get_usuarios():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    result = cursor.fetchall()
    mydb.close()
    return {"usuarios": result}

# Obtener un usuario por su ID
@app.get("/usuarios/{username}")
def get_usuario(username: str):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
    result = cursor.fetchone()
    mydb.close()
    if result:
        return {"usuario": result}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Agregar un nuevo usuario
@app.post("/usuarios")
def add_usuario(item: schemas.Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    username = item.username
    nombre = item.nombre
    sexo = item.sexo
    correo = item.correo
    fecha_nacimiento = item.fecha_nacimiento
    direccion = item.direccion
    # Agregar más campos según la estructura de tu tabla de usuarios en la base de datos
    cursor = mydb.cursor()
    sql = "INSERT INTO usuarios (username, nombre, sexo, correo, fecha_nacimiento, direccion) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (username, nombre, sexo, correo, fecha_nacimiento, direccion)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Usuario agregado exitosamente"}

# Modificar un usuario
@app.put("/usuarios/{username}")
def update_usuario(username: str, item: schemas.Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    nombre = item.nombre
    sexo = item.sexo
    correo = item.correo
    fecha_nacimiento = item.fecha_nacimiento
    direccion = item.direccion
    # Modificar según la estructura de tu tabla de usuarios en la base de datos
    cursor = mydb.cursor()
    sql = "UPDATE usuarios SET username=%s, nombre=%s, sexo=%s, correo=%s, fecha_nacimiento=%s, direccion=%s WHERE username=%s"
    val = (username, nombre, sexo, correo, fecha_nacimiento, direccion, username)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Usuario modificado exitosamente"}


# Eliminar un usuario por su ID
@app.delete("/usuarios/{username}")
def delete_usuario(username: str):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM usuarios WHERE username = %s", (username,))
    mydb.commit()
    mydb.close()
    return {"message": "Usuario eliminado exitosamente"}

