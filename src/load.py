from pathlib import Path

PROCESSED_DIR = Path("data/processed")

def salvar_base_final(df, nome_arquivo="base_final.csv"):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    caminho = PROCESSED_DIR / nome_arquivo
    df.to_csv(caminho, index=False, encoding="utf-8-sig")
    print(f"{nome_arquivo} salvo com sucesso em {caminho}")