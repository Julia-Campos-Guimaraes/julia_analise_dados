import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = sns.load_dataset("tips")

#Histograma
sns.histplot(data=df, x = "total_bill")

#Boxplot
sns.boxplot(data=df, x = "total_bill")

#Correlação
df_numerico = df.select_dtypes(include = "number")
df_corr = df_numerico.corr()
sns.heatmap(df_corr, annot=True)

#Linha
sns.lineplot(data=df, x = "day", y= "tip")

#Barra
sns.barplot(data=df, x = "day", y= "tip")
sns.countplot(data=df, x = "day", hue = "sex")