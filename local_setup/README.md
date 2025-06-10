## `local_setup/` — *Ambiente de Teste Local*

### O que faz:
* Sobe um container com **PostgreSQL local**.
* Popula o `/data_warehouse/seeds` com dados fake

### Como Rodar:
```bash
# 1. Acesse o diretório
cd local_setup

# 2. Inicie o container
docker-compose up -d

# 3. Verifique se o banco está funcionando
docker ps

# 4. Acesse o banco com um cliente SQL (ex: DBeaver ou psql)
# Host: localhost
# Port: 5433
# User: ${DBT_USER}
# Password: ${DBT_PASSWORD}
```

### Gerar Dados Fake:
```bash
uv run .\local_setup\generate_fake_data.py
```

