#
# TP1 - Aragon Joaquin, Gómez Nicolas Miguel,
#       Marraccini Daniel, Vazquez Federico. 
# 

import pandas as pd
import matplotlib.pyplot as plt

from colorPrinter import ColorPrint, COLORS

# 1)
dtSet = pd.read_csv('./mock/dataset2.csv') # leemos el .csv desde mocks

# 2)
ColorPrint(dtSet.head(4), COLORS.GREEN) # primeras 4 filas printeada

ColorPrint(dtSet.info(), COLORS.GREEN) # printea el informacion sobre el DataSet (no nulos, tipo de dato, columna)

ColorPrint(format(f"Filas x Columnas: {dtSet.shape}"), COLORS.GREEN) #printea dimensiones

ColorPrint(format(f" Descripcion:\n{dtSet.describe()}"), COLORS.GREEN) #printea descripcion general (min, max, standard, media, etc...)

#2.5) Transformamos a sus respectivos tipos
dtSet[['Ingresos', 'Edad']] = dtSet[['Ingresos', 'Edad']].apply(pd.to_numeric, errors='coerce')  # transformamos campo a numero para luego ordernalo y suprimimos erorres
dtSet = dtSet.astype({"Nombre": str, "Ciudad": str, "Ocupacion": str})

# 3)
ColorPrint(format(f"3.1) DETECTAR NULOS POR CAMPO:\n{dtSet.isnull().sum()}"), COLORS.RED) # printea true si el campo es nulo

edadMedia = dtSet["Edad"].mean() # calculamos la media de edad
ingresoMediana = dtSet["Ingresos"].median() #calculamos la mediana de ingresos

dtSet.fillna({"Ingresos": ingresoMediana, "Edad": edadMedia}, inplace=True) #usando la media y mediana respectivamente

ColorPrint(format(f"3.2) RELLENAR VALORES nan!:\n{dtSet}"), COLORS.RED)

# 4)
prevDups = dtSet.duplicated().sum()
dtSet.drop_duplicates(inplace=True) # modificamos el dataset
ColorPrint(format(f"4) BORRAR DUPLICADOS!:\n{prevDups} han sido borrados"), COLORS.YELLOW)

# 5) 
ColorPrint(format(f"5.1) NUMERO DE VALORES NULOS EN LOS CAMPOS STR: \n{dtSet[['Nombre','Ciudad','Ocupacion']].isnull().sum()}"), COLORS.RED) 

# dtSet["Nombre"].replace('nan', 'Anonimo')
# dtSet["Ciudad"].replace('nan', 'Desconocido')
# dtSet["Ocupacion"].replace('nan', 'Desconocido')


dtSet.replace({'Nombre': {pd.NA: 'Anonimo'}, 'Ciudad': {pd.NA: 'Desconocido'}, 'Ocupacion': {pd.NA: 'Desconocido'}}, inplace=True) #equivalente al bloque anterior
ColorPrint(format(f"5.1) NUMERO DE VALORES LUEGO DE REEMPLAZAR NULOS: \n{dtSet[['Nombre','Ciudad','Ocupacion']].isnull().sum()}"), COLORS.RED) 


# 6)
ColorPrint(format(f"6) ANALISIS DESCRIPTIVO:\n{dtSet.describe()}"), COLORS.MAGENTA) #analisis descriptivo

# 7) 
# 7.1) grafico de barras 
dtProm = dtSet.groupby('Nombre')['Ingresos'].mean().reset_index() # agrupamos por nombre y calculamos la media de sus ingresos, reseteamos el index para que quede prolijo
dtProm.sort_values('Ingresos', ascending=True, inplace=True) # reescribrimos en dtProm y ordenamos desde menor a mayor

plt.bar(dtProm['Nombre'], dtProm['Ingresos'], color='red')
plt.xlabel("Nombre", size=12)
plt.ylabel("Ingresos", size=12)
plt.title("Ingresos por persona", size=16)
plt.grid(True)
plt.show()

# # 7.2) Grafico de esparcimiento 
plt.scatter(dtSet['Ocupacion'],dtSet['Edad'])
plt.xlabel("Ocupacion", size=12)
plt.ylabel("Edad", size=12)
plt.title("Edad por Ocupacion", size=16)
plt.grid(True)
plt.show()

# 7.3) Grafico circular (pie chart)
names = []
timeAppeared = []

for name, count in dtSet['Nombre'].value_counts().items():
    names.append(name)
    timeAppeared.append(count)

fig, ax = plt.subplots()
ax.pie(timeAppeared, labels=names, autopct='%1.1f%%')
ax.set_title('Porcentaje de aparicion de nombres', size=16)
plt.show()