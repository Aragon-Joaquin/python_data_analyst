#!/usr/bin/env python
#
# TP2 - Aragon Joaquin, Gómez Nicolas Miguel,
#       Marraccini Daniel, Vazquez Federico. 
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
ColorPrint(format(f"2.A) NULOS ACTUALES:\n{df.isna().sum()}"), COLORS.CYAN)

#2.B)
df['Age'] = df['Age'].apply(pd.to_numeric, errors='coerce')

valores_remplazables = ["NA", "N/A", "-", "na", "Desconocido"]
df.replace(valores_remplazables, pd.NA, inplace=True)

#2.C)

#todo: reducir boilerplate
edad_mediana = df['Age'].fillna(df['Age'].median())
edad_media = df['Age'].fillna(df['Age'].mean())
edad_std = df['Age'].fillna(df['Age'].std())

edad_por_genero = df.groupby('Gender', dropna=False)['Age'].median()

ColorPrint(format(f"2.C) GENERO PROMEDIADO EN EDAD:\n{edad_por_genero}"), COLORS.CYAN)

#2.D)

ColorPrint(format(f"2.D) EDAD ANTES:\n{df['Age']}"), COLORS.CYAN)

ColorPrint(format(f"2.D) EDAD DESPUES:\n"), COLORS.CYAN)
ColorPrint(format(f"-----MEDIA-----\n               {edad_media}"), COLORS.CYAN)
ColorPrint(format(f"-----MEDIANA-----\n             {edad_mediana}"), COLORS.CYAN)
ColorPrint(format(f"-----DESVIACION ESTANDAR-----\n {edad_std}"), COLORS.CYAN)

#------------------------------------------------------------------------------------------

#3.A)
ColorPrint(format(f"3.A) DUPLICADOS TOTAL:\n{df.duplicated().sum()}"), COLORS.MAGENTA)

#3.B)
ColorPrint(format(f"3.B) DUPLICADOS EN PatientId y AppointmentID:\n{df.duplicated(subset=["PatientId", "AppointmentID"]).sum()}"), COLORS.MAGENTA)

#3.C)
df.drop_duplicates(inplace=True,keep="first")
ColorPrint(format(f"3.C) TRAS BORRAR DUPLICADOS EXACTOS:\n{df.duplicated().sum()} restantes"), COLORS.MAGENTA)
# la razon por la cual eliminamos todos los duplicados excepto los primeros es debido a que pudo haber sido un error de un registro doble.

#------------------------------------------------------------------------------------------

#4.A)

#TODO: REDO THIS!! 
s = df["ScheduledDay"].astype("string").str.strip().str.replace("\u00A0", " ", regex=False)
a = df["AppointmentDay"].astype("string").str.strip().str.replace("\u00A0", " ", regex=False)

formatDate = "ISO8601" #or '%d/%m/%Y', idk

dtScheduled = pd.to_datetime(s, dayfirst=True, errors='coerce', format=formatDate) 
dtAppointment = pd.to_datetime(a, dayfirst=True, errors='coerce', format=formatDate)

maskS = dtScheduled.isna() & s.notna()
dtScheduled = dtScheduled.fillna(pd.to_datetime(s.where(maskS), errors="coerce", utc=True, dayfirst=True, format=formatDate))

maskA = dtAppointment.isna() & a.notna()
dtAppointment = dtAppointment.fillna(pd.to_datetime(s.where(maskA), errors="coerce", utc=True, dayfirst=True, format=formatDate))

#4.B)
df['DiffDays'] = (dtAppointment - dtScheduled).dt.days
ColorPrint(format(f"4.B) COLUMNA DiffDays (AppointmentDay - ScheduledDay):\n{df['DiffDays']}"), COLORS.YELLOW)

#4.C)
df['DiffDays'] = df['DiffDays'].where(df['DiffDays'] >= 0, df['DiffDays'].mean())
ColorPrint(format(f"4.C) VALORES 0 DE DiffDays REEMPLAZADOS POR LA MEDIA :\n{df['DiffDays']}"), COLORS.YELLOW)

#------------------------------------------------------------------------------------------
# La baja cardinalidad se refiere a columnas con pocos valores unicos.

#5.A)
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

df["Gender"] = (df["Gender"].astype("string").str.strip().str.upper())
df["No-show"] = (df["No-show"].astype("string").str.strip().str.upper())

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

#5.B)
gender_categories = CategoricalDtype(categories=[G_ANOTHER, G_FEMALE, G_MALE])
noShow_categories = CategoricalDtype(categories=[NS_NO, NS_YES])

#5.D)
df['DidAttend'] = df['No-show'].map({NS_NO: 0, NS_YES: 1})
ColorPrint(format(f"5.D) COLUMNA 'DidAttend':\n{df["DidAttend"]}"), COLORS.BLUE)

#------------------------------------------------------------------------------------------

#6.A)

df["Age"] = pd.to_numeric(df["Age"], errors="coerce").astype("Int64")
# usa pd.NA en vez de numpy.nan


df["Age"] = df["Age"].fillna(df["Age"].median())

AGE_MIN = 0
AGE_MAX = 120

invalid_ages = ((df['Age'] < AGE_MIN) | (df['Age'] > AGE_MAX)).sum()
ColorPrint(format(f"6.A) EDADES INVALIDAS:\n{invalid_ages}"), COLORS.RED)

#6.B)
ColorPrint(format(f"6.B)\n> 'Gender' CANTIDAD DE DATOS INVALIDOS:\n{df["Gender"].nunique()} VALORES UNICOS"), COLORS.RED)
ColorPrint(df["Gender"].value_counts(), COLORS.RED)

ColorPrint(format(f"> 'No-show' CANTIDAD DE DATOS INVALIDOS:\n{df["No-show"].nunique()} VALORES UNICOS"), COLORS.RED)
ColorPrint(df["No-show"].value_counts(), COLORS.RED)

#6.C)

#------------------------------------------------------------------------------------------

#7.A)

#IQR (Q3 ​ −Q1) es el rango entre el primer quartil (25%) y el tercer cuartil (75%)
#los outliers (valor atipico) son aquellos que no encajan por debajo de:
# Q1 - 1.5 x IQR
# o por arriba de:
# Q3 + 1.5 * IQR

def showAtipicos(df): 
    quartil_1 = df.quantile(0.25)
    quartil_3 = df.quantile(0.75)
    IQR = quartil_3 - quartil_1

    limite_menor = quartil_1 - 1.5 * IQR
    limite_mayor = quartil_3 + 1.5 * IQR

    return (df < limite_menor) | (df > limite_mayor)    

fig, ax = plt.subplots()
ax.boxplot(df['Age'][showAtipicos(df["Age"])])
ax.set_title('Age Outliers')
ax.set_ylabel('Edades')

plt.show()

# Winsorizar: 
# reemplaza los valores extremos (los mas altos y los mas bajos) por valores menos extremos
df["AgeWinzor"] = df['Age'].clip(lower= df['Age'].quantile(0.05), upper=df['Age'].quantile(0.95))

ColorPrint(format(f"7.C)\n> DATOS 'Age' WINSORIZADOS:"), COLORS.CYAN )
ColorPrint(format(f"NO WINSORIZADOS: {df['Age'].min()}MIN, {df['Age'].max()}MAX"), COLORS.CYAN )
ColorPrint(format(f"WINSORIZADOS: {df['AgeWinzor'].min()}MIN, {df['AgeWinzor'].max()}MAX"), COLORS.CYAN )


fig, ax = plt.subplots()
ax.boxplot(df['DiffDays'][showAtipicos(df["DiffDays"])])
ax.set_title('DiffDays Outliers')
ax.set_ylabel('Diferencia de dias')

plt.show()

#excluimos los outliers
df['DaysDeleted'] = df["DiffDays"][(df["DiffDays"] < df['DiffDays'].quantile(0.95)) & (df["DiffDays"] > df["DiffDays"].quantile(0.05))]

ColorPrint(format(f"> DATOS 'DiffDays' ELIMINADOS/EXCLUIDOS:"), COLORS.CYAN )
ColorPrint(format(f"NO ELIMINADOS: {df['DiffDays'].min()}MIN, {df['DiffDays'].max()}MAX"), COLORS.CYAN )
ColorPrint(format(f"ELIMINADOS/EXCLUIDOS: {df['DaysDeleted'].min()}MIN, {df['DaysDeleted'].max()}MAX"), COLORS.CYAN )
