# Aprendendo FASTAPI

Este projeto é um estudo sobre o framework FastAPI, utilizando autenticação JWT, SQLAlchemy e PostgreSQL.

## Instalação das dependências

```bash
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

## Como executar

```bash
uvicorn main:app --reload
```

Acesse `http://localhost:8000` no navegador para ver a API em funcionamento.

## Autenticação

A autenticação é feita via OAuth2 com JWT. Para obter um token, faça um POST em `/login` com os campos `username` (e-mail) e `password`.

Exemplo usando `curl`:

```bash
curl -X POST "http://localhost:8000/login" -d "username=seu_email&password=sua_senha"
```

## Endpoints principais

- `POST /users` — Cria um novo usuário
- `GET /users/{id}` — Busca usuário por ID
- `POST /login` — Autentica e retorna um token JWT
- `GET /posts` — Lista posts (requer autenticação)
- `POST /posts` — Cria um post (requer autenticação)
- `GET /posts/my_posts` — Lista seus posts (requer autenticação)
- `GET /posts/{id}` — Busca post por ID (requer autenticação)
- `PUT /posts/{id}` — Atualiza post (apenas dono)
- `DELETE /posts/{id}` — Remove post (apenas dono)

## Licença

Este projeto está sob a licença MIT.
