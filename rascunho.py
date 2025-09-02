
import requests
import pandas as pd
import time

# === Autenticação ===
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxMzUzLCJpYXQiOjE3NTYzNzkzNTMsImp0aSI6ImYxMmMzYjlmNDc0MzQxYmFhOGMzMzQwMDFjMzMzMmFlIiwidXNlcl9pZCI6IjgyIn0.ovZAHyl81GECYRq-rKDIYyvaQyUJM4Eac_ML1iP2564"
headers = {'Authorization': f'JWT {token}'}

# === 1) Buscar todos os tickers disponíveis ===
resp_tickers = requests.get('https://laboratoriodefinancas.com/api/v1/ticker', headers=headers)
resp_tickers.raise_for_status()
payload = resp_tickers.json()

# Normaliza a resposta para uma lista de itens
if isinstance(payload, dict):
    if 'results' in payload:
        itens = payload['results']
    elif 'dados' in payload:
        itens = payload['dados']
    else:
        # caso venha um dict com outra chave, tenta usar todos os valores
        itens = list(payload.values())
        # achata 1 nível se necessário
        if itens and isinstance(itens[0], list):
            itens = itens[0]
elif isinstance(payload, list):
    itens = payload
else:
    itens = []

def extrair_ticker(item):
    if isinstance(item, dict):
        for k in ['ticker', 'sigla', 'codigo', 'symbol', 'cd_acao', 'cd_ticker']:
            if k in item and isinstance(item[k], str) and item[k].strip():
                return item[k].strip().upper()
    elif isinstance(item, str):
        return item.strip().upper()
    return None

lista_todos_tickers = sorted({t for t in (extrair_ticker(x) for x in itens) if t})

# (Opcional) Filtra tickers claramente inválidos (ex.: None, muito curtos)
lista_todos_tickers = [t for t in lista_todos_tickers if len(t) >= 4]

print(f"Total de tickers carregados: {len(lista_todos_tickers)}")

# === 2) Loop no MESMO MODELO que você enviou, mas agora para todos os tickers ===
resultados = []  # para armazenar (ticker, lucro, pl, roe)

for ticker in lista_todos_tickers:
    params = {
        'ticker': ticker,
        'ano_tri': '20252T',   # mantenho igual ao seu modelo
    }

    try:
        response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',
                                params=params, headers=headers)

        if response.status_code != 200:
            # pula tickers que não retornam 200
            continue

        response = response.json()
        if not response or "dados" not in response or len(response["dados"]) == 0:
            continue

        dados = response["dados"][0]
        balanco = dados.get("balanco", [])
        if not balanco:
            continue

        df = pd.DataFrame(balanco)

        # Garantir que as colunas existem
        if not set(['conta','descricao','data_ini','valor']).issubset(df.columns):
            continue

        # Lucro Líquido (mesmo filtro do seu modelo)
        filtro = (
            (df["conta"] == "3.11") &
            (df["descricao"].str.contains("^lucro", case=False, na=False)) &
            (df["data_ini"] == "2025-01-01")
        )

        if df.loc[filtro, "valor"].empty:
            # fallback: pega a 1ª linha de lucro com conta 3.11 caso a data específica não exista
            filtro_alt = (
                (df["conta"] == "3.11") &
                (df["descricao"].str.contains("^lucro", case=False, na=False))
            )
            if df.loc[filtro_alt, "valor"].empty:
                continue
            lucro_liquido = float(pd.to_numeric(df.loc[filtro_alt, "valor"], errors='coerce').dropna().iloc[0])
        else:
            lucro_liquido = float(pd.to_numeric(df.loc[filtro, "valor"], errors='coerce').dropna().iloc[0])

        # Patrimônio Líquido (mesmo filtro do seu modelo)
        filtro2 = (
            (df["conta"].astype(str).str.contains("2.0.", case=False, na=False)) &
            (df["descricao"].str.contains("^patrim.nio", case=False, na=False))
        )

        if df.loc[filtro2, "valor"].empty:
            continue

        patrimonio_liquido = float(pd.to_numeric(df.loc[filtro2, "valor"], errors='coerce').dropna().iloc[0])

        # Evita divisão por zero
        if patrimonio_liquido == 0:
            continue

        roe = lucro_liquido / patrimonio_liquido

        resultados.append({
            "ticker": ticker,
            "lucro_liquido": lucro_liquido,
            "patrimonio_liquido": patrimonio_liquido,
            "roe": roe
        })

        # imprime no formato do seu modelo
        print(roe)

        # (Opcional) pequena pausa para não sobrecarregar a API
        time.sleep(0.15)

    except Exception as e:
        # Em produção, você pode querer logar o erro com mais detalhes
        # print(f"Erro com {ticker}: {e}")
        continue

# === 3) DataFrame final com todos os ROEs (se quiser trabalhar depois) ===
df_roe = pd.DataFrame(resultados).sort_values("roe", ascending=False).reset_index(drop=True)
print(df_roe.head())
# df_roe.to_csv("roe_todos_tickers.csv", index=False)  # opcional
# df_roe.to_excel("roe_todos_tickers.xlsx", index=False)  # opcional


#### Planilhão ####

import requests
import pandas as pd
import numpy as np

token = "SEU_TOKEN_AQUI"
headers = {'Authorization': 'JWT {}'.format(token)}

params = {
    'data_base': '2025-09-01'
}

response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',
                        params=params, headers=headers)
response = response.json()
dados = response["dados"]
df = pd.DataFrame(dados)

filtro = df["setor"] == "construção"
tickers = df.loc[filtro, "ticker"].values

# início do for loop
lista_resultados = []
for ticker in tickers:
    params = {
        'ticker': ticker,
        'ano_tri': '20252T',
    }

    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',
                            params=params, headers=headers)
    response = response.json()
    dados = response["dados"][0]
    balanco = dados["balanco"]
    df = pd.DataFrame(balanco)

    # Lucro Líquido
    filtro = (
        (df["conta"] == "3.11") &
        (df["descricao"].str.contains("^lucro", case=False)) &
        (df["data_ini"] == "2025-01-01")
    )
    lucro_liquido = df.loc[filtro, ["valor"]].iloc[0]["valor"] if not df.loc[filtro].empty else np.nan

    # Patrimônio Líquido (Capital Próprio)
    filtro2 = (
        (df["conta"].str.contains("2.0.", case=False)) &
        (df["descricao"].str.contains("^patrim.nio", case=False))
    )
    patrimonio_liquido = df.loc[filtro2, ["valor"]].iloc[0]["valor"] if not df.loc[filtro2].empty else np.nan

    # ROE
    roe = lucro_liquido / patrimonio_liquido if patrimonio_liquido not in [0, np.nan] else np.nan

    # EBIT
    filtro_ebit = (
        (df["conta"] == "3.05") &
        (df["descricao"].str.contains("ebit", case=False)) &
        (df["data_ini"] == "2025-01-01")
    )
    ebit = df.loc[filtro_ebit, ["valor"]].iloc[0]["valor"] if not df.loc[filtro_ebit].empty else np.nan

    # Empréstimos e Financiamentos (Capital de Terceiros)
    filtro_divida = (
        (df["conta"] == "2.0104") &
        (df["descricao"].str.contains("empréstimos|financiamentos", case=False))
    )
    divida = df.loc[filtro_divida, ["valor"]].iloc[0]["valor"] if not df.loc[filtro_divida].empty else 0

    # Capital Investido = PL + Dívida
    capital_investido = patrimonio_liquido + divida if patrimonio_liquido is not np.nan else np.nan

    # ROIC
    roic = ebit / capital_investido if capital_investido not in [0, np.nan] else np.nan

    # Guarda os resultados
    resultados = {
        "ticker": ticker,
        "roe": roe,
        "roic": roic
    }
    lista_resultados.append(resultados)

# DataFrame final
df_final = pd.DataFrame(lista_resultados)
print(df_final)

# opcional: exportar para CSV
df_final.to_csv("resultados_roe_roic.csv", index=False)
