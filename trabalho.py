import pandas as pd
import seaborn as sns
import statsmodels.api as sm 
import pandas as pd
import matplotlib.pyplot as plt

### Testes 

df= pd.read_csv("C:\\Documentos\\analise_dados\\dados_completos (1).csv")
df

#Primeira analise dos dados
df.shape
df.columns

#variavel independente
X= df[["Gasto_Seguranca", "PIB"]]

#variavel dependente
y= df["Qtd_Homicidios"]

#Constante
x = sm.add_constant(X)
modelo = sm.OLS(y,X).fit()
print(modelo.summary())

modelo.params
modelo.pvalues
modelo.rsquared
modelo.rsquared_adj

# Variável independente (X)
X = df["Gasto_Seguranca"]

# Variável dependente (y)
y = df["Qtd_Homicidios"]

# Adicionar constante (intercepto)
X = sm.add_constant(X)

# Estimar o modelo MQO (OLS)
modelo = sm.OLS(y, X).fit()

# Exibir o resumo dos resultados
print(modelo.summary())

#Histograma
sns.histplot(data=df, x = "Gasto_Seguranca")

#Boxplot
sns.boxplot(data=df, x = "Gasto_Seguranca")

#Correlação
df2 = df[["Gasto_Seguranca","PIB","Qtd_Homicidios","População"]]
df_numerico = df2.select_dtypes(include = "number")
df_corr = df_numerico.corr()
sns.heatmap(df_corr, annot=True)

###

# Variável independente (X)
X = df["PIB"]

# Variável dependente (y)
y = df["Gasto_Seguranca"]

# Adicionar constante (intercepto)
X = sm.add_constant(X)

# Estimar o modelo MQO (OLS)
modelo = sm.OLS(y, X).fit()

# Exibir o resumo dos resultados
print(modelo.summary())




