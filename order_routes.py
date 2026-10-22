from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema
from models import Pedido, Usuario

order_router = APIRouter(prefix="/pedidos",tags=["pedidos"], dependencies=[Depends(verificar_token)])


@order_router.get("/")
async def getPedidos():
    return {"mensagem": "voce acessou a rota de pedidos!"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    """Rota de Criação do pedido, por enquanto recebe id do usuario e retorna uma mensagem de sucesso"""

    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    usuario = session.query(Usuario).filter(Usuario.id == pedido_schema.usuario).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario nao encontrado")

    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}


@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    """Cancela um pedido. Permitido apenas para admins ou para o dono do pedido."""

    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Voce nao tem autorizacao para fazer essa modificacao")

    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido numero: {id_pedido} cancelado com sucesso",
        "pedido": {"id": pedido.id, "status": pedido.status}
    }

