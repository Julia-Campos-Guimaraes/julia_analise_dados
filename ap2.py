import pandas as pd
import seaborn as sns
import statsmodels.api as sm 
import pandas as pd
import matplotlib.pyplot as plt
from linearmodels.iv import IV2SLS
import numpy as np


### Testes 

df= pd.read_excel("C:\\Documentos\\analise_dados\\dados_completos_final.xlsx")
df

#Primeira analise dos dados
df.shape
df.columns

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

# Primeira etapa: regredir Gasto_Seguranca no instrumento e controles
X_first = sm.add_constant(df[['valor_icms', 'População', 'PIB_per_capita']])
y_first = df['Gasto_Seguranca']

first_stage = sm.OLS(y_first, X_first).fit()
print(first_stage.summary())

# Variáveis
y = df['Qtd_Homicidios']            # dependente
endog = df['Gasto_Seguranca']       # endógena
instr = df['valor_icms']        # instrumental
controls = df[['População', 'PIB_per_capita']]

# Adiciona constante
exog = sm.add_constant(controls)


# Modelo 2SLS
iv_model = IV2SLS(
    dependent=y,
    exog=exog,
    endog=endog,
    instruments=instr
).fit(cov_type='robust')

print(iv_model.summary)

#Correlação
df2 = df[["Gasto_Seguranca","PIB_per_capita","Qtd_Homicidios","População"]]
df_numerico = df2.select_dtypes(include = "number")
df_corr = df_numerico.corr()
sns.heatmap(df_corr, annot=True)


# --- 1) Calcular MDE aproximado a partir do SE do coeficiente IV ---
coef = -4.851e-07   # seu coef IV
se = 5.135e-07      # seu SE do coef (do output)
alpha = 0.05
z = 1.96            # z para 95% CI
MDE = z * se
print(f"MDE (95% CI) ≈ {MDE:.3e}")
print(f"Coef estimado = {coef:.3e} (|coef| < MDE? -> {abs(coef) < MDE})")

# --- 2) Rodar IV com LOGs (ajuda escala/heterocedasticidade) ---
df['ln_homicidios'] = np.log(df['Qtd_Homicidios'] + 1)
df['ln_gasto_seg'] = np.log(df['Gasto_Seguranca'] + 1)
df['ln_pop'] = np.log(df['População'])
df['ln_pibpc'] = np.log(df['PIB_per_capita'] + 1)

# instrumento (pode usar log também se fizer sentido)
df['ln_valor_icms'] = np.log(df['valor_icms'] + 1)

y = df['ln_homicidios']
endog = df['ln_gasto_seg']
instr = df['ln_valor_icms']            # ou lista de instrumentos
controls = df[['ln_pop','ln_pibpc']]
exog = sm.add_constant(controls)

iv_log = IV2SLS(dependent=y, exog=exog, endog=endog, instruments=instr).fit(cov_type='robust')
print(iv_log.summary)

# Criar variáveis ao quadrado
df["ln_gasto_seg_quadrado"] = df["ln_gasto_seg"] ** 2
df["ln_valor_icms_quadrado"] = df["ln_valor_icms"] ** 2

# Variáveis
y = df["ln_homicidios"]
endog = df[["ln_gasto_seg", "ln_gasto_seg_quadrado"]]   # duas endógenas
instr = df[["ln_valor_icms", "ln_valor_icms_quadrado"]] # dois instrumentos
controls = df[["ln_pop", "ln_pibpc"]]
exog = sm.add_constant(controls)

# Modelo IV com termos quadráticos
iv_quad = IV2SLS(
    dependent=y,
    exog=exog,
    endog=endog,
    instruments=instr
).fit(cov_type="robust")

print(iv_quad.summary)

# Criar variáveis ao quadrado
df["ln_gasto_seg_quadrado"] = df["ln_gasto_seg"] ** 2
df["ln_valor_icms_quadrado"] = df["ln_valor_icms"] ** 2

# Variáveis
y = df["ln_homicidios"]
endog = df[["ln_gasto_seg", "ln_gasto_seg_quadrado"]]   # duas endógenas
instr = df[["ln_valor_icms", "ln_valor_icms_quadrado"]] # dois instrumentos
controls = df[["ln_pop"]]
exog = sm.add_constant(controls)

# Modelo IV com termos quadráticos
iv_quad = IV2SLS(
    dependent=y,
    exog=exog,
    endog=endog,
    instruments=instr
).fit(cov_type="robust")

print(iv_quad.summary)
