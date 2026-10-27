from sqlalchemy import Boolean, Column, Integer, String

from models.base import Base


class Usuario(Base):
  __tablename__ = "usuarios"

  id = Column("id", Integer, primary_key=True, autoincrement=True)
  nome = Column("nome", String)
  email = Column("email", String, nullable=False)
  senha = Column("senha", String)
  ativo = Column("ativo", Boolean)
  admin = Column("admin", Boolean, default=False)

  def __init__(self, nome, email, senha, ativo=True, admin=False):
    self.nome = nome
    self.email = email
    self.senha = senha
    self.ativo = ativo
    self.admin = admin
