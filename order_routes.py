from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido, Usuario

order_router = APIRouter(prefix="/pedidos",tags=["pedidos"])

@order_router.get("/")
async def getPedidos():
    return {"mensagem": "voce acessou a rota de pedidos!"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    """Rota de Criação do pedido, por enquanto recebe id do usuario e retorna uma mensagem de sucesso."""

    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    usuario = session.query(Usuario).filter(Usuario.id == pedido_schema.usuario).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario nao encontrado")

    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}





