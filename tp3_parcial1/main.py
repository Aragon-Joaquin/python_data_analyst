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
df = pd.read_csv('./mock/AllGPUS.csv')
