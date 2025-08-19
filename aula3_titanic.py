import pandas as pd
arquivo = "C:\\Documentos\\analise_dados\\titanic.csv"
df = pd.read_csv(arquivo)

df.shape
df.columns
df.info()

# Encontrar linhas com valores NA
df.isnull().sum()
filtro = df["Fare"].isna()
df.loc[filtro]

filtro_age = df["Age"].isna()
df.loc[filtro_age]

#Substituir os valores NA por 0
media_age = df["Age"].mean()
df["Age"]= df["Age"].fillna(0)

#Exclui os valores NA
df["Age"]= df["Age"].dropna()

#Calcular a media de idade dos homens e das mulheres
filtro_homem = df["Sex"] == "male"
df_homem = df.loc[filtro_homem]
df_homem["Age"].mean()

filtro_mulheres = df["Sex"] == "female"
df_mulheres = df.loc[filtro_mulheres]
df_mulheres["Age"].mean()

#groupby
df.groupby("Sex")["Age"].mean()
df.groupby("Sex")["Age"].min()
df.groupby("Sex")["Age"].max()

#Filtrar atraves de duas colunas
filtro= (df["Sex"] == "male") & (df["Survived"] ==1)
df_homem_sobrevivente = df.loc[filtro]

filtro= (df["Sex"] == "female") & (df["Survived"] ==1)
df_mulheres_sobrevivente = df.loc[filtro]

#Criar uma coluna nova chamada "FamilyMembers"
df.columns
df["FamilyMembers"] = df["SibSp"] + df["Parch"] + 1
df.head()

