from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, Usuario, ItemPedido

order_router = APIRouter(prefix="/pedidos",tags=["pedidos"], dependencies=[Depends(verificar_token)])


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

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin :
        raise HTTPException(status_code=403, detail="Voce nao tem autorizacao para fazer essa operacao")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos":pedidos
        }

@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int,
                                item_pedido_schema: ItemPedidoSchema, 
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="essse pedido nao existe")
    elif not usuario.admin and usuario.id != pedido.usuario:
            raise HTTPException(status_code=401, detail="Voce nao tem autorizacao para fazer essa operacao")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, 
                             item_pedido_schema.sabor, 
                             item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "item criado com SUCESSO",
        "item_id":  item_pedido.id,
        "preco_pedido": pedido.preco
    }
