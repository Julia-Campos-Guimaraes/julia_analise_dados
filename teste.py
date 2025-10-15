import pandas as pd

# FIPEZAP: preço médio de imóveis
precos = pd.read_excel("fipezap.xlsx")

# Banco Central: juros de financiamento e Selic
juros = pd.read_csv("juros_credito_imobiliario.csv", sep=";")
selic = pd.read_csv("selic.csv", sep=";")

# IBGE: renda e desemprego
renda = pd.read_excel("renda_pnad.xlsx")
desemprego = pd.read_excel("desemprego_pnad.xlsx")

# Mesclar por data
df = precos.merge(juros, on="data", how="inner")\
           .merge(selic, on="data", how="inner")\
           .merge(renda, on="data", how="inner")\
           .merge(desemprego, on="data", how="inner")

df.head()
