#Planilhao

import requests
import pandas as pd

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5NDAyODg3LCJpYXQiOjE3NTY4MTA4ODcsImp0aSI6ImY5ZDE5OTNkYjNhYzQ3NTNiNjk3ZGMwZWIwZjJkNDg5IiwidXNlcl9pZCI6IjgyIn0.ROdPmL1g4fTMTZTgbAe5MlNWHvG8A8w6Jh24cX28CXU"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'data_base': '2025-09-01'}
response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
response = response.json()
dados = response["dados"]
df = pd.DataFrame(dados)
filtro = df["setor"]=="construção"
tickers = df.loc[filtro, "ticker"].values

# Inicio do for loop
lista_roic = []
lista_roe = []

for ticker in tickers:
    params = {
        'ticker': ticker,
        'ano_tri': '20252T',
    }
    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco', params=params, headers=headers)
    response = response.json()
    dados = response["dados"][0]
    balanco = dados["balanco"]
    df = pd.DataFrame(balanco)

    # EBIT (Lucro Operacional)
    filtro = (
        (df["conta"]=="3.05") &
        (df["descricao"].str.contains("^resultado antes", case=False)) &
        (df["data_ini"]=="2025-01-01")
    )
    lucro_operacional = df.loc[filtro, ["valor"]].iloc[0]

    # PL
    filtro = (
        (df["conta"].str.contains("2.0.", case=False)) &
        (df["descricao"].str.contains("^patrim", case=False))
    )
    pl = df.loc[filtro, ["valor"]].iloc[0]

    # Empréstimos
    filtro = (
        (df["conta"].str.contains("2.01.04", case=False)) &
        (df["descricao"].str.contains("^empr.stimo", case=False))
    )
    emprestimo = df.loc[filtro, ["valor"]].iloc[0]

    # ROIC
    roic = (lucro_operacional / (pl + emprestimo)).iloc[0]
    lista_roic.append({"ticker": ticker, "roic": roic})

    # Lucro Líquido
    filtro = (
        (df["conta"]=="3.11") &
        (df["descricao"].str.contains("^lucro", case=False)) &
        (df["data_ini"]=="2025-01-01")
    )
    lucro_liquido = df.loc[filtro, ["valor"]].iloc[0]

    # ROE
    roe = (lucro_liquido / pl).iloc[0]
    lista_roe.append({"ticker": ticker, "roe": roe})


# Criar DataFrames separados
df_roic = pd.DataFrame(lista_roic)  # contém ticker e roic
df_roe = pd.DataFrame(lista_roe)   # contém ticker e roe

# Merge
df_final = pd.DataFrame.merge(df_roic, df_roe, on="ticker")

# Coluna média
df_final["media"] = (df_final["roic"] + df_final["roe"]) / 2

