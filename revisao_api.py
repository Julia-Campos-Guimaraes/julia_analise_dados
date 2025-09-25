# 1 - A BrasilAPI possui um endpoint que retorna os feriados nacionais de um ano específico.
# Acesse o endpoint:https://brasilapi.com.br/api/feriados/v1/{ano}
# Responda: quantos feriados nacionais existem no ano atual? 13

import requests as rq
import pandas as pd

ano = "2025"
url =  f"https://brasilapi.com.br/api/feriados/v1/{ano}"
response = rq.get(url)
dic_ano = response.json()
df= pd.DataFrame(dic_ano)
len(df)

# 2 - A BrasilAPI disponibiliza informações da tabela FIPE, incluindo marcas, modelos e preços de veículos.
# Acesse o endpoint de marcas da FIPE para o tipo de veículo carros.
# import requests
# import pandas as pd
# tipoVeiculo = "carros"
# api = f"https://brasilapi.com.br/api/fipe/marcas/v1/{tipoVeiculo}"
# Transforme em DataFrame e acha o codigo BYD através da coluna "nome"
# Use esse código para acessar o endpoint de modelos da marca BYD.
# codigoMarca=""
# api = f"https://brasilapi.com.br/api/fipe/veiculos/v1/{tipoVeiculo}/{codigoMarca}"
# Construa um DataFrame com os modelos disponíveis.
# Responda: quantos modelos de veículos BYD estão cadastrados na FIPE? 
# Estão cadastrados 17 modelos

import requests as rq
import pandas as pd
tipoVeiculo = "carros"
api = f"https://brasilapi.com.br/api/fipe/marcas/v1/{tipoVeiculo}"

response = rq.get(api)
dados = response.json()
df= pd.DataFrame(dados)

df_byd = df[df['nome'] == 'BYD']

codigoMarca="238"
api = f"https://brasilapi.com.br/api/fipe/veiculos/v1/{tipoVeiculo}/{codigoMarca}"

response = rq.get(api)
dados = response.json()
df2= pd.DataFrame(dados)
len(df2)


# 3 - O Banco Mundial disponibiliza uma API pública com diversos indicadores econômicos. 
# O código do indicador NY.GDP.PCAP.CD corresponde ao PIB per capita (em dólares correntes).
# Usando Python e a biblioteca requests para acessar a API e pandas para manipulação dos dados:
# Acesse o indicador NY.GDP.PCAP.CD para o Brasil (BRA).
# Construa um DataFrame contendo os anos (date) e os valores de PIB per capita (value).
# Identifique em qual ano o Brasil apresentou o menor PIB per capita e mostre o respectivo valor.

# import requests
# import pandas as pd
# pais=""
# indicador=""
# url = f"https://api.worldbank.org/v2/country/{pais}/indicator/{indicador}?format=json"

import requests as rq
import pandas as pd
pais="BRA"
indicador="NY.GDP.PCAP.CD"
url = f"https://api.worldbank.org/v2/country/{pais}/indicator/{indicador}?format=json"

dados2 = rq.get(url).json()[1]
pd.json_normalize(dados2)
df= pd.DataFrame(dados2)
response = rq.get(url)

df= df[["date","value"]]
menor= df["value"].min()
filtro = df["value"]==menor

df.sort_values(["value"], ascending=True).head(1)



# 4 - O IPEA disponibiliza uma API pública com diversas séries econômicas. 
# Para encontrar a série de interesse, é necessário primeiro acessar o endpoint de metadados.
# Acesse o endpoint de metadados: http://www.ipeadata.gov.br/api/odata4/Metadados
# e filtre para encontrar as séries da ANFAVEA relacionadas a “licenciamento”.
# Dica Técnica, filtre atraves das colunas FNTSIGLA e depois SERNOME:

import requests as rq
import pandas as pd

api= "http://www.ipeadata.gov.br/api/odata4/Metadados"
dados= rq.get(api).json()['value']
df=pd.DataFrame(dados)
df_anfave = df[df["FNTSIGLA"].str.contains("anfavea.*",regex=True,case=False)]
df_anfave[df_anfave["SERNOME"].str.contains("licenciamento",regex=True,case=False)]

# df_anfavea = df[df["FNTSIGLA"].str.contains("anfavea.*", regex=True, case=False)]
# df_anfavea[df_anfavea["SERNOME"].str.contains("licenciamento", regex=True, case=False)]

# Descubra qual é o código da série correspondente ao total de Licenciamentos de Autoveículos.
# Observe a descrição da série (SERCOMENTARIO) para confirmar que se trata de automóveis, veículos comerciais leves e pesados.
# Usando o código encontrado, acesse a API de valores: http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='CODIGO_ENCONTRADO')
# e construa um DataFrame pandas com as datas (DATA) e os valores (VALVALOR).
# Converta a coluna de datas para o formato adequado.
# Dicas técnicas: Para tratar corretamente as datas da série:

import requests as rq
import pandas as pd

SERCODIGO= "ANFAVE12_LICVETOT12"
api =  f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{SERCODIGO}')"

dados=rq.get(api).json()
dados=dados['value']
df=pd.DataFrame(dados)

df["VALDATA"] = pd.to_datetime(df["VALDATA"], utc=True, errors="coerce")
df["VALDATA"] = df["VALDATA"].dt.tz_convert("America/Sao_Paulo")
df["DATA"] = df["VALDATA"].dt.date

# Monte um gráfico de linha mostrando a evolução dos licenciamentos de autoveículos ao longo do tempo.
# Dica: você pode usar a biblioteca matplotlib ou pandas.plot para gerar o gráfico.

import matplotlib.pyplot as plt
plt.figure(figsize=(12,6))
plt.plot(df["DATA"], df["VALVALOR"])
plt.title("Licenciamento de Autoveículos no Brasil")
plt.xlabel("Ano")
plt.ylabel("Quantidade")
plt.grid(True)
plt.show()




# 5 - Utilize a API PTAX do Banco Central (endpoint CotacaoDolarPeriodo) para obter as cotações do dólar (compra e venda) em um período definido por você (ex.: de 01/01/2023 a 31/12/2023).
# Baixe os dados e monte um DataFrame com as datas e as cotações.
# Converta a coluna de datas para o formato adequado.
# Construa um gráfico de linha mostrando a evolução do dólar (venda) ao longo do período.
# import requests
# import pandas as pd
# url = (
#     "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
#     "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
#     "@dataInicial='01-01-2023'&@dataFinalCotacao='12-31-2023'&$format=json"
# )

import requests as rq
import pandas as pd

url = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
     "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
    "@dataInicial='01-01-2023'&@dataFinalCotacao='12-31-2023'&$format=json"
)
dados=rq.get(url).json()
dados=dados['value']
df=pd.DataFrame(dados)

df["dataHoraCotacao"] = pd.to_datetime(df["dataHoraCotacao"], utc=True, errors="coerce")
df["dataHoraCotacao"] = df["dataHoraCotacao"].dt.tz_convert("America/Sao_Paulo")
df["dataHoraCotacao"] = df["dataHoraCotacao"].dt.date

import matplotlib.pyplot as plt
plt.figure(figsize=(12,6))
plt.plot(df["dataHoraCotacao"], df["cotacaoVenda"])
plt.title("Cotação do Dolar")
plt.xlabel("Ano-Mes")
plt.ylabel("Cotação")
plt.grid(True)
plt.show()