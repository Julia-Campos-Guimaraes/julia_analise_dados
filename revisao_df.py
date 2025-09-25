### Revisão AP1 ###

# Lista de Exercícios sobre Pandas DataFrame (Myntra Dataset)

import pandas as pd

df= pd.read_csv("C:\\Documentos\\analise_dados\\myntra_dataset_ByScraping.csv")
df

#1- Mostrar as 5 primeiras e as 5 últimas linhas do DataFrame. 
df.head()
df.tail()

#2 - Exibir o número de linhas e colunas.
df.shape

#3 - Listar os nomes das colunas.
df.columns

#4 - Mostrar os tipos de dados de cada coluna.
df.dtypes

#5 - Usar info() para ver informações gerais.
df.info()

#6 - Verifique quais são as marcas (brand_name) que temos na amostra.
df["brand_name"].unique()

#7- Filtrar produtos com price acima de 1.000,00 e abaixo de 3.000,00
filtro_price= (df["price"]>1000) & (df["price"]<3000)
df.loc[filtro_price]

#8-Selecionar as colunas brand_name, pants_description e price em um novo DataFrame chamado df2.
df2 = df[["brand_name","pants_description","price"]]

#9-Filtrar os produtos da marca Roadster e gravar em um novo df_roadster.
df_roadster = df[df['brand_name'] == 'Roadster']
df_roadster

#10-Verificar valores nulos em cada coluna.
df.isnull().sum()

#11-Ordenar os 10 produtos mais caros (price em ordem decrescente).
df.sort_values(["price"], ascending=False).head(10)

#12-Qual é o preço médio (mean) dos produtos no dataset?
df["price"].mean()

#13- Qual é o preço mediano (median)?
df["price"].median()

#14-Qual é o desvio padrão do preço (std)?
df["price"].std()

#15- Mostre o valor mínimo e o valor máximo do desconto (discount_percent).
df["discount_percent"].min()
df["discount_percent"].max()

#16-Quantos produtos estão abaixo do preço médio e quantos estão acima?
media= df["price"].mean()

filtro = df["price"] < media
df_menor = df.loc[filtro]
len(df_menor)

filtro2 = df["price"] > media
df_maior = df.loc[filtro2]
len(df_maior)

#17-Adicionar uma nova coluna chamada preco_desconto que multiplica MRP por (1 - discount_percent).
df["preco_desconto"] = df["MRP"] * (1 - df["discount_percent"])
df.head()

#18-Remover todos os produtos com ratings menores que 2.0.
df_maiores_2 = df[df["ratings"] >= 2]

#19-Excluir a coluna pants_description.
df = df.drop(columns=['pants_description'])

#20-Agrupar por brand_name e calcular o preço médio (price).
df.groupby("brand_name")["price"].mean()


# Lista de Exercícios sobre Concat e Merge (Myntra Dataset)

#1-Crie um novo DataFrame fictício chamado df_novos_produtos com as seguintes informações e 
# use pd.concat([df, df_novos_produtos]) para juntar ao dataset original e verifique o novo tamanho do DataFrame.

dados_novos_produtos = {
    "brand_name": ["Myntra Basics", "Denim Pro", "Urban Style"],
    "pants_description": [
        "Men Slim Fit Blue Jeans",
        "Men Regular Fit Jeans",
        "Men Tapered Fit Jeans"
    ],
    "price": [1299, 1599, 1899],
    "MRP": [1999, 2499, 2899],
    "discount_percent": [0.35, 0.40, 0.34],
    "ratings": [4.1, 3.8, 4.3],
    "number_of_ratings": [23, 12, 47]
}

df_novos_produtos= pd.DataFrame(dados_novos_produtos)
df = pd.concat([df,df_novos_produtos])

#2-Crie outro DataFrame df_promocoes apenas com colunas brand_name, pants_description e discount_percent para 3 novos produtos fictícios. Depois, use pd.concat([...], axis=0) e pd.concat([...], axis=1) e explique a diferença entre concatenação por linhas e concatenação por colunas.
#Concat (juntar DataFrames):
#Por linhas (axis=0): adiciona registros.
#Por colunas (axis=1): adiciona novas colunas.

dados_promocoes = {
    "brand_name": ["Test Brand A", "Test Brand B", "Test Brand C"],
    "pants_description": [
        "Men Slim Fit Black Jeans",
        "Men Regular Fit Grey Jeans",
        "Men Loose Fit White Jeans"
    ],
    "discount_percent": [0.50, 0.60, 0.45]
}

df_promacoes= pd.DataFrame(dados_promocoes)
pd.concat([df,df_promacoes],axis=1)

#3-Crie um DataFrame auxiliar chamado df_marcas_info com informações extras sobre algumas marcas e faça um merge entre o dataset original (df) e esse DataFrame usando a coluna brand_name.
dados_marcas_info = {
    "brand_name": ["Roadster", "WROGN", "Flying Machine", "Urban Style"],
    "country": ["India", "India", "USA", "Brazil"],
    "year_founded": [2012, 2014, 1980, 2018]
}

df_marcas_info= pd.DataFrame(dados_marcas_info)
pd.merge(df,df_marcas_info, on = "brand_name", how= "inner")

## inner é a intercecção 
## left esquerda + intercecção
## right direita + intercecção
## outer junta os dois

#4- Crie um DataFrame df_categorias e faça um merge (inner join) entre df e df_categorias para adicionar a coluna category.
dados_categorias = {
    "pants_description": [
        "Men Slim Fit Jeans",
        "Men Regular Fit Jeans",
        "Men Loose Fit Cotton Jeans",
        "Men Tapered Fit Jeans"
    ],
    "category": ["Slim", "Regular", "Loose", "Tapered"]
}
df.columns
df_categorias= pd.DataFrame(dados_categorias)
pd.merge(df,df_categorias, on="pants_description", how= "inner")

#5-Imagine que você tem um DataFrame df_ratings_extra com avaliações atualizadas. Faça um merge com o dataset original, mantendo todos os registros (how='left'). Depois compare ratings (antiga) com avg_new_rating (nova).
dados_ratings_extra = {
    "brand_name": ["Roadster", "WROGN", "Urban Style"],
    "avg_new_rating": [4.0, 4.3, 4.1]
}

df_ratings_extra= pd.DataFrame(dados_ratings_extra)
df_novo = pd.merge(df,df_ratings_extra, on="brand_name", how= "left")
df_novo[["ratings","avg_new_rating"]]

