from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# cria conexao banco
db = create_engine("sqlite:///database/banco.db")

# base do banco
Base = declarative_base()

# Para efetivamente gerar as tabelas no arquivo SQLite:
# Base.metadata.create_all(bind=db)
