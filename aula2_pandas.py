import pandas as pd

df= pd.read_csv("C:\\Documentos\\analise_dados\\imoveis_brasil.csv")
df

#Primeira analise dos dados
df.shape
df.columns
df.head(5)
df.tail(5)
df.sample(5)
df.info()

#Verificar os tipos de imoveis
df["Tipo_Imovel"].unique()

#Imoveis com valor maiores que 1 milhão
filtro = df["Valor_Imovel"] > 1000000
df_1M = df.loc[filtro]
df_1M

#Selecionar Cidade, Bairro e Valor imovel
df2 = df[["Cidade","Bairro","Valor_Imovel"]]

#Ordenar os valores dos imoveis mais caros
df.sort_values(["Valor_Imovel"], ascending=False)

#Valor medio dos imoveis
valor_medio_geral = df["Valor_Imovel"].mean()

# Valor medio imoveis de curitiba
filtro1= df["Cidade"] == "Curitiba"
valor_medio = df.loc[filtro1, ["Valor_Imovel"]].mean()
valor_medio

#Numero de imoveis abaixo do valor medio
filtro = df["Valor_Imovel"] < valor_medio_geral
df_menor = df.loc[filtro]
len(df_menor)

#Numero de imoveis acima do valor medio
filtro2 = df["Valor_Imovel"] > valor_medio_geral
df_maior = df.loc[filtro2]
len(df_maior)