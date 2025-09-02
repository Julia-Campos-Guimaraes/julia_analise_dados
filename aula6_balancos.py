####  Petrobras  ####

import requests
import pandas as pd 

#Pegar o token na area access no site

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxMzUzLCJpYXQiOjE3NTYzNzkzNTMsImp0aSI6ImYxMmMzYjlmNDc0MzQxYmFhOGMzMzQwMDFjMzMzMmFlIiwidXNlcl9pZCI6IjgyIn0.ovZAHyl81GECYRq-rKDIYyvaQyUJM4Eac_ML1iP2564"
headers = {'Authorization': 'JWT {}'.format(token)}

#ticker é a  sigla da empresa que eu quero

params = {
'ticker': 'PETR4',
'ano_tri': '20252T',
}

response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)

response.status_code
response = response.json()
dados = response["dados"][0]
balanco = dados["balanco"]
df = pd.DataFrame(balanco)

df.columns
df.shape

#Lucro Liquido

filtro= (
    (df["conta"] == "3.11") & 
    (df["descricao"].str.contains("^lucro", case=False)) &
    (df["data_ini"]=="2025-01-01")
    )

lucro_liquido = df.loc[filtro,["valor"]].iloc[0]

#Patrimonio liquido

filtro2= (
    (df["conta"] == "2.03") & 
    (df["descricao"].str.contains("^patrim.nio", case=False))
    )

patrimonio_liquido = df.loc[filtro2,["valor"]].iloc[0]

roe = lucro_liquido / patrimonio_liquido
roe

####  VALE ####

import requests
import pandas as pd 

#Pegar o token na area access no site

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxMzUzLCJpYXQiOjE3NTYzNzkzNTMsImp0aSI6ImYxMmMzYjlmNDc0MzQxYmFhOGMzMzQwMDFjMzMzMmFlIiwidXNlcl9pZCI6IjgyIn0.ovZAHyl81GECYRq-rKDIYyvaQyUJM4Eac_ML1iP2564"
headers = {'Authorization': 'JWT {}'.format(token)}

#ticker é a  sigla da empresa que eu quero

params = {
'ticker': 'VALE3',
'ano_tri': '20252T',
}

response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)

response.status_code
response = response.json()
dados = response["dados"][0]
balanco = dados["balanco"]
df = pd.DataFrame(balanco)

df.columns
df.shape

#Lucro Liquido

filtro= (
    (df["conta"] == "3.11") & 
    (df["descricao"].str.contains("^lucro", case=False)) &
    (df["data_ini"]=="2025-01-01")
    )

lucro_liquido = df.loc[filtro,["valor"]].iloc[0]

#Patrimonio liquido

filtro2= (
    (df["conta"] == "2.03") & 
    (df["descricao"].str.contains("^patrim.nio", case=False))
    )

patrimonio_liquido = df.loc[filtro2,["valor"]].iloc[0]

roe = lucro_liquido / patrimonio_liquido
roe

# criar um for loop

for ticker in ["PETR4", "VALE3", "BBAS3"]:
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

    df.columns
    df.shape

    #Lucro Liquido

    filtro= (
        (df["conta"] == "3.11") & 
        (df["descricao"].str.contains("^lucro", case=False)) &
        (df["data_ini"]=="2025-01-01")
        )

    lucro_liquido = df.loc[filtro,["valor"]].iloc[0]

    #Patrimonio liquido

    filtro2= (
        (df["conta"].str.contains("2.0.", case=False)) & 
        (df["descricao"].str.contains("^patrim.nio", case=False))
        )

    patrimonio_liquido = df.loc[filtro2,["valor"]].iloc[0]

    roe = lucro_liquido / patrimonio_liquido
    print(roe)

    
#### Planilhão ####

import requests
import pandas as pd

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5NDAyODg3LCJpYXQiOjE3NTY4MTA4ODcsImp0aSI6ImY5ZDE5OTNkYjNhYzQ3NTNiNjk3ZGMwZWIwZjJkNDg5IiwidXNlcl9pZCI6IjgyIn0.ROdPmL1g4fTMTZTgbAe5MlNWHvG8A8w6Jh24cX28CXU"
headers = {'Authorization': 'JWT {}'.format(token)}

params = {
'data_base': '2025-09-01'
}

response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
response = response.json()
dados= response["dados"]
df = pd.DataFrame(dados)

filtro= df["setor"] == "construção"
tickers = df.loc[filtro, "ticker"].values

# início do for loop
lista_resultados= []
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

    df.columns
    df.shape

    #Lucro Liquido

    filtro= (
        (df["conta"] == "3.11") & 
        (df["descricao"].str.contains("^lucro", case=False)) &
        (df["data_ini"]=="2025-01-01")
        )

    lucro_liquido = df.loc[filtro,["valor"]].iloc[0]

    #Patrimonio liquido

    filtro2= (
        (df["conta"].str.contains("2.0.", case=False)) & 
        (df["descricao"].str.contains("^patrim.nio", case=False))
        )

    patrimonio_liquido = df.loc[filtro2,["valor"]].iloc[0]

    roe = lucro_liquido / patrimonio_liquido
    roe= roe.iloc[0]
    print(roe)


    resultados={
        "ticker":ticker,
        "roe":roe
    }

    lista_resultados.append(resultados)
    print(ticker,roe)
    df_final = pd.DataFrame(lista_resultados)

    
df_final['roe'].min()
df_final['roe'].max()
df_final.sort_values(["roe"])

    # EBIT
filtro_ebit = (
        (df["conta"] == "3.05") &
        (df["descricao"].str.contains("ebit", case=False)) &
        (df["data_ini"] == "2025-01-01")
    )
ebit = df.loc[filtro_ebit, ["valor"]].iloc[0]["valor"]

    # Empréstimos e Financiamentos
filtro_divida = (
        (df["conta"] == "2.0104") &
        (df["descricao"].str.contains("empréstimos|financiamentos", case=False))
    )
divida = df.loc[filtro_divida, ["valor"]].iloc[0]["valor"]

    # Capital investido
capital_investido = patrimonio_liquido + divida

    # ROIC
roic = ebit / capital_investido

    # adiciona no dicionário final
resultados = {
        "ticker": ticker,
        "roe": roe,
        "roic": roic
    }


