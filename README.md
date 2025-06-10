# Data Warehouse com Airflow + DBT + PostgreSQL
Este projeto implementa uma arquitetura de Data Warehouse utilizando Airflow (via Astronomer), DBT e PostgreSQL. Ele é voltado para automação de pipelines de dados, com CI/CD integrado para facilitar o deploy e testes em ambientes locais e na nuvem (Railway).

## Estrutura do Projeto
```bash
.
├── .github/workflows/     # Pipelines de CI/CD com GitHub Actions
├── airflow/               # DAGs e configuração do Airflow com Astro CLI e Astronomer
├── data_warehouse/        # Projeto DBT com modelo em camadas (staging, intermediate, mart)
└── local_setup/           # PostgreSQL local + geração de dados fake
```

## Tecnologias Utilizadas
- **Airflow 3.0 (Astro Runtime)**: Orquestração de pipelines de dados
- **DBT**: Transformações SQL em múltiplas camadas (staging, intermediate, mart)
- **PostgreSQL**: Armazenamento de dados (local e Railway)
- **Docker + Docker Compose**: Ambiente de desenvolvimento local
- **GitHub Actions**: CI/CD para deploy e execução de pipelines
- **Faker + Scripts Python**: Geração de dados fake para testes

## Como Funciona
1. **Local Setup**:
   - Sobe um container com PostgreSQL local
   - Popula o banco com dados fictícios
   - Ideal para testes e desenvolvimento

2. **Data Warehouse (DBT)**:
   - Carrega e transforma dados usando o modelo em camadas:
     - `staging`: limpeza e padronização
     - `intermediate`: junções e transformações intermediárias
     - `mart`: modelagem final para consumo

3. **Airflow (Astronomer)**:
   - DAGs orquestram a execução dos modelos DBT
   - Planejado para rodar no Astronomer (Airflow 3.0)

4. **CI/CD (.github/workflows)**:
   - Deploy automático do DBT para o banco PostgreSQL na Railway
   - Executa DAGs no Astronomer via GitHub Actions

## Diretórios em Detalhe
| Diretório           | Descrição                                                            |
| ------------------- | -------------------------------------------------------------------- |
| `.github/workflows` | Pipelines de CI/CD com deploy na Railway e execução de DAGs no Astro |
| `airflow`           | DAGs do Airflow 3.0 e configuração do projeto Astronomer             |
| `data_warehouse`    | Projeto DBT com estrutura de camadas (staging, intermediate, mart)   |
| `local_setup`       | Setup local com Docker Compose e gerador de dados fake               |

---

# Data Warehouse with Airflow + DBT + PostgreSQL
This project implements a Data Warehouse architecture using Airflow (via Astronomer), DBT and PostgreSQL. It is focused on automating data pipelines, with integrated CI/CD to facilitate deployment and testing in local and cloud environments (Railway).

## Project Structure
```bash
.
├── .github/workflows/ # CI/CD pipelines with GitHub Actions
├── airflow/ # DAGs and Airflow configuration with Astro CLI and Astronomer
├── data_warehouse/ # DBT project with layered model (staging, intermediate, mart)
└── local_setup/ # Local PostgreSQL + fake data generation
```

## Technologies Used
- **Airflow 3.0 (Astro Runtime)**: Data pipeline orchestration
- **DBT**: SQL transformations in multiple layers (staging, intermediate, mart)
- **PostgreSQL**: Data storage (local and Railway)
- **Docker + Docker Compose**: Local development environment
- **GitHub Actions**: CI/CD for deploying and executing pipelines
- **Faker + Python Scripts**: Fake data generation for testing

## How it works
1. **Local Setup**:
- Creates a container with local PostgreSQL
- Populates the database with dummy data
- Ideal for testing and development

2. **Data Warehouse (DBT)**:
- Loads and transforms data using the layered model:
- `staging`: cleaning and standardization
- `intermediate`: intermediate joins and transformations
- `mart`: final modeling for consumption

3. **Airflow (Astronomer)**:
- DAGs orchestrate the execution of DBT models
- Planned to run on Astronomer (Airflow 3.0)

4. **CI/CD (.github/workflows)**:
- Automatic deployment of DBT to the PostgreSQL database at Railway
- Executes DAGs on Astronomer via GitHub Actions

## Directories in Detail
| Directory | Description |
| ------------------- | -------------------------------------------------------------------- |
| `.github/workflows` | CI/CD pipelines with deployment on Railway and DAG execution on Astro |
| `airflow`           | Airflow 3.0 DAGs and Astronomer project setup |
| `data_warehouse`    | DBT project with layer structure (staging, intermediate, mart) |
| `local_setup`       | Local setup with Docker Compose and fake data generator |