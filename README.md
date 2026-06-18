# ETL SELIC e Dólar Dashboard

Projeto em Python para extração, transformação, carga e visualização de dados públicos do Banco Central do Brasil, com foco nas séries da taxa Selic e do dólar comercial (venda) [1][2].

## Objetivo

O projeto coleta dados do Banco Central, trata os arquivos em formato tabular e disponibiliza uma dashboard interativa para análise de histórico, variações e médias móveis dos indicadores Selic e Dólar [1][3].

## Estrutura do projeto

```text
ETL-SELIC-DOLLAR-DASHBOARD/
├── data/
│   ├── raw/
│   └── processed/
├── dashboard/
│   └── app.py
├── docs/
│   └── prints/
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Etapas do pipeline

### Extract

A etapa de extração consome séries temporais do SGS do Banco Central por meio do endpoint `bcdata.sgs.{codigo}/dados`, com parâmetros como `formato=json`, `dataInicial` e `dataFinal` [1][2]. No projeto, são utilizadas as séries 11 para Selic e 1 para dólar americano de venda diário [2][4].

Arquivos gerados:

- `data/raw/selic_raw.csv`
- `data/raw/dolar_raw.csv`

### Transform

A etapa de transformação lê os arquivos brutos com `pandas`, converte datas com `pd.to_datetime()` e calcula métricas por indicador usando operações como `groupby()`, `diff()`, `pct_change()` e `rolling()` [5][6][7]. A saída consolidada contém as colunas `data`, `indicador`, `valor`, `variacao_absoluta`, `variacao_percentual`, `media_movel_7` e `media_movel_30` [6][8].

Arquivo gerado:

- `data/processed/base_final.csv`

### Load

A etapa de carga salva a base tratada em CSV, permitindo reutilização em análises, dashboards e futuras integrações com banco de dados [9][10].

### Dashboard

A dashboard foi construída em Streamlit com leitura do CSV processado, filtros laterais, KPIs com `st.metric` e gráficos interativos com Plotly [11][12][13]. O app permite visualizar a evolução temporal dos indicadores e métricas derivadas do processamento [14][15].

## Requisitos

Instale as dependências do projeto no ambiente virtual:

```bash
pip install -r requirements.txt
```

Conteúdo sugerido para `requirements.txt`:

```txt
requests
pandas
streamlit
plotly
```

## Como executar

### 1. Rodar o pipeline ETL completo

```bash
python src/main.py
```

Esse comando executa extração, transformação e carga em sequência, seguindo a separação por módulos com `main()` e o padrão `if __name__ == "__main__"` [16][17].

### 2. Abrir a dashboard

```bash
streamlit run dashboard/app.py
```

O Streamlit é apropriado para dashboards leves e interativos em Python, com suporte nativo a layout em colunas, widgets de filtro e gráficos Plotly [18][12].

## Indicadores disponíveis

| Indicador | Fonte | Código |
|---|---|---|
| Selic | SGS/BCB [2] | 11 [2] |
| Dólar americano (venda) | SGS/BCB [4] | 1 [1] |

## Funcionalidades da dashboard

- Filtro por indicador.
- Filtro por período.
- Cards com valores mais recentes.
- Gráfico principal de evolução temporal.
- Gráfico de métricas calculadas.
- Tabela com os dados filtrados [18][13][12].

## Screenshots

### Dashboard principal



### Filtros da dashboard



### Dados filtrados



### Métricas calculadas



### Execução do pipeline



## Melhorias futuras

- Adicionar novos indicadores econômicos do Banco Central.
- Incluir publicação do app em nuvem.
- Criar logs e tratamento de erro mais detalhados no pipeline.
- Integrar a saída final a um banco de dados ou data warehouse.