import pandas as pd

df = pd.read_csv("C:\\Documentos\\analise_dados\\imoveis_brasil.csv")

# 1. Mostrar as 5 primeiras, 5 últimas e amostra de 5
df.head()
df.tail()
df.sample(5)

# 2. Número de linhas e colunas
df.shape

# 3. Listar nomes das colunas
df.columns

# 4. Tipos de dados
df.dtypes

# 5. Estatísticas numéricas
df.describe()

# 6. Informações gerais
df.info()

# 7. Tipos de imóveis
df['Tipo_Imovel'].unique()

# 8. Filtrar imóveis acima de R$ 1.000.000,00
df_caros = df["Valor_Imovel"] > 1000000
df_1M = df.loc[df_caros]
df_1M

# 9. Selecionar colunas cidade, bairro e valor
df2 = df[['Cidade', 'Bairro', 'Valor_Imovel']]
df2.head()

# 10. Filtrar imóveis de Curitiba
df_curitiba = df[df['Cidade'] == 'Curitiba']
df_curitiba

# 11. Verificar valores nulos
df.isnull().sum()

# 12. Ordenar 10 imóveis mais caros
df.sort_values(by='Valor_Imovel', ascending=False).head(10)

# 13. Valor médio
df['Valor_Imovel'].mean()

# 14. Valor mediano
df['Valor_Imovel'].median()

# 15. Desvio padrão
print(df['Valor_Imovel'].std())

# 16. Valor mínimo e máximo da área construída
df['Area_m2'].min()
df['Area_m2'].max()

# 17. Quantos imóveis estão abaixo/acima da média
media = df['Valor_Imovel'].mean()
"Abaixo:", (df['Valor_Imovel'] < media).sum()
"Acima:", (df['Valor_Imovel'] >= media).sum()

filtro = df["Valor_Imovel"] < media
df_menor = df.loc[filtro]
len(df_menor)

filtro2 = df["Valor_Imovel"] > media
df_maior = df.loc[filtro2]
len(df_maior)

# 18. Adicionar coluna valor_m2
df['valor_m2'] = df['Valor_Imovel'] / df['Area_m2']
df.head()

# 19. Inserir linha fictícia
nova_linha = {
    'ID_Imovel': 9999,
    'Tipo_Imovel': 'Casa',
    'Cidade': 'Teste',
    'Bairro': 'Centro',
    'Area_m2': 100,
    'Numero_Quartos': 2,
    'Numero_Banheiros': 1,
    'Numero_Vagas': 1,
    'Valor_Imovel': 999999,
    'Ano_Construcao': 2025,
    'valor_m2': 999999 / 100
}
df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)

# 20. Verificar valores nulos novamente
df.isnull().sum()

# 21. Remover imóveis com Numero_Quartos = 5
df = df[df['Numero_Quartos'] == 5]

# 22. Excluir coluna ID_Imovel
df = df.drop(columns=['ID_Imovel'])

# 23. Remover imóveis da cidade "Teste"
df = df[df['Cidade'] == 'Teste']

# 24. Agrupar por cidade e calcular média de valor dos imóveis
df.groupby('Cidade')['Valor_Imovel'].mean()