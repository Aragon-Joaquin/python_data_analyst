#!/usr/bin/env python
#
# TP2 - Aragon Joaquin, Gómez Nicolas Miguel,
#       Vazquez Federico. 
# 

import pandas as pd

from colorPrinter import ColorPrint, COLORS
from parseFields import ParseFields
from descriptiveAnalysis import descriptiveAnalysis

# 2.A)
df = pd.read_csv('./mock/All_GPUs.csv')

# 2.B) estandarizancion de cada columna
dfParsed = ParseFields(df)
# 3) Analisis Descriptivo
descriptiveAnalysis(dfParsed)
