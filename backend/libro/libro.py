from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas

app = FastAPI()

host_name = "database-2.cbekimjprojv.us-east-1.rds.amazonaws.com"
port_number = "3306"
user_name = "admin2"
password_db = "CC-utec_2024-s3"
database_name = "bd_api_libro"  

# Obtener todos los libros
@app.get("/libros")
def get_libros():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM libros")
    result = cursor.fetchall()
    mydb.close()
    return {"libros": result}

# Obtener un libro por su ID
@app.get("/libro/{id}")
def get_libro(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM libros WHERE id = {id}")
    result = cursor.fetchone()
    mydb.close()
    if result:
        return {"libro": result}
    else:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
# Buscar libros por título
@app.get("/libros/{titulo}")
def buscar_libros_por_titulo(titulo: str):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM libros WHERE titulo LIKE %s AND disponible = 1", ('%' + titulo + '%',))
    result = cursor.fetchall()
    mydb.close()
    return {"libros": result}

# Agregar un nuevo libro
@app.post("/libros")
def add_libro(item: schemas.Libro):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    titulo = item.titulo
    autor = item.autor
    descripcion = item.descripcion
    imagen=item.imagen
    # Agregar más campos según la estructura de tu tabla de libros en la base de datos
    cursor = mydb.cursor()
    sql = "INSERT INTO libros (titulo, autor, descripcion, imagen) VALUES (%s, %s, %s, %s)"
    val = (titulo, autor, descripcion, imagen)
    cursor.execute(sql, val)
    mydb.commit()
    libro_id = cursor.lastrowid  # Obtener el ID del libro recién insertado
    mydb.close()
    return {"message": "Libro agregado exitosamente"}

# Modificar un libro
@app.put("/libros/{id}")
def update_libro(id: int, item: schemas.Libro):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    titulo = item.titulo
    autor = item.autor
    descripcion = item.descripcion
    imagen=item.imagen
    # Modificar según la estructura de tu tabla de libros en la base de datos
    cursor = mydb.cursor()
    sql = "UPDATE libros SET titulo=%s, autor=%s, descripcion=%s, imagen=%s WHERE id=%s"
    val = (titulo, autor, descripcion, imagen, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Libro modificado exitosamente"}

# Eliminar un libro por su ID
@app.delete("/libros/{id}")
def delete_libro(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM libros WHERE id = {id}")
    mydb.commit()
    mydb.close()
    return {"message": "Libro eliminado exitosamente"}
