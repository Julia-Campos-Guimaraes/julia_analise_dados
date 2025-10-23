import seaborn as sns
import statsmodels.api as sm 
import pandas as pd
import matplotlib.pyplot as plt

#Dataset de gorjetas 

df = sns.load_dataset("tips")
df.head()
df["time"].unique()
df["day"].unique()

#Regressão linear Simples

#variavel independente
X= df["total_bill"]

#variavel dependente
y= df["tip"]

#Constante
x = sm.add_constant(X)
modelo = sm.OLS(y,X).fit()
print(modelo.summary())

# Regressão linear multipla

#variavel independente
X= df[["total_bill", "size"]]

#variavel dependente
y= df["tip"]

#Constante
x = sm.add_constant(X)
modelo = sm.OLS(y,X).fit()
print(modelo.summary())

modelo.params
modelo.pvalues
modelo.rsquared
modelo.rsquared_adj

#Previsao do modelo 
pred = modelo.predict()
comparacao = pd.DataFrame({
    "real": df["tip"],
    "calculada": pred
})
comparacao["residuos"] = comparacao["real"] - comparacao["calculada"]
sns.scatterplot(x=modelo.predict(), y=comparacao["residuos"])
plt.axhline(0,color = "red", linestyle="--")
