import requests
import pandas as pd

# === Token ===
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxMzUzLCJpYXQiOjE3NTYzNzkzNTMsImp0aSI6ImYxMmMzYjlmNDc0MzQxYmFhOGMzMzQwMDFjMzMzMmFlIiwidXNlcl9pZCI6IjgyIn0.ovZAHyl81GECYRq-rKDIYyvaQyUJM4Eac_ML1iP2564"
headers = {'Authorization': 'JWT {}'.format(token)}

# === 1) Pegar todos os tickers disponíveis ===
resp = requests.get('https://laboratoriodefinancas.com/api/v1/ticker', headers=headers)
tickers_json = resp.json()

# Se vier em 'dados', pega de lá
if "dados" in tickers_json:
    lista_tickers = [t["ticker"] for t in tickers_json["dados"]]
# Se já vier como lista direta
elif isinstance(tickers_json, list):
    lista_tickers = [t["ticker"] for t in tickers_json]
else:
    raise ValueError("Não consegui encontrar os tickers na resposta da API.")

print(f"Total de tickers carregados: {len(lista_tickers)}")

# === 2) Loop para calcular ROE de cada ticker ===
for ticker in lista_tickers:
    params = {
        'ticker': ticker,
        'ano_tri': '20252T',
    }

    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',
                            params=params, headers=headers)

    if response.status_code != 200:
        continue

    response = response.json()
    if len(response["dados"]) == 0:
        continue

    dados = response["dados"][0]
    balanco = dados["balanco"]
    df = pd.DataFrame(balanco)

    # --- Lucro Líquido ---
    filtro = (
        (df["conta"] == "3.11") &
        (df["descricao"].str.contains("^lucro", case=False)) &
        (df["data_ini"] == "2025-01-01")
    )

    if df.loc[filtro, "valor"].empty:
        continue
    lucro_liquido = df.loc[filtro, "valor"].iloc[0]

    # --- Patrimônio Líquido ---
    filtro2 = (
        (df["conta"].str.contains("2.0.", case=False)) &
        (df["descricao"].str.contains("^patrim.nio", case=False))
    )

    if df.loc[filtro2, "valor"].empty:
        continue
    patrimonio_liquido = df.loc[filtro2, "valor"].iloc[0]

    # --- ROE ---
    if patrimonio_liquido != 0:
        roe = lucro_liquido / patrimonio_liquido
        print(f"{ticker}: ROE = {roe:.2%}")


