#Revisao dicionario
dic = {
    "nome": "Julia",
    "idade": 19,
    "email": "julia@gmail.com"
}

#Para acessar a chave nome, idade e email
dic["nome"]
dic["idade"]
dic["email"]

#Transformar para dataframe 
import pandas as pd
df = pd.DataFrame([dic])

# API VIACEP.com.br
import requests as rq
cep = "70295080"
url =  f"https://viacep.com.br/ws/{cep}/json/"
response = rq.get(url)
dic_cep = response.json()

# API IPEADATA
url =  f"http://www.ipeadata.gov.br/api/odata4/Metadados"
response = rq.get(url)
metadados = response.json()
metadados = metadados["value"]
pd.DataFrame(metadados)

# Acessar o codigo do IBGE
SERCODIGO = "HOMIC"
url =  f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{SERCODIGO}')"
response = rq.get(url)
dados = response.json()
dados = dados["value"]
df= pd.DataFrame(dados)

df.shape
df.columns
df.info()

pd.to_datetime(df["VALDATA"])
df["VALDATA"] = pd.to_datetime(df["VALDATA"], errors="coerce")
df["VALDATA"] = df["VALDATA"].dt.year
df["VALDATA"].unique()

filtro = df["NIVNOME"] == "Brasil"
df_brasil= df.loc[filtro]
df_brasil[["VALDATA", "VALVALOR"]].plot()

#Formatando o gráfico 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Plot
ax = df_brasil[["VALDATA", "VALVALOR"]].plot(x="VALDATA", y="VALVALOR", legend=False)
# Formatação do eixo X
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
# ou '%Y-%m-%d' conforme sua preferência
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
