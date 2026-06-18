from pathlib import Path
from datetime import datetime
import requests
import pandas as pd

DATA_INICIAL = "01/01/2020"
DATA_FINAL = datetime.today().strftime("%d/%m/%Y")

BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
RAW_DIR = Path("data/raw")

SERIES = {
    "selic": 11,
    "dolar": 1
}


def fetch_bcb_series(codigo, data_inicial, data_final):
    url = BASE_URL.format(codigo=codigo)
    params = {
        "formato": "json",
        "dataInicial": data_inicial,
        "dataFinal": data_final
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    if not data:
        raise ValueError(f"Nenhum dado retornado para a série {codigo}.")

    return pd.DataFrame(data)


def save_raw_data(df, nome_arquivo):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    caminho = RAW_DIR / nome_arquivo
    df.to_csv(caminho, index=False, encoding="utf-8-sig")


def main():
    for nome, codigo in SERIES.items():
        df = fetch_bcb_series(codigo, DATA_INICIAL, DATA_FINAL)
        save_raw_data(df, f"{nome}_raw.csv")
        print(f"{nome}_raw.csv salvo com sucesso.")


if __name__ == "__main__":
    main()