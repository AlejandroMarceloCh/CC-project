from pydantic import BaseModel, EmailStr
class Item(BaseModel):
    username: str
    nombre: str
    sexo: str
    correo: EmailStr
    fecha_nacimiento: str
    direccion: str
