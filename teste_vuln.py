import subprocess

from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()
engine = create_engine("sqlite:///teste.db")


@app.get("/buscar")
def buscar(nome: str):
    # Seguro: usa parâmetro bindado para evitar SQL injection
    with engine.connect() as conn:
        resultado = conn.execute(
            text("SELECT * FROM usuarios WHERE nome = :nome"),
            {"nome": nome},
        )
        return [dict(r._mapping) for r in resultado]


@app.get("/ping")
def ping(host: str):
    # VULNERAVEL: command injection (shell=True com entrada do usuario)
    return subprocess.check_output(f"ping -c 1 {host}", shell=True)