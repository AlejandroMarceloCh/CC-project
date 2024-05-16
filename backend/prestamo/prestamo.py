from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas

app = FastAPI()

# Configuración para conectarse a las bases de datos RDS
db_config = {
    "host": "database-2.cbekimjprojv.us-east-1.rds.amazonaws.com",
    "port": 3306,
    "user": "admin2",
    "password": "CC-utec_2024-s3"
}

# Obtener todos los préstamos
@app.get("/prestamos")
def get_prestamos():
    mydb = mysql.connector.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database="bd_api_prestamo"
    )
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prestamos")
    result = cursor.fetchall()
    mydb.close()
    return {"prestamos": result}

# Obtener un préstamo por su ID
@app.get("/prestamo/{id}")
def get_prestamo(id: int):
    mydb = mysql.connector.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database="bd_api_prestamo"
    )
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prestamos WHERE id = %d", (id,))
    result = cursor.fetchone()
    mydb.close()
    if result:
        return {"prestamo": result}
    else:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

# Agregar un nuevo préstamo
@app.post("/prestamos")
def add_prestamo(item: schemas.Item):
    # Conectar a la base de datos de usuarios para verificar si el usuario existe
    user_db = mysql.connector.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database="bd_api_usuario"
    )
    
    usuario_username = item.usuario_username
    user_cursor = user_db.cursor(dictionary=True)
    user_cursor.execute("SELECT * FROM usuarios WHERE username = %s", (usuario_username,))
    user_result = user_cursor.fetchone()
    user_db.close()
    
    if not user_result:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    # Conectar a la base de datos de préstamos para agregar el nuevo préstamo
    prestamo_db = mysql.connector.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database="bd_api_prestamo"
    )

    libro_id = item.libro_id
    estado = item.estado
    cursor = prestamo_db.cursor()
    sql = "INSERT INTO prestamos (usuario_username, libro_id, estado) VALUES (%s, %s, %s)"
    val = (usuario_username, libro_id, estado)
    cursor.execute(sql, val)
    prestamo_db.commit()
    prestamo_db.close()
    
    return {"message": "Préstamo agregado exitosamente"}

# Modificar un préstamo
@app.put("/prestamos/{id}")
def update_prestamo(id: int, item: schemas.Item):
    mydb = mysql.connector.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database="bd_api_prestamo"
    )
    usuario_username = item.usuario_username
    libro_id = item.libro_id
    estado = item.estado
    # Modificar según la estructura de tu tabla de préstamos en la base de datos
    cursor = mydb.cursor()
    sql = "UPDATE prestamos SET usuario_username=%s, libro_id=%s, estado=%s WHERE id=%s"
    val = (usuario_username, libro_id, estado, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Préstamo modificado exitosamente"}

# Eliminar un préstamo por su ID
@app.delete("/prestamos/{id}")
def delete_prestamo(id: int):
    mydb = mysql.connector.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database="bd_api_prestamo"
    )
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM prestamos WHERE id = %s", (id,))
    mydb.commit()
    mydb.close()
    return {"message": "Préstamo eliminado exitosamente"}


