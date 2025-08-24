#
# TP1 - Aragon Joaquin
# 

import pandas as pd
import matplotlib.pyplot as plt

from colorPrinter import ColorPrint, COLORS

# 1)
dtSet = pd.read_csv('./mock/dataset2.csv') # leemos el .csv desde mocks

# 1.5) Transformamos a sus respectivos tipos

dtSet[['Ingresos', 'Edad']] = dtSet[['Ingresos', 'Edad']].apply(pd.to_numeric, errors='coerce')  # transformamos campo a numero para luego ordernalo y suprimimos erorres
dtSet = dtSet.astype({"Nombre": str, "Ciudad": str, "Ocupacion": str})

# 2)
ColorPrint(dtSet.head(4), COLORS.GREEN) # primeras 4 filas printeadas

ColorPrint(dtSet.info(), COLORS.GREEN) # printea el informacion sobre el DataSet (no nulos, tipo de dato, columna)

ColorPrint(format(f"Filas x Columnas: {dtSet.shape}"), COLORS.GREEN) #printea dimensiones

ColorPrint(format(f" Descripcion:\n{dtSet.describe()}"), COLORS.GREEN) #printea descripcion general (min, max, standard, media, etc...)

# 3)
ColorPrint(format(f"3.1) DETECTAR NULOS POR CAMPO:\n{dtSet.isnull().sum()}"), COLORS.RED) # printea true si el campo es nulo

edadMedia = round(dtSet["Edad"].mean()) # agarramos la media y la redondeamos
ingresoMedia = round(dtSet["Ingresos"].mean()) # x2 aca

# dtSet["Ingresos"].fillna(0, inplace = True) #cambiamos ingresos a 0 modificando el dataSet Previo (inplace=true)
# dtSet["Edad"].fillna(0, inplace = True) #mismo para edad
dtSet.fillna({"Ingresos": ingresoMedia, "Edad": edadMedia}, inplace=True) # pero mejor en una sola linea! (y haciendolo con la media!)

ColorPrint(format(f"3.2) RELLENAR VALORES nan!:\n{dtSet}"), COLORS.RED)

# 5) (cambie de orden con el 4 por inconsistencias de 0 y "?")

# Linea de abajo es irrelevante debido a que no existen datos "?" / "desconocido" por la conversion del punto 1.5 (aunque con errors="ignore" si se podria llegar a este caso, pero por el bien de no añadir complejidad innecesaria, sera de esta forma)

#dtSet.replace({"Ingresos": "?", "Edad": "desconocido" }, {"Ingresos": ingresoMedia, "Edad": edadMedia}, inplace=True)
#ColorPrint(format(f"4) REEMPLAZAR INCOSISTENCIAS '?' Y 'desconocido'!:\n{dtSet}"), COLORS.CYAN)

ColorPrint(f"4.1) NUMERO DE VALORES NULOS EN LOS CAMPOS STR: \n",df[['Nombre','Ciudad','Ocupacion']].isnull().sum()) 

# df["Nombre"].replace('nan', 'Anonimo')
# df["Ciudad"].replace('nan', 'Desconocido')
# df["Ocupacion"].replace('nan', 'Desconocido')

df.replace({'Nombre': {pd.NA: 'Anonimo'}, 'Ciudad': {pd.NA: 'Desconocido'}, 'Ocupacion': {pd.NA: 'Desconocido'}}, inplace=True) #equivalente al bloque anterior
ColorPrint(f"4.1) NUMERO DE VALORES LUEGO DE REEMPLAZAR NULOS: \n",df[['Nombre','Ciudad','Ocupacion']].isnull().sum()) 

# 4)

prevDups = dtSet.duplicated().sum()
dtSet.drop_duplicates(inplace=True) # modificamos el dataset
ColorPrint(format(f"5) BORRAR DUPLICADOS!:\n{prevDups} han sido borrados"), COLORS.YELLOW)


# 6)
ColorPrint(format(f"6) ANALISIS DESCRIPTIVO:\n{dtSet.describe()}"), COLORS.MAGENTA) #analisis descriptivo

# 7) 

#  WARNING: 
# Es posible que no funcione
# https://stackoverflow.com/questions/77507580/userwarning-figurecanvasagg-is-non-interactive-and-thus-cannot-be-shown-plt-sh
# SOLUCION: pip install PyQt6... y tener python 3.12+

# 7.1) grafico de barras 
dtIngresos = dtSet.sort_values('Ingresos', ascending=True)

plt.bar(dtIngresos['Nombre'], dtIngresos['Ingresos'], color='red')
plt.xlabel("Nombre", size=12)
plt.ylabel("Ingresos", size=12)
plt.title("Ingresos por persona", size=16)
plt.grid(True)
plt.show()

# # 7.2) grafico de esparcimiento 
plt.scatter(dtSet['Ocupacion'],dtSet['Edad'])
plt.xlabel("Ocupacion", size=12)
plt.ylabel("Edad", size=12)
plt.title("Edad por Ocupacion", size=16)
plt.grid(True)
plt.show()

# 7.3) grafico circular (pie chart)
names = []
timeAppeared = []

for name, count in dtSet['Nombre'].value_counts().items():
    names.append(name)
    timeAppeared.append(count)

fig, ax = plt.subplots()
ax.pie(timeAppeared, labels=names, autopct='%1.1f%%')
ax.set_title('Porcentaje de aparecimiento de nombres', size=16)
plt.show()
