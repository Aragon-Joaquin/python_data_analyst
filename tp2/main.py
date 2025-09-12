#!/usr/bin/env python
#
# TP2 - Aragon Joaquin, Gómez Nicolas Miguel,
#       Marraccini Daniel, Vazquez Federico. 
# 

import pandas as pd
# import matplotlib.pyplot as plt

from colorPrinter import ColorPrint, COLORS

# 1.A)
df = pd.read_csv('./mock/DatasetClase3_corrupto.csv', low_memory=False)
# lowMemory usará mas memoria y cargará el archivo completo en vez de chunks con el beneficio de no mezclar las inferencias de tipos

# 1.B)
ColorPrint(format(f"1.B) FILAS x COLUMNAS:\n{df.shape}"), COLORS.GREEN)

ColorPrint(format(f"1.B) INFORMACION DEL DATAFRAME:\n{df.info()}"), COLORS.GREEN)

ColorPrint(format(f"1.B) DESCRIPCION DEL DATAFRAME:\n{df.describe()}"), COLORS.GREEN)

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

#improve this later :/
s = df["ScheduledDay"].astype("string").str.strip().str.replace("\u00A0", " ", regex=False)
a = df["AppointmentDay"].astype("string").str.strip().str.replace("\u00A0", " ", regex=False)

dtScheduled = pd.to_datetime(s, dayfirst=True, errors='coerce', format="ISO8601") 
dtAppointment = pd.to_datetime(a, dayfirst=True, errors='coerce', format="ISO8601")

maskS = dtScheduled.isna() & s.notna()
dtScheduled = dtScheduled.fillna(pd.to_datetime(s.where(maskS), errors="coerce", utc=True, dayfirst=True))

maskA = dtAppointment.isna() & a.notna()
dtAppointment = dtAppointment.fillna(pd.to_datetime(s.where(maskA), errors="coerce", utc=True, dayfirst=True))

#4.B)
df['DiffDays'] = (dtAppointment - dtScheduled).dt.days
ColorPrint(format(f"4.B) COLUMNA DiffDays (AppointmentDay - ScheduledDay):\n{df['DiffDays']}"), COLORS.YELLOW)

#4.C)
df['DiffDays'] = df['DiffDays'].where(df['DiffDays'] >= 0, df['DiffDays'].mean())
ColorPrint(format(f"4.B) VALORES 0 DE DiffDays REEMPLAZADOS POR LA MEDIA :\n{df['DiffDays']}"), COLORS.YELLOW)

#------------------------------------------------------------------------------------------
