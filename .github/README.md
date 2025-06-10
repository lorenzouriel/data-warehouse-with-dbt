## `.github/workflows/` — *GitHub Actions (CI/CD)*

### O que faz:
* Realiza deploy automático para o banco de dados PostgreSQL na **Railway**.
* Executa pipelines do **Airflow** no **Astronomer**.

### Como Rodar:
1. Faça **push** para o branch `main` ou abra um **pull request**.
2. O GitHub Actions será automaticamente acionado:
   * Valida o projeto DBT.
   * Faz deploy para o banco PostgreSQL (Railway).
   * Executa os DAGs definidos no projeto Airflow.

### Requisitos:
* Secrets configurados no GitHub:
  * `ASTRO_API_TOKEN`
  * `ASTRO_DEPLOYMENT_ID`
  * `RAILWAY_DB_HOST`
  * `RAILWAY_DB_NAME`
  * `RAILWAY_DB_PASS`
  * `RAILWAY_DB_PORT`
  * `RAILWAY_DB_USER`