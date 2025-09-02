
import requests
import pandas as pd
import numpy as np

# Pegar o token na área "access" no site
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxMzUzLCJpYXQiOjE3NTYzNzkzNTMsImp0aSI6ImYxMmMzYjlmNDc0MzQxYmFhOGMzMzQwMDFjMzMzMmFlIiwidXNlcl9pZCI6IjgyIn0.ovZAHyl81GECYRq-rKDIYyvaQyUJM4Eac_ML1iP2564"
headers = {'Authorization': 'JWT {}'.format(token)}

# Ticker da Petrobras
params = {
    'ticker': 'PETR4',
    'ano_tri': '20252T',
}

response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',
                        params=params, headers=headers)

if response.status_code == 200:
    response = response.json()

    if "dados" in response and len(response["dados"]) > 0:
        dados = response["dados"][0]
        balanco = dados["balanco"]
        df = pd.DataFrame(balanco)

        # Lucro Líquido (conta 3.11)
        filtro = (
            (df["conta"] == "3.11") &
            (df["descricao"].str.contains("^lucro", case=False)) &
            (df["data_ini"] == "2025-01-01")
        )
        lucro_liquido = df.loc[filtro, ["valor"]].iloc[0]["valor"] if not df.loc[filtro].empty else np.nan

        # Patrimônio Líquido (conta 2.03)
        filtro2 = (df["conta"] == "2.03")
        patrimonio_liquido = df.loc[filtro2, ["valor"]].iloc[0]["valor"] if not df.loc[filtro2].empty else np.nan

        # EBIT (conta 3.05)
        filtro_ebit = (df["conta"] == "3.05")
        ebit = df.loc[filtro_ebit, ["valor"]].iloc[0]["valor"] if not df.loc[filtro_ebit].empty else np.nan

        # Empréstimos e Financiamentos (conta 2.0104)
        filtro_divida = (df["conta"] == "2.0104")
        divida = df.loc[filtro_divida, ["valor"]].iloc[0]["valor"] if not df.loc[filtro_divida].empty else 0

        # Cálculo dos indicadores
        roe = lucro_liquido / patrimonio_liquido if patrimonio_liquido not in [0, np.nan] else np.nan
        capital_investido = patrimonio_liquido + divida if patrimonio_liquido is not np.nan else np.nan
        roic = ebit / capital_investido if capital_investido not in [0, np.nan] else np.nan

        # Mostrar os resultados
        print(f"Lucro Líquido: {lucro_liquido}")
        print(f"Patrimônio Líquido: {patrimonio_liquido}")
        print(f"EBIT: {ebit}")
        print(f"Dívida: {divida}")
        print(f"Capital Investido: {capital_investido}")
        print(f"ROE: {roe}")
        print(f"ROIC: {roic}")

        # Organizar em DataFrame
        resultados = [{
            "ticker": "PETR4",
            "lucro_liquido": lucro_liquido,
            "patrimonio_liquido": patrimonio_liquido,
            "ebit": ebit,
            "divida": divida,
            "roe": roe,
            "roic": roic
        }]
        df_result = pd.DataFrame(resultados)
        print(df_result)

    else:
        print("⚠️ Nenhum dado encontrado para esse ticker/periodo.")
else:
    print("Erro na requisição:", response.status_code)
