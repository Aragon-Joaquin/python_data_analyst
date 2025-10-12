#!/usr/bin/env python
#
# TP2 - Aragon Joaquin, Gómez Nicolas Miguel,
#       Vazquez Federico. 
# 

import pandas as pd
from pandas.api.types import CategoricalDtype

from colorPrinter import ColorPrint, COLORS
from parseFields import ParseFields

# 2.A)
df = pd.read_csv('./mock/All_GPUs.csv')

ColorPrint(df.head(100), COLORS.RED) # test

# 2.B) estandarizancion de cada columna
dfParsed = ParseFields(df)
print(dfParsed.info())