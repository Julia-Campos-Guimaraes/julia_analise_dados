import pandas as pd
import seaborn as sns
import statsmodels.api as sm 
import pandas as pd
import matplotlib.pyplot as plt

df= pd.read_excel("C:\\Documentos\\analise_dados\\despesas_seguranca.xlsx")
df

#Primeira analise dos dados
df.shape
df.columns

#variavel independente
X= df["População"]

#variavel dependente
y= df["Valor"]

#Constante
x = sm.add_constant(X)
modelo = sm.OLS(y,X).fit()
print(modelo.summary())



import pandas as pd
import seaborn as sns
import statsmodels.api as sm 
import matplotlib.pyplot as plt

# Importar os dados
df = pd.read_excel("C:\\Documentos\\analise_dados\\despesas_seguranca.xlsx")

# Verificar estrutura dos dados
print(df.shape)
print(df.columns)

# Variável independente (X)
X = df["População"]

# Variável dependente (y)
y = df["Valor"]

# Adicionar constante (intercepto)
X = sm.add_constant(X)

# Estimar o modelo MQO (OLS)
modelo = sm.OLS(y, X).fit()

# Exibir o resumo dos resultados
print(modelo.summary())

sns.regplot(x="População", y="Valor", data=df, ci=None, line_kws={'color':'red'})
plt.title("Relação entre População e Despesa com Segurança")
plt.show()


