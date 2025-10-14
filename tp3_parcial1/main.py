#!/usr/bin/env python
#
# TP2 - Aragon Joaquin, Gómez Nicolas Miguel,
#       Vazquez Federico. 
# 

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from colorPrinter import ColorPrint, COLORS
from parseFields import ParseFields
from descriptiveAnalysis import descriptiveAnalysis

# 2.A)
df = pd.read_csv('./mock/All_GPUs.csv')

# 2.B) estandarizancion de cada columna
dfParsed = ParseFields(df)
# 3) Analisis Descriptivo
descriptiveAnalysis(dfParsed)

# 4)
sns.set_theme()

# 4.A) Histograma simple de una variable numérica.

sns.histplot(
    data = dfParsed,
    x = "Memory_Speed",
    bins = 20,
    alpha = 0.8,
    label = "mem_speed",
)

plt.title("Velocidad de memoria en MHz")
plt.xlabel("Memoria")
plt.ylabel("Cantidad de GPU's")
plt.show()
plt.close()


# 4.B) Histograma superpuesto de dos variables comparables.

sns.histplot(
    data=dfParsed,
    x="Memory_Speed", 
    bins=25,
    alpha=0.6,
    label="Memoria"
)

sns.histplot(
    data=dfParsed, 
    x="Core_Speed", 
    bins=25,
    alpha=0.6,
    label="Ciclos"
)

plt.title("Velocidad de los ciclos del cpu VS la memoria (en MHz)")
plt.xlabel("Ciclos del cpu & memoria")
plt.ylabel("Frecuencia/Cantidad")
plt.legend()
plt.tight_layout()
plt.show()
plt.close()

# 4.C) Boxplot por categoría o mes.

dfParsed['Release_Year'] = dfParsed['Release_Date'].dt.year
mask_anios = (dfParsed['Release_Year'] >= 2007) & (dfParsed['Release_Year'] <= 2020)
df_filtered = dfParsed[mask_anios].copy()

# forzar para que se vea como el año y no como flotante
df_filtered['Release_Year'] = df_filtered['Release_Year'].astype('Int32') 

sns.boxplot(
    data= df_filtered,
    x="Release_Year",
    y="ROPs",
    whis=1.5,
    showfliers=True,
)

plt.title("Variacion de ROPs desde 2007 - 2020")
plt.xlabel("Años")
plt.ylabel("Render Output Units (ROPs)")
plt.tight_layout()
plt.show()
plt.close()

# 4.D) Scatterplot bivariado con una dimensión adicional (color o tamaño).

#debido a que hay un precio con el valor de 14999.0, lo limitamos a 2000
df_filtered_price = dfParsed[dfParsed['Release_Price'] <= 2000]

sns.scatterplot(
    data=df_filtered_price,
    x="Memory",
    y="Boost_Clock",
    hue="Release_Price",
    size="Release_Price",
    alpha=0.8,
)

plt.title("GPU's calidad-precio filtradas por memoria y frecuencia maxima")
plt.xlabel("Memoria total en MB")
plt.ylabel("Frecuencia máxima")
plt.tight_layout()
plt.show()
plt.close()

# 4.E) Heatmap de correlaciones entre 3 o más variables numéricas
corr = dfParsed[['Core_Speed','PSU_W','Memory_Bus','Max_Power']].corr()

plt.figure(figsize=(8, 6))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f", # format to .2 floating value (creo que es)
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    square=True,
)

plt.title("Heatmap de correlaciones.")
plt.tight_layout()
plt.show()
plt.close()

#4.F) Opcional: matriz de dispersión (pairplot) para un subconjunto de variables

sns.pairplot(
    dfParsed[["TMUs", "Texture_Rate", "Open_GL"]].dropna(),
    diag_kind="hist",
    corner=False
)

plt.suptitle("Heatmap de correlaciones.")
plt.tight_layout()
plt.show()
plt.close()