

# O dataset NCR Ride Bookings contém registros de corridas urbanas realizadas em regiões da National Capital Region (NCR), que abrange Delhi, Gurgaon, Noida, Ghaziabad, Faridabad e áreas próximas.
# Utilize os arquivos : ncr_ride_bookings.csv e ncr_ride_regions.xlsx para resolver as questoes.
# Principais informaçoes no dataset:
# Date → Data da corrida
# Time → Horário da corrida
# Booking ID → Identificador da corrida
# Booking Status → Status da corrida
# Customer ID → Identificador do cliente
# Vehicle Type → Tipo de veículo
# Pickup Location → Local de embarque
# Drop Location → Local de desembarque
# Booking Value → Valor da corrida
# Ride Distance → Distância percorrida
# Driver Ratings → Avaliação do motorista
# Customer Rating → Avaliação do cliente
# Payment Method → Método de pagamento


import pandas as pd

df_bookings= pd.read_csv("C:\\Documentos\\analise_dados\\ncr_ride_bookings.csv")

df_regioes = pd.read_excel("C:\\Documentos\\analise_dados\\ncr_ride_regioes.xlsx")

df_bookings.columns

# 1 - Quantas corridas estão com Status da Corrida como Completada ("Completed") no dataset? 
df_Completed = df_bookings[df_bookings['Booking Status'] == 'Completed']
len(df_Completed)

# 2 - Qual a proporção em relação ao total de corridas?
total = len(df_bookings)
completada = len(df_Completed)

proporcao = completada / total
proporcao

# 3 - Calcule a média e mediana da Distância percorrida por cada Tipo de veículo.
df_bookings.groupby("Vehicle Type")["Ride Distance"].mean()
df_bookings.groupby("Vehicle Type")["Ride Distance"].median()

# 4 - Qual o Metodo de Pagamento mais utilizado pelas bicicletas ("Bike") ?
df_Bike = df_bookings[df_bookings['Vehicle Type'] == 'Bike']

df_Bike.sort_values(["Payment Method"], ascending=False).head(10)

# 5 - Faca um merge com ncr_ride_regions.xlsx pela coluna ("Pickup Location") para pegar as regioes das corrifas.
# e verifique qual a Regiao com o maior Valor da corrida?

df = pd.merge(df_bookings,df_regioes, on = "Pickup Location", how= "inner")
df.columns

colunas= ["Regiao", "Booking Value"]
df= df[colunas]

df.sort_values(["Booking Value"], ascending=False).head(10)


# 6 - O IPEA disponibiliza uma API pública com diversas séries econômicas. 
# Para encontrar a série de interesse, é necessário primeiro acessar o endpoint de metadados.
# Acesse o endpoint de metadados: "http://www.ipeadata.gov.br/api/odata4/Metadados"
# e filtre para encontrar as séries da Fipe relacionadas a venda de imoveis (“venda”).
# Dica Técnica, filtre atraves das coluna FNTSIGLA: df["FNTSIGLA"].str.contains() 
# e depois SERNOME: df["SERNOME"].str.contains() 

import requests as rq
import pandas as pd


api = f"http://www.ipeadata.gov.br/api/odata4/Metadados"

response = rq.get(api)
dados = response.json()
df= pd.DataFrame(dados)


df["FNTSIGLA"].str.contains()
df["SERNOME"].str.contains()

# Descubra qual é o código da série correspondente.
# Usando o código encontrado, acesse a API de valores: f"http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{CODIGO_ENCONTRADO}')"
# e construa um DataFrame pandas com as datas (DATA) e os valores (VALVALOR).
# Converta a coluna de datas para o formato adequado (pd.to_datetime())

# 7 -  Monte um gráfico de linha mostrando a evolução das vendas ao longo do tempo.
# Dica: você pode usar a biblioteca matplotlib para gerar o gráfico.

df["data"] = pd.to_datetime(df["data"], utc=True, errors="coerce")
df["data"] = df["data"].dt.tz_convert("America/Sao_Paulo")
df["data"] = df["data"].dt.date

import matplotlib.pyplot as plt
plt.figure(figsize=(12,6))
plt.plot(df["data"], df["data"])
plt.title("evolução das vendas ao longo do tempo")
plt.xlabel("Ano")
plt.ylabel("Quantidade")
plt.grid(True)
plt.show()


# 8 - Crie o grafico do bitcoin (ticker: "btc") atraves da api preco-diversos
# Pegue o periodo compreendido entre 2001 a 2025
# Monte um gráfico de linha mostrando a evolução do preco de fechamento

import requests
import pandas as pd

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjE2OTYyLCJpYXQiOjE3NTg2MjQ5NjIsImp0aSI6ImVlMzBiNGRkZjZjNDQyODk5MGM3YWQyZjNiZTY5NGYwIiwidXNlcl9pZCI6IjgyIn0.HnQ6wHi0m7P4vNJup-xoQmblly2NzbKVeopa-99y5As"
headers = {'Authorization': 'Bearer {}'.format(token)}
params = {
'ticker': 'btc',
'data_ini': '2023-01-01',
'data_fim': '2023-09-01'
}
response = requests.get('https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params, headers=headers)

response = response.json()
dados = response["dados"]
df = pd.DataFrame(dados)

df["data"] = pd.to_datetime(df["data"], utc=True, errors="coerce")
df["data"] = df["data"].dt.tz_convert("America/Sao_Paulo")
df["data"] = df["data"].dt.date

import matplotlib.pyplot as plt
plt.figure(figsize=(12,6))
plt.plot(df["data"], df["data"])
plt.title("evolução do preco de fechamento")
plt.xlabel("Ano")
plt.ylabel("Quantidade")
plt.grid(True)
plt.show()



# 9 - Você tem acesso à API do Laboratório de Finanças, que fornece dados do Planilhão em formato JSON. 
# A autenticação é feita via JWT Token no cabeçalho da requisição.
# Acesse a API no endpoint: https://laboratoriodefinancas.com/api/v1/planilhao
# passando como parâmetro a data (por exemplo, "2025-09-23").
# Construa um DataFrame pandas a partir dos dados recebidos.
# Selecione a empresa do setor de "tecnologia" que apresenta o maior ROC (Return on Capital) nessa data.
# Exiba o ticker da empresa, setor e o valor do ROC correspondente.

import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjE2OTYyLCJpYXQiOjE3NTg2MjQ5NjIsImp0aSI6ImVlMzBiNGRkZjZjNDQyODk5MGM3YWQyZjNiZTY5NGYwIiwidXNlcl9pZCI6IjgyIn0.HnQ6wHi0m7P4vNJup-xoQmblly2NzbKVeopa-99y5As"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {
'data_base': '2025-09-23'
}
response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)


dados = response.json()
response = response.json()
dados = response["dados"]
df = pd.DataFrame(dados)
df.columns
filtro = (df["setor"]=="tecnologia")
colunas= ["ticker", "setor", "roc"]
df= df[colunas]

df[filtro].sort_values("roc", ascending= False)


# 10 - A API do Laboratório de Finanças fornece informações de balanços patrimoniais de empresas listadas na B3.
# Acesse o endpoint: https://laboratoriodefinancas.com/api/v1/balanco
# usando a empresa Gerdau ("GGBR4") e o período 2025/2º trimestre (ano_tri = "20252T").
# O retorno da API contém uma chave "balanco", que é uma lista com diversas contas do balanço.
# Localize dentro dessa lista a conta cuja descrição é “Ativo Total” e "Lucro Liquido".
# Calcule o Return on Assets que é dados pela formula: ROA = Lucro Liquido / Ativo Totais

import requests
import pandas as pd

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjE2OTYyLCJpYXQiOjE3NTg2MjQ5NjIsImp0aSI6ImVlMzBiNGRkZjZjNDQyODk5MGM3YWQyZjNiZTY5NGYwIiwidXNlcl9pZCI6IjgyIn0.HnQ6wHi0m7P4vNJup-xoQmblly2NzbKVeopa-99y5As"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'ticker': 'GGBR4', 
          'ano_tri': '20252T'
          }
response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)

response.status_code
response = response.json()
dados = response["dados"][0]
dados = dados["balanco"]
df = pd.DataFrame(dados)

df.columns
df.shape


filtro= (
        (df["conta"] == "3.11") & 
        (df["descricao"].str.contains("^lucro", case=False)) &
        (df["data_ini"]=="2025-01-01")
        )

lucro_liquido = df.loc[filtro,["valor"]].iloc[0]

filtro2 = (df["descricao"]=="Ativo Total")

ativo_total =df.loc[filtro2,["valor"]].iloc[0]

roa = lucro_liquido / ativo_total
roa




