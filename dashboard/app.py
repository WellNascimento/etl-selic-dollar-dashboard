from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Selic e Dólar",
    page_icon="📊",
    layout="wide"
)

CAMINHO_BASE = Path("data/processed/base_final.csv")

@st.cache_data
def carregar_dados():
    df = pd.read_csv(CAMINHO_BASE)
    df["data"] = pd.to_datetime(df["data"])
    return df

def formatar_valor(row):
    if row["indicador"] == "Dólar":
        return f"R$ {row['valor']:.2f}"
    return f"{row['valor']:.2f}%"

df = carregar_dados()

st.title("Dashboard ETL - Selic e Dólar")
st.caption("Visão inicial dos dados tratados do Banco Central.")

indicadores = st.sidebar.multiselect(
    "Indicadores",
    options=sorted(df["indicador"].unique()),
    default=sorted(df["indicador"].unique())
)

data_min = df["data"].min().date()
data_max = df["data"].max().date()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

if len(periodo) == 2:
    data_inicio, data_fim = periodo
else:
    data_inicio, data_fim = data_min, data_max

df_filtrado = df[
    (df["indicador"].isin(indicadores)) &
    (df["data"].dt.date >= data_inicio) &
    (df["data"].dt.date <= data_fim)
].copy()

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

df_filtrado["valor_formatado"] = df_filtrado.apply(formatar_valor, axis=1)

ultimos = (
    df_filtrado.sort_values("data")
    .groupby("indicador", as_index=False)
    .tail(1)
    .set_index("indicador")
)

col1, col2, col3 = st.columns(3)

with col1:
    if "Selic" in ultimos.index:
        st.metric(
            "Selic atual",
            f"{ultimos.loc['Selic', 'valor']:.2f}%",
            f"{ultimos.loc['Selic', 'variacao_absoluta']:.2f}" if pd.notna(ultimos.loc['Selic', 'variacao_absoluta']) else None
        )

with col2:
    if "Dólar" in ultimos.index:
        st.metric(
            "Dólar atual",
            f"R$ {ultimos.loc['Dólar', 'valor']:.2f}",
            f"{ultimos.loc['Dólar', 'variacao_absoluta']:.2f}" if pd.notna(ultimos.loc['Dólar', 'variacao_absoluta']) else None
        )

with col3:
    st.metric("Registros filtrados", len(df_filtrado))

st.divider()

col_graf, col_info = st.columns([2, 1])

with col_graf:
    st.subheader("Evolução dos indicadores")
    fig = px.line(
        df_filtrado,
        x="data",
        y="valor",
        color="indicador",
        title="Série temporal",
        markers=False
    )
    fig.update_layout(legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

with col_info:
    st.subheader("Resumo")
    st.write(f"**Início:** {data_inicio}")
    st.write(f"**Fim:** {data_fim}")
    st.write(f"**Indicadores:** {', '.join(indicadores)}")
    st.write(f"**Total de linhas:** {len(df_filtrado)}")

st.subheader("Métricas calculadas")
metrica = st.selectbox(
    "Escolha a métrica",
    ["variacao_absoluta", "variacao_percentual", "media_movel_7", "media_movel_30"]
)

fig_metrica = px.line(
    df_filtrado,
    x="data",
    y=metrica,
    color="indicador",
    title=f"{metrica.replace('_', ' ').title()}"
)
fig_metrica.update_layout(legend_title_text="")
st.plotly_chart(fig_metrica, use_container_width=True)

st.subheader("Dados filtrados")
mostrar_colunas = ["data", "indicador", "valor", "variacao_absoluta", "variacao_percentual"]
st.dataframe(df_filtrado[mostrar_colunas], use_container_width=True)