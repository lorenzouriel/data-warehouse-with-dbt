## `data_warehouse/` — *Projeto DBT*

### O que faz:
* Contém as transformações SQL organizadas nas camadas:
  * `staging/`: ingestão e limpeza dos dados CSV
  * `intermediate/`: transformações intermediárias
  * `mart/`: modelos finais para análise

### Como Rodar Localmente:
```bash
cd data_warehouse

# Constrói todo o pipeline (models + seeds + snapshots + tests)
dbt build

# (Opcional) Instala dependências externas (se houver pacotes dbt no projeto)
dbt deps

# Executa os modelos dbt
dbt run

# Gera e abre a documentação dos modelos
dbt docs generate
dbt docs serve
```

### Requisitos:
* [DBT CLI](https://docs.getdbt.com/docs/dbt-cli/installation)
* Conexão com PostgreSQL (local ou Railway)
