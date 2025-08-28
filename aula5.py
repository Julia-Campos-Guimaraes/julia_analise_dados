import pandas as pd
file = "C:\\Users\\21701079836\\Documents\\analise_dados\\cadastro_alunos.xlsx"
df = pd.read_excel(file)
filtro = df["nome_aluno"].str.contains("^sabrina|ana|lucas", case=False)
df.loc[filtro]

import requests
import pandas as pd
url = "http://www.ipeadata.gov.br/api/odata4/Metadados"
response = requests.get(url)
metadados = response.json()
metadados = metadados["value"]
df = pd.DataFrame(metadados)
filtro = df["SERNOME"].str.contains("IPCA - educação, leitura e papelaria - taxa de variação", case=False)
df.loc[filtro, ["SERNOME"]].values
df.loc[filtro]
# Acessar o cogigo do IBGE
SERCODIGO = "PRECOS12_IPCAED12"
url = f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{SERCODIGO}')"
response = requests.get(url)
dados = response.json()
dados = dados["value"]
df = pd.DataFrame(dados)
df.info()
df["VALDATA"] = pd.to_datetime(df["VALDATA"], errors="coerce")
df[["VALDATA", "VALVALOR"]].plot()



import requests
uri = 'https://api.football-data.org/v4/matches'
headers = { 'X-Auth-Token': '60b7e30e5d1240758181bad62d9cd7dd' }
response = requests.get(uri, headers=headers)
response = response.json()
matches = response["matches"]
df = pd.DataFrame(matches)