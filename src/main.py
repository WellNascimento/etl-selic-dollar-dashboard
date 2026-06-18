from extract import main as extract_main
from transform import main as transform_main
from load import salvar_base_final

def main():
    extract_main()
    df_final = transform_main()
    salvar_base_final(df_final)

if __name__ == "__main__":
    main()