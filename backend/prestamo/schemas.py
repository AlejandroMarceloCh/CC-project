from pydantic import BaseModel
class Item(BaseModel):
    usuario_username: str
    libro_id: int
    estado: str