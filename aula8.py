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
lista_resultado = []
# Inicio do for loop
for ticker in tickers:
    params = {
        'ticker': ticker,
        'ano_tri': '20252T',
        }
    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
    response.status_code
    response = response.json()
    dados = response["dados"][0]
    balanco = dados["balanco"]
    df = pd.DataFrame(balanco)
    # Lucro Liquido
    filtro = (
            (df["conta"]=="3.11") &
            (df["descricao"].str.contains("^lucro", case=False)) &
            (df["data_ini"]=="2025-01-01")
            )
    lucro_liquido = df.loc[filtro, ["valor"]].iloc[0]
    # PL
    filtro = (
            (df["conta"].str.contains("2.0.", case=False)) &
            (df["descricao"].str.contains("^patrim", case=False))
            )
    pl = df.loc[filtro, ["valor"]].iloc[0]
    roe = lucro_liquido / pl
    roe = roe.iloc[0]
    resultados = {
                "ticker":ticker,
                "roe": roe
        }
    lista_resultado.append(resultados)
    print(ticker, roe)
df_roe = pd.DataFrame(lista_resultado)


lista_resultado2 = []
#Looping do ROIC
for ticker in tickers:
    params = {
        'ticker': ticker,
        'ano_tri': '20252T',
        }
    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
    response.status_code
    response = response.json()
    dados = response["dados"][0]
    balanco = dados["balanco"]
    df = pd.DataFrame(balanco)
    # Lucro Liquido
    filtro = (
            (df["conta"]=="3.05") &
            (df["descricao"].str.contains("Resultado Antes do Resultado Financeiro e dos Tributos", case=False)) &
            (df["data_ini"]=="2025-01-01")
            )
    lucro_operacional = df.loc[filtro, ["valor"]].iloc[0]
     # PL
    filtro = (
            (df["conta"].str.contains("2.0.", case=False)) &
            (df["descricao"].str.contains("^patrim", case=False))
            )
    pl = df.loc[filtro, ["valor"]].iloc[0]
    # Emprestimos
    filtro = (
            (df["conta"].str.contains("2.01.04", case=False)) &
            (df["descricao"].str.contains("^empr.stimos.*", case=False))
            )
    emprestimos = df.loc[filtro, ["valor"]].iloc[0]
    #ROIC
    roic = lucro_operacional / (emprestimos+pl)
    roic = roic.iloc[0]
    resultados = {
                "ticker":ticker,
                "roic": roic
        }
    lista_resultado2.append(resultados)
    print(ticker, roic)

df_roic = pd.DataFrame(lista_resultado2)
df_final = pd.merge(df_roe,df_roic)
df_final["media"] = (df_final["roe"] + df_final["roic"]) / 2
df_final.sort_values("media")
 
 # Calcular P/VA
lista_resultado3 = []
for ticker in tickers:
    params = {
        'ticker': ticker,
        'ano_tri': '20252T',
        }
    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
    response.status_code
    response = response.json()
    dados = response["dados"][0]
    # Numero de acoes da empresa (ticker)
    n_acoes = dados["total"]
    # Balanco
    balanco = dados["balanco"]
    df = pd.DataFrame(balanco)
   # Lucro Liquido
    filtro = (
            (df["conta"]=="3.11") &
            (df["descricao"].str.contains("^lucro", case=False)) &
            (df["data_ini"]=="2025-01-01")
            )
    lucro_liquido = df.loc[filtro, "valor"].iloc[0]
    # PL
    filtro = (
            (df["conta"].str.contains("2.0.", case=False)) &
            (df["descricao"].str.contains("^patrim", case=False))
            )
    pl = df.loc[filtro, "valor"].iloc[0]
    # Pegar o preco
    params = {'data_base': '2025-09-01'}
    response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
    response = response.json()
    dados = response["dados"]
    df_planilhao = pd.DataFrame(dados)
    filtro = df_planilhao["ticker"] == ticker
    preco = df_planilhao.loc[filtro,"preco"].iloc[0]
    p_vp = (preco * n_acoes ) / (pl * 1000 )
    p_lucro = ( preco * n_acoes) / (lucro_liquido * 1000)
    resultados = {
                "ticker":ticker,
                "p_vp": p_vp,
                "p_lucro": p_lucro
        }
    lista_resultado3.append(resultados)
    print(ticker, p_vp, p_lucro)

df_desconto = pd.DataFrame(lista_resultado3)
df_final = pd.merge(df_final, df_desconto)
df_final["media_desconto"] = ( abs(df_final["p_vp"]) + abs(df_final["p_lucro"]) ) / 2
df_final.sort_values("media_desconto", ascending=False)