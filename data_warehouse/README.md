## `data_warehouse/` — *Projeto DBT*

### O que faz:
* Contém as transformações SQL organizadas nas camadas:
  * `staging/`: ingestão e limpeza dos dados CSV
  * `intermediate/`: transformações intermediárias
  * `mart/`: modelos finais para análise

### Como Rodar Localmente:
```bash
cd data_warehouse

dbt build

dbt deps

dbt run

dbt docs generate
dbt docs serve
```

### Requisitos:
* [DBT CLI](https://docs.getdbt.com/docs/dbt-cli/installation)
* Conexão com PostgreSQL (local ou Railway)
