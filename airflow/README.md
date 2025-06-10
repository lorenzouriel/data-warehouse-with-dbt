## `airflow/` — *Orquestração com Astronomer*

### O que faz:
* Contém os DAGs que orquestram a execução dos modelos DBT.
* Configurado para ser executado na plataforma **Astronomer** com **Airflow 3.0**.

### Como Rodar Localmente (com Astro CLI):
```bash
# 1. Instale o Astro CLI
curl -sSL https://install.astronomer.io | sudo bash

# 2. Vá até o diretório do projeto
cd airflow

# 3. Inicie o ambiente Airflow local
astro dev start

# 4. Acesse o Airflow UI:
# URL: http://localhost:8080
# Usuário: admin
# Senha: admin
```

### Como Rodar na Nuvem (Astronomer Cloud):
```bash
# 1. Faça login na Astronomer
astro login

# 2. Faça deploy
astro deploy
```