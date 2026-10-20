# API de Pedidos

API REST desenvolvida com **FastAPI** para cadastro de usuários e gerenciamento de pedidos. Os dados são persistidos em SQLite, o esquema do banco é versionado com **Alembic** e as senhas são protegidas com hash **bcrypt**.

## Sumário

- [Funcionalidades](#funcionalidades)
- [Tecnologias e bibliotecas](#tecnologias-e-bibliotecas)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Modelo de dados](#modelo-de-dados)
- [Endpoints](#endpoints)
- [Instalação e execução](#instalação-e-execução)
- [Migrações com Alembic](#migrações-com-alembic)
- [Licença](#licença)

## Funcionalidades

- Cadastro de usuários, com verificação de e-mail já existente
- Armazenamento de senhas em hash bcrypt, nunca em texto puro
- Configuração do ambiente por arquivo `.env`
- Versionamento do esquema do banco com migrações Alembic
- Documentação interativa gerada automaticamente (Swagger UI e ReDoc)
- Rotas de pedidos já registradas, com lógica de negócio ainda não implementada

## Tecnologias e bibliotecas

| Biblioteca | Função no projeto | Onde é usada |
|---|---|---|
| **FastAPI** | Framework web: definição de rotas, injeção de dependências e documentação automática | `main.py`, `auth_routes.py`, `order_routes.py`, `dependencies.py` |
| **Uvicorn** | Servidor ASGI que executa a aplicação | Comando de execução (`uvicorn main:app`) |
| **Pydantic** | Validação e tipagem dos dados recebidos nas requisições | `schemas.py` |
| **SQLAlchemy** | ORM: modelos das tabelas, engine e sessões de banco | `models.py`, `dependencies.py` |
| **SQLAlchemy-Utils** | Tipos adicionais para o SQLAlchemy (`ChoiceType`) | `models.py` (importado, ainda não utilizado) |
| **Alembic** | Migrações de esquema do banco de dados | `alembic/`, `alembic.ini` |
| **Passlib** | Contexto de criptografia de senhas (`CryptContext`) | `main.py` |
| **Bcrypt** | Algoritmo de hash utilizado pelo Passlib | Através de `main.py` |
| **python-dotenv** | Carrega as variáveis definidas no arquivo `.env` | `main.py` |
| **sqlite3** (biblioteca padrão) | Driver do banco SQLite, usado pelo SQLAlchemy | `models.py` |

## Estrutura do projeto

```
FastAPI/
├── main.py               # Ponto de entrada: cria a aplicação e registra os routers
├── auth_routes.py        # Rotas de autenticação (prefixo /auth)
├── order_routes.py       # Rotas de pedidos (prefixo /order)
├── models.py             # Engine do banco e modelos ORM (Usuario, Pedido, ItemPedido)
├── schemas.py            # Schemas Pydantic para validação das requisições
├── dependencies.py       # Dependências do FastAPI (pegar_sessao)
├── alembic.ini           # Configuração do Alembic
├── alembic/
│   ├── env.py            # Ambiente de execução das migrações
│   ├── script.py.mako    # Template usado para gerar novas migrações
│   ├── README            # Notas padrão do Alembic
│   └── versions/
│       └── 10edf7148fca_initial_migration.py   # Migração inicial: cria as tabelas
├── database/
│   └── banco.db          # Banco de dados SQLite
├── requirements.txt      # Dependências do projeto
├── .env                  # Variáveis de ambiente (não versionar)
├── .vscode/
│   └── settings.json     # Configurações do editor
├── .venv/                # Ambiente virtual local (não versionar)
├── LICENSE               # Licença MIT
└── README.md
```

A arquitetura separa responsabilidades em módulos:

- **Rotas**: cada domínio tem seu próprio `APIRouter` (`auth_routes.py`, `order_routes.py`), registrado em `main.py`.
- **Modelos**: `models.py` concentra a conexão com o banco e as classes ORM.
- **Validação**: `schemas.py` define o formato esperado do corpo das requisições.
- **Dependências**: `dependencies.py` fornece a sessão do banco para as rotas, que é fechada ao final de cada requisição.

## Modelo de dados

```
usuarios 1 ──── N pedidos 1 ──── N itens_pedido
```

**usuarios**

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | Integer | Chave primária |
| `nome` | String | Nome do usuário |
| `email` | String | E-mail do usuário (obrigatório) |
| `senha` | String | Hash bcrypt da senha |
| `ativo` | Boolean | Indica se a conta está ativa |
| `admin` | Boolean | Indica privilégios de administrador (padrão: `false`) |

**pedidos**

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | Integer | Chave primária |
| `status` | String | Situação do pedido (padrão: `PENDENTE`) |
| `usuario` | Integer | Chave estrangeira para `usuarios.id` |
| `preco` | Float | Preço do pedido |
| `data_pedido` | Date | Data do pedido (padrão: data atual) |
| `hora_pedido` | Time | Hora do pedido (padrão: hora atual) |

**itens_pedido**

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | Integer | Chave primária |
| `quantidade` | Integer | Quantidade do item |
| `sabor` | String | Sabor do item |
| `tamanho` | String | Tamanho do item |
| `preco_unitario` | Float | Preço unitário |
| `pedido` | Integer | Chave estrangeira para `pedidos.id` |

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/auth/` | Rota padrão do módulo de autenticação |
| `POST` | `/auth/criar_conta` | Cadastra um novo usuário |
| `GET` | `/order/pedidos` | Rota de pedidos (retorna mensagem de teste; a lógica ainda não foi implementada) |

### Exemplo: criar conta

`POST /auth/criar_conta`

Corpo da requisição (JSON). Os campos `ativo` e `admin` são obrigatórios e podem receber `null`:

```json
{
  "nome": "Maria",
  "email": "maria@exemplo.com",
  "senha": "senha123",
  "ativo": true,
  "admin": false
}
```

Resposta de sucesso:

```json
{
  "mensagem": "Usuario cadastrado com sucesso! maria@exemplo.com"
}
```

Resposta quando o e-mail já está cadastrado (HTTP 400):

```json
{
  "detail": "E-mail ja esta cadastrado no sistema"
}
```

Para testar os endpoints de forma visual, acesse a documentação interativa em `http://127.0.0.1:8000/docs`.

## Instalação e execução

### Pré-requisitos

- Python 3.10 ou superior (o projeto foi desenvolvido com Python 3.14)
- pip

### 1. Crie e ative um ambiente virtual

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt alembic sqlalchemy-utils
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta
```

Para gerar uma chave segura:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

> O arquivo `.env` contém segredos e não deve ser versionado nem publicado.

### 4. Prepare o banco de dados

O arquivo `database/banco.db` já acompanha o projeto com o esquema aplicado. Para criar um banco do zero, remova o arquivo `database/banco.db` e execute:

```bash
alembic upgrade head
```

### 5. Inicie o servidor

Execute sempre a partir da raiz do projeto, pois o caminho do banco SQLite é relativo:

```bash
uvicorn main:app --reload
```

Após a inicialização, os seguintes endereços ficam disponíveis:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Migrações com Alembic

Sempre que os modelos em `models.py` forem alterados, gere e aplique uma nova migração:

```bash
alembic revision --autogenerate -m "descricao da mudanca"   # gera uma migração a partir dos modelos
alembic upgrade head                                        # aplica todas as migrações pendentes
alembic downgrade -1                                        # desfaz a última migração
alembic current                                             # exibe a revisão atual do banco
```

## Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
