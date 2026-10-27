from datetime import date, datetime
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from models.base import Base


class Pedido(Base):
  __tablename__ = "pedidos"

  # STATUS_PEDIDOS = (
  #     ("PENDENTE", "PENDENTE"),
  #     ("CANCELADO", "CANCELADO"),
  #     ("FINALIZADO", "FINALIZADO"),
  # )

  id = Column("id", Integer, primary_key=True, autoincrement=True)
  status = Column("status", String)
  usuario = Column("usuario", ForeignKey("usuarios.id"))
  preco = Column("preco", Float)
  data_pedido = Column("data_pedido", Date, default=date.today)
  hora_pedido = Column("hora_pedido", Time, default=lambda: datetime.now().time())
  itens = relationship("ItemPedido", cascade="all, delete" )

  def __init__(self,usuario,status="PENDENTE",preco=0,data_pedido=None,hora_pedido=None):
    self.usuario = usuario
    self.preco = preco
    self.status = status
    if data_pedido:
      self.data_pedido = data_pedido
    if hora_pedido:
      self.hora_pedido = hora_pedido
  def calcular_preco(self):
    # percorrer todos os itens do pedido, depois somar todos os precos de todos os itens 
    # editar no campo preco o valor final do preco do pedido
    self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)

class ItemPedido(Base):
  __tablename__ = "itens_pedido"

  id = Column("id", Integer, primary_key=True, autoincrement=True)
  quantidade = Column("quantidade", Integer)
  sabor = Column("sabor", String)
  tamanho = Column("tamanho", String)
  preco_unitario = Column("preco_unitario", Float)
  pedido = Column("pedido", ForeignKey("pedidos.id"))

  def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
    self.quantidade = quantidade
    self.sabor = sabor
    self.tamanho = tamanho
    self.preco_unitario = preco_unitario
    self.pedido = pedido
