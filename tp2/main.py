#!/usr/bin/env python
#
# TP2 - Aragon Joaquin, Gómez Nicolas Miguel,
#       ,Vazquez Federico. 
# 

import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt

from colorPrinter import ColorPrint, COLORS

# 1.A)
df = pd.read_csv('./mock/DatasetClase3_corrupto.csv', low_memory=False)
# lowMemory usará mas memoria y cargará el archivo completo en vez de chunks con el beneficio de no mezclar las inferencias de tipos

# 1.B)
ColorPrint(format(f"1.B)\n> FILAS x COLUMNAS:\n{df.shape}"), COLORS.GREEN)

ColorPrint(format(f"> INFORMACION DEL DATAFRAME:\n{df.info()}"), COLORS.GREEN)

ColorPrint(format(f"> DESCRIPCION DEL DATAFRAME:\n{df.describe()}"), COLORS.GREEN)

# 1.C)
ColorPrint(format(f"1.C) DATOS INFERIDOS DEL DATAFRAME:\n{df.dtypes}"), COLORS.GREEN)

#------------------------------------------------------------------------------------------

#2.A)
# cantidad de nulos que hay en el dataFrame
ColorPrint(format(f"2.A) NULOS ACTUALES:\n{df.isna().sum()}"), COLORS.CYAN)

#2.B)
#transformamos las edades a numericos
df['Age'] = df['Age'].apply(pd.to_numeric, errors='coerce')

#a las edades que dieron error porque eran string, reemplazamos su valor por el nulo de Pandas
valores_remplazables = ["NA", "N/A", "-", "na", "Desconocido"]
df.replace(valores_remplazables, pd.NA, inplace=True)

#2.C)
#seleccionamos todas las edades y la agrupamos por cada genero diferente 
# para luego calcular la media de edad por genero
edad_por_genero = df.groupby('Gender', dropna=False)['Age']

ColorPrint(format(f"2.C)\n> GENERO PROMEDIADO EN EDAD:\n{edad_por_genero.median()}"), COLORS.CYAN)

#2.D)
def fillAge(operation):
    return edad_por_genero.fillna(operation)

ColorPrint(format(f"2.D) EDAD POR GENERO ANTES:\n{df['Age']}"), COLORS.CYAN)

ColorPrint(format(f"2.D) EDAD POR GENERO DESPUES:\n"), COLORS.CYAN)
ColorPrint(format(f"-----MEDIA-----\n               {fillAge(df['Age'].mean())}"), COLORS.CYAN)
ColorPrint(format(f"-----MEDIANA-----\n             {fillAge(df['Age'].median())}"), COLORS.CYAN)
ColorPrint(format(f"-----DESVIACION ESTANDAR-----\n {fillAge(df['Age'].std())}"), COLORS.CYAN)

#------------------------------------------------------------------------------------------

#3.A)
# la suma de duplicados actuales
ColorPrint(format(f"3.A) DUPLICADOS TOTAL:\n{df.duplicated().sum()}"), COLORS.MAGENTA)

#3.B)
#seleccionamos los duplicados de PatientId y AppointmentID y lo sumamos
ColorPrint(format(f"3.B) DUPLICADOS EN PatientId y AppointmentID:\n{df.duplicated(subset=["PatientId", "AppointmentID"]).sum()}"), COLORS.MAGENTA)

#3.C)
# la razon por la cual eliminamos todos los duplicados excepto los primeros es debido a que pudo haber sido un error de un registro doble.
df.drop_duplicates(inplace=True,keep="first")
ColorPrint(format(f"3.C) TRAS BORRAR DUPLICADOS EXACTOS:\n{df.duplicated().sum()} restantes"), COLORS.MAGENTA)


#------------------------------------------------------------------------------------------

#4.A)
#indicamos el tipo de fecha que usaremos para parsear los datos, esta fecha seria algo asi: 30/12/2025
formatDate = '%d/%m/%Y' #o "ISO8601"

# definimos una funcion para ahorrarnos repetir lineas
def transformToDate(dtName):
    strippedDays = dtName.astype("string").str.strip().str.replace("\u00A0", " ", regex=False)
    dt = pd.to_datetime(strippedDays, errors="coerce", dayfirst=True, format="ISO8601").dt.tz_localize(None)
    dt2 = pd.to_datetime(strippedDays.where(dt.isna()), errors="coerce", format=formatDate, dayfirst=True).dt.tz_localize(None)
    return dt.fillna(dt2)

dtScheduled = transformToDate(df["ScheduledDay"])
dtAppointment = transformToDate(df["AppointmentDay"])
dtFechaLibre = transformToDate(df["FechaLibre"])

ColorPrint(format(f"4.A)\n>COLUMNA ScheduledDay PARSEADA:\n{dtScheduled}"), COLORS.YELLOW)
ColorPrint(format(f"COLUMNA AppointmentDay PARSEADA:\n{dtAppointment}"), COLORS.YELLOW)
ColorPrint(format(f"COLUMNA FechaLibre PARSEADA:\n{dtFechaLibre}"), COLORS.YELLOW)

#4.B)
# obtenemos la diferencia de dias
df['DiffDays'] = (dtAppointment - dtScheduled).dt.days
ColorPrint(format(f"4.B) COLUMNA DiffDays (AppointmentDay - ScheduledDay):\n{df['DiffDays']}"), COLORS.YELLOW)

#4.C)
# reemplazamos la diferencia de dias menor a 0 por su media 
mediana_diffDays = df['DiffDays'].where(df['DiffDays'] >= 0).mean()
df['DiffDays'] = df['DiffDays'].where(df['DiffDays'] >= 0, mediana_diffDays)
ColorPrint(format(f"4.C) VALORES 0 DE DiffDays REEMPLAZADOS POR LA MEDIA :\n{df['DiffDays']}"), COLORS.YELLOW)

#------------------------------------------------------------------------------------------
# La baja cardinalidad se refiere a columnas con pocos valores unicos.

#5.A)
#imprimimos en pantalla los valores unicos de cada columna antes de parsearlos
ColorPrint(format(f"5.A)\n> 'Gender' CARDINALIDAD :\n{df["Gender"].nunique()} VALORES UNICOS"), COLORS.BLUE)
ColorPrint(format(f"> 'No-Show' CARDINALIDAD :\n{df["No-show"].nunique()} VALORES UNICOS"), COLORS.BLUE)

#5.C)
#variables para genero
G_MALE = "M"
G_FEMALE = "F"
G_ANOTHER = "OTRO"

UNKNOWN = "DESCONOCIDO"

#variables para No-Show
NS_YES = "SI"
NS_NO = "NO"

#variables para estado-turno
ET_PROGRAMMED = "PROGRAMADO"
ET_ATTENDED = "ATENDIDO"
ET_PENDING = "PENDIENTE"
ET_CANCELLED = "CANCELADO"
ET_REPROGRAM = "REPROGRAMADO"

#eliminamos espacios en blanco del principio y fin y ponemos todos los valores en mayuscula
df["Gender"] = (df["Gender"].astype("string").str.strip().str.upper())
df["No-show"] = (df["No-show"].astype("string").str.strip().str.upper())
df["EstadoTurno"] = (df["EstadoTurno"].astype("string").str.strip().str.upper())

#reemplazamos posibles valores incorrectos por nuestras variables 
df["Gender"] = df["Gender"].replace({
    "FEM":G_FEMALE, "FEMALE": G_FEMALE ,"FEMENINO": G_FEMALE, "MUJER": G_FEMALE,
    "MASC": G_MALE, "MALE": G_MALE, "MASCULINO": G_MALE, "HOMBRE": G_MALE,
    "OTHER": G_ANOTHER, 
    pd.NA: UNKNOWN, "": UNKNOWN, " ": UNKNOWN
})

df["No-show"] = df["No-show"].replace({
    "0": NS_NO, "N": NS_NO, "FALSE": NS_NO,
    "1": NS_YES, "Y": NS_YES, "TRUE": NS_YES, "YES": NS_YES,

    pd.NA: UNKNOWN, "": UNKNOWN, " ": UNKNOWN
})

df["EstadoTurno"] = df["EstadoTurno"].replace({
    pd.NA: UNKNOWN, "X": UNKNOWN, "??": UNKNOWN
})

#5.B)
#indica que solo dicha columna puede tener esos valores
gender_categories = CategoricalDtype(categories=[G_ANOTHER, G_FEMALE, G_MALE, UNKNOWN])
noShow_categories = CategoricalDtype(categories=[NS_NO, NS_YES, UNKNOWN])
estadoTurno_categories = CategoricalDtype(categories=[ET_PROGRAMMED, ET_ATTENDED, ET_PENDING,ET_CANCELLED,ET_REPROGRAM,UNKNOWN])

df["Gender"] = df["Gender"].astype(gender_categories)
df["No-show"] = df["No-show"].astype(noShow_categories)
df["EstadoTurno"] = df["EstadoTurno"].astype(estadoTurno_categories)

ColorPrint(format(f">5.B)\n COLUMNA 'Gender' EN CATEGORIA:\n{df["Gender"]}"), COLORS.BLUE)
ColorPrint(format(f"COLUMNA 'No-show' EN CATEGORIA:\n{df["No-show"]}"), COLORS.BLUE)
ColorPrint(format(f"COLUMNA 'EstadoTurno' EN CATEGORIA:\n{df["EstadoTurno"]}"), COLORS.BLUE)

#5.D)
df['DidAttend'] = df['No-show'].map({NS_NO: 0, NS_YES: 1})
ColorPrint(format(f"5.D) COLUMNA 'DidAttend':\n{df["DidAttend"]}"), COLORS.BLUE)

#------------------------------------------------------------------------------------------

#6.A)

# Int64 usa pd.NA en vez de numpy.nan
df["Age"] = pd.to_numeric(df["Age"], errors="coerce").astype("Int64")


# los valores nulos ahora seran la media
df["Age"] = df["Age"].fillna(df["Age"].median())

AGE_MIN = 0
AGE_MAX = 120

# seleccionamos las edades menores a 0 y mayor a 120 y sumamos su cantidad total
invalid_ages = ((df['Age'] < AGE_MIN) | (df['Age'] > AGE_MAX)).sum()
ColorPrint(format(f"6.A) EDADES INVALIDAS:\n{invalid_ages}"), COLORS.RED)

#6.B)
gender_invalids = df["Gender"].isna().sum()
ColorPrint(format(f"6.B)\n> 'Gender' CANTIDAD DE DATOS INVALIDOS:\n{gender_invalids}"), COLORS.RED)

noshow_invalids = df["No-show"].isna().sum()
ColorPrint(format(f"> 'No-show' CANTIDAD DE DATOS INVALIDOS:\n {noshow_invalids}"), COLORS.RED)

#6.C)
#rellenamos los valores nulos con el valor "Desconocido" que anteriormente habiamos declarado
df["Gender"] = df["Gender"].fillna(UNKNOWN)
df["No-show"] = df["No-show"].fillna(UNKNOWN)

#eliminamos las edades invalidas
df["Age"] = df["Age"].clip(lower=AGE_MIN, upper=AGE_MAX)

ColorPrint(format(f"6.C)\n> 'Gender' CANTIDAD DE VALORES UNICOS:\n{df["Gender"].nunique()}"), COLORS.RED)
ColorPrint(format(f"> 'No-show' CANTIDAD DE VALORES UNICOS:\n{df["No-show"].nunique()}"), COLORS.RED)
ColorPrint(format(f"> ELIMINAMOS 'Age' INVALIDOS:\n{df["Age"].min()}MIN, {df["Age"].max()}MAX "), COLORS.RED)

#------------------------------------------------------------------------------------------

#7.A)

#IQR (Q3 ​ −Q1) es el rango entre el primer quartil (25%) y el tercer cuartil (75%)
#los outliers (valor atipico) son aquellos que no encajan por debajo de:
# Q1 - 1.5 x IQR
# o por arriba de:
# Q3 + 1.5 * IQR

def showAtipicos(df): 
    #calculamos el 25% y el 75% + el IQR 
    quartil_1 = df.quantile(0.25)
    quartil_3 = df.quantile(0.75)
    IQR = quartil_3 - quartil_1
    
    #definimos nuestros limites
    limite_menor = float(quartil_1 - 1.5 * IQR)
    limite_mayor = float(quartil_3 + 1.5 * IQR)

    
    #enmascaramos los valores que son menores al limite menor y mayores al limite mayor
    # es decir, solo los valores invalidos
    outliers_mask = (df < limite_menor) | (df > limite_mayor)

    return outliers_mask, limite_menor, limite_mayor   

fig, ax = plt.subplots()


ageAtipicos, AgeLMenor, AgeLMayor = showAtipicos(df["Age"])

ax.boxplot(df['Age'][ageAtipicos])
ax.set_title('Age Outliers')
ax.set_ylabel('Edades')

plt.show()

# Winsorizar: 
# reemplaza los valores extremos (los mas altos y los mas bajos) por valores menos extremos
df["AgeWinzor"] = df['Age'].clip(lower=AgeLMenor, upper=AgeLMayor)

ColorPrint(format(f"7.C)\n> DATOS 'Age' WINSORIZADOS:"), COLORS.CYAN )

# mostramos los valores mas bajos y altos ANTES y DESPUES de winsorizar
ColorPrint(format(f"NO WINSORIZADOS: {df['Age'].min()}MIN, {df['Age'].max()}MAX"), COLORS.CYAN )
ColorPrint(format(f"WINSORIZADOS: {df['AgeWinzor'].min()}MIN, {df['AgeWinzor'].max()}MAX"), COLORS.CYAN )


#hacemos lo mismo pero con DiffDays
daysAtipicos, daysLMenor, daysLMayor = showAtipicos(df["DiffDays"])

fig, ax = plt.subplots()
ax.boxplot(df['DiffDays'][daysAtipicos])
ax.set_title('DiffDays Outliers')
ax.set_ylabel('Diferencia de dias')

plt.show()

#excluimos los outliers
mask_noeliminados = (df["DiffDays"] < daysLMayor) & (df["DiffDays"] > daysLMenor)

# days deleted dará NaN debido a la cantidad de numeros de similar valor
# eso afectara que los cuartiles sean identicos
df["DaysDeleted"] = df["DiffDays"].where(mask_noeliminados)

ColorPrint(format(f"> DATOS 'DiffDays' ELIMINADOS/EXCLUIDOS:"), COLORS.CYAN )
ColorPrint(format(f"NO ELIMINADOS: {df['DiffDays'].min()}MIN, {df['DiffDays'].max()}MAX"), COLORS.CYAN )
ColorPrint(format(f"ELIMINADOS/EXCLUIDOS: {df['DaysDeleted'].min()}MIN, {df['DaysDeleted'].max()}MAX"), COLORS.CYAN )

#------------------------------------------------------------------------------------------

#8.A)
edad_promedio = df.groupby("Gender", as_index=False)['Age'].mean()
edad_mediana = df.groupby("Gender", as_index=False)['Age'].median()

ColorPrint(format(f"8.A)\n> EdadPromedia: {edad_promedio}"), COLORS.YELLOW )
ColorPrint(format(f"> EdadMedia: {edad_mediana}"), COLORS.YELLOW )

#8.B)

tiempo_espera = df.groupby('DidAttend')['DiffDays'].mean()

ColorPrint(format(f"8.B)\n> Tiempo de espera promedio: {tiempo_espera}"), COLORS.YELLOW )

#8.C)
#agrupamos las edades por cada estado de turno diferente y obtenemos los siguientes valores:
# - cuantos datos hay en total
# - cuantos datos son unicos
# - el dato menor
# - el dato mayor
res = df.groupby('EstadoTurno')['Age'].agg(["count", "nunique", "min", "max"])
ColorPrint(format(f"8.C)\n> metodo Aggregation de pandas: {res}"), COLORS.YELLOW )