# Aprendendo FASTAPI

Este projeto é um estudo sobre o framework FastAPI, utilizando autenticação JWT, SQLAlchemy e PostgreSQL.

## Pré-requisitos

- Python 3.8+
- PostgreSQL

## Instalação das dependências

Clone o repositório, criei um ambiente virtual e instale as dependências:

```bash
git clone https://github.com/GSStoffel/learning_fastapi.git
cd learning_fastapi
python -m venv venv
source .\venv\bin\activate
pip install -r requirements.txt
```

## Configuração de desenvolvimento

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
DATABASE_HOSTNAME=host_ip_banco
DATABASE_PORT=5432
DATABASE_USERNAME=seu_usuario
DATABASE_PASSWORD=sua_senha
DATABASE_NAME=fastapi
SECRET_KEY=sua_secret_key
ALGORITHM=algoritmo_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=1
```

Obs: Altere os valores conforme seu ambiente.

## Como executar

```bash
alembic upgrade head
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 127.0.0.1:8000
```

Acesse `http://localhost:8000` no navegador para ver a API em funcionamento.

## Autenticação

A autenticação é feita via OAuth2 com JWT. Para obter um token, faça um POST em `/login` com os campos `username` (
e-mail) e `password`.

Exemplo usando `curl`:

```bash
curl -X POST "http://localhost:8000/login" -d "username=seu_email&password=sua_senha"
```

## Endpoints principais

A documentação dos métodos pode ser encontrada em http://localhost:8000/docs

- `GET /users/{id}` — Busca usuário por ID
- `GET /posts` — Lista posts (requer autenticação)
- `GET /posts/my_posts` — Lista seus posts (requer autenticação)
- `GET /posts/{id}` — Busca post por ID (requer autenticação)
- `POST /users` — Cria um novo usuário
- `POST /login` — Autentica e retorna um token JWT
- `POST /posts` — Cria um post (requer autenticação)
- `POST /vote` — Adicionar/Remover voto de um post
- `PUT /posts/{id}` — Atualiza post (apenas dono)
- `DELETE /posts/{id}` — Remove post (apenas dono)

## Licença

Este projeto está sob a licença MIT.
