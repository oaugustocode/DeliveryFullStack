from pydantic import BaseModel
from typing import Optional, List

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]
    class Config:
        from_atributtes = True

class PedidoSchema(BaseModel):
    usuario: int 

    class Config:
        from_atributtes = True

class LoginSchema(BaseModel):
    email: str
    senha: str 

    class Config:
        from_atributtes = True 

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    class Config:
        from_atributtes = True

class ResponsePedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoSchema]

    class Config:
        from_atributtes = True