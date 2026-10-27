import subprocess

from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()
engine = create_engine("sqlite:///teste.db")


@app.get("/buscar")
def buscar(nome: str):
    # VULNERAVEL: SQL injection (entrada do usuario dentro da query)
    with engine.connect() as conn:
        resultado = conn.execute(text(f"SELECT * FROM usuarios WHERE nome = '{nome}'"))
        return [dict(r._mapping) for r in resultado]


@app.get("/ping")
def ping(host: str):
    # VULNERAVEL: command injection (shell=True com entrada do usuario)
    return subprocess.check_output(f"ping -c 1 {host}", shell=True)