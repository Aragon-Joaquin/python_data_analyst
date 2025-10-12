#!/usr/bin/env python
#
# TP2 - Aragon Joaquin, Gómez Nicolas Miguel,
#       ,Vazquez Federico. 
# 

import pandas as pd
from pandas.api.types import CategoricalDtype

from colorPrinter import ColorPrint, COLORS

# 2.A)
df = pd.read_csv('./mock/All_GPUs.csv')

# cambiamos los nombres de columna de MAYUSCULA a minuscula
#df.columns = df.columns.str.lower()


ColorPrint(df.head(100), COLORS.RED) # test
# 2.B) estandarizancion de cada columna

transformToString = df[['Architecture', 'Dedicated', 'Best_Resolution', 'Boost_Clock', 'Core_Speed', 'Integrated', 'L2_Cache']]
transformToString = transformToString.astype(str).apply(lambda x: x.str.strip()) #por cada columna, le eliminamos espacios redundantes

df['Best_Resolution'] = df['Best_Resolution'].str.replace(' ', '')
df[['Boost_Clock', 'Core_Speed']] = df[['Boost_Clock', 'Core_Speed']].apply(lambda x: x.str.replace(' MHz', '')) # son todos medidos en MHz

df['Direct_X'] = pd.to_numeric(
    df['Direct_X'].str.replace('DX ', ''),  # medido en DX (redundante)
    errors='coerce'
)

L2_CacheSplit = df['L2_Cache'].str.split('(', n=1, expand=True) # 1024KB(x2) -> ['1024KB', 'x2)']

df['L2_Cache'] = L2_CacheSplit[0].str.strip() \
    .replace('KB','') \
    .astype('Int64', errors='ignore') # '1024KB' -> 1024

df["L2_CacheQuantity"] = L2_CacheSplit[1].str.strip() \
    .str.replace('x', '') \
    .str.replace(')', '') \
    .fillna('1') \
    .astype('Int64', errors='ignore') # 'x2)' -> '2'

df.loc[df['L2_Cache'] == 0, 'L2_CacheQuantity'] = 0 # 0 -> 0 en vez de 1

transformToNumber = df[['DVI_Connection', 'DisplayPort_Connection','HDMI_Connection']]
transformToNumber = transformToNumber.astype('Int8', errors='ignore')

# categories
DEDICATED_YES = "Yes"
DEDICATED_NO = "No"
UNKNOWN = "Unknown"

df[["Dedicated", "Integrated"]] = df[["Dedicated", "Integrated"]].replace({ 
    pd.NA: UNKNOWN, "": UNKNOWN, " ": UNKNOWN
})


df[["Dedicated", "Integrated"]] = df[["Dedicated", "Integrated"]].astype(CategoricalDtype(categories=[DEDICATED_YES, DEDICATED_NO, UNKNOWN]))