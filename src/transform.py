from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")

ARQUIVOS = {
    "selic": "selic_raw.csv",
    "dolar": "dolar_raw.csv",
}

NOMES_INDICADORES = {
    "selic": "Selic",
    "dolar": "Dólar",
}

def carregar_base(nome, arquivo):
    df = pd.read_csv(RAW_DIR / arquivo)

    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["valor"] = pd.to_numeric(
        df["valor"].astype(str).str.replace(",", ".", regex=False),
        errors="coerce"
    )
    df["indicador"] = NOMES_INDICADORES[nome]

    return df[["data", "indicador", "valor"]]

def calcular_metricas(df):
    df = df.sort_values(["indicador", "data"]).copy()

    df["variacao_absoluta"] = df.groupby("indicador")["valor"].diff()
    df["variacao_percentual"] = df.groupby("indicador")["valor"].pct_change() * 100
    df["media_movel_7"] = df.groupby("indicador")["valor"].transform(
        lambda s: s.rolling(7, min_periods=1).mean()
    )
    df["media_movel_30"] = df.groupby("indicador")["valor"].transform(
        lambda s: s.rolling(30, min_periods=1).mean()
    )

    return df

def main():
    partes = []

    for nome, arquivo in ARQUIVOS.items():
        partes.append(carregar_base(nome, arquivo))

    base = pd.concat(partes, ignore_index=True)
    base = calcular_metricas(base)

    return base

if __name__ == "__main__":
    df_final = main()
    print(df_final.head())