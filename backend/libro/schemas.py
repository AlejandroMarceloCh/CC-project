from pydantic import BaseModel
class Libro(BaseModel):
    titulo: str
    autor: str
    descripcion: str
    imagen: str  
    
