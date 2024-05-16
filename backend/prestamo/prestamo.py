from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas

app = FastAPI()

host_name = "database-2.cbekimjprojv.us-east-1.rds.amazonaws.com"
port_number = "3306"
user_name = "admin2"
password_db = "CC-utec_2024-s3"
database_name = "bd_api_prestamo"  

# Obtener todos los préstamos
@app.get("/prestamos")
def get_prestamos():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prestamos")
    result = cursor.fetchall()
    mydb.close()
    return {"prestamos": result}

# Obtener un préstamo por su ID
@app.get("/prestamo/{id}")
def get_prestamo(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM prestamos WHERE id = {id}")
    result = cursor.fetchone()
    mydb.close()
    if result:
        return {"prestamo": result}
    else:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

# Agregar un nuevo préstamo
@app.post("/prestamos")
def add_prestamo(item: schemas.Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    
    # Verificar si el usuario existe
    usuario_username = item.usuario_username
    user_response = requests.get(f"http://{host_name}:{port_number}/usuarios/{usuario_username}")
    if user_response.status_code != 200:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    libro_id = item.libro_id
    estado = item.estado
    cursor = mydb.cursor()
    sql = "INSERT INTO prestamos (usuario_username, libro_id, estado) VALUES (%s, %s, %s)"
    val = (usuario_username, libro_id, estado)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Préstamo agregado exitosamente"}

# Modificar un préstamo
@app.put("/prestamos/{id}")
def update_prestamo(id: int, item: schemas.Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
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
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM prestamos WHERE id = {id}")
    mydb.commit()
    mydb.close()
    return {"message": "Préstamo eliminado exitosamente"}
