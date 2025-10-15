import pandas as pd
from colorPrinter import ColorPrint, COLORS

def descriptiveAnalysis(df_parsed):
    selected_columns = [
        'Core_Speed',
        'Boost_Clock',
        'Shader',
        'Release_Price',
        'Process'
    ]

    ColorPrint("Análisis Descriptivo de Características Seleccionadas de GPUs", COLORS.MAGENTA)
    ColorPrint("="*50, COLORS.MAGENTA)

    for col in selected_columns:
        ColorPrint(f"--- Análisis para: {col} ---", COLORS.CYAN)
        
        desc_stats = df_parsed[col].describe()
        col_range = df_parsed[col].max() - df_parsed[col].min()
        
        ColorPrint("Medidas de Tendencia Central:", COLORS.YELLOW)
        ColorPrint(f"  Media: {desc_stats['mean']:.2f}", COLORS.GREEN)
        ColorPrint(f"  Mediana: {desc_stats['50%']:.2f}", COLORS.GREEN)
        
        ColorPrint("Medidas de Dispersión:", COLORS.YELLOW)
        ColorPrint(f"  Desviación Estándar: {desc_stats['std']:.2f}", COLORS.GREEN)
        ColorPrint(f"  Rango: {col_range:.2f}", COLORS.GREEN)
        
        ColorPrint("Medidas de Posición:", COLORS.YELLOW)
        ColorPrint(f"  Mínimo: {desc_stats['min']:.2f}", COLORS.GREEN)
        ColorPrint(f"  Percentil 25 (Q1): {desc_stats['25%']:.2f}", COLORS.GREEN)
        ColorPrint(f"  Percentil 75 (Q3): {desc_stats['75%']:.2f}", COLORS.GREEN)
        ColorPrint(f"  Máximo: {desc_stats['max']:.2f}", COLORS.GREEN)

'''
    En el ejemplo de "Core_Speed", las siguientes medidas pueden ser intrepretadas de la siguiente manera:

    - Media: Nos ayuda a promediar cual va a ser el valor mas probable de la velocidad del Nucleo
    - Mediana: De todos los valores, selecciona el intermedio logrando que separe la mitad superior
        de la inferior. Devolviendo la tendencia central de la velocidad del Nucleo
    
    - Desviación estándar: Mide si los valores tienen valores similares o si diferen mucho de uno y otro.
        Mientras mas alta la Desviacion, entonces mas disperso estaran los datos
    - Rango: Indica la diferencia entre el valor maximo y el valor menor de los datos

    - Mínimo: El valor con menor velocidad de nucleo
    - Máximo: El valor con mayor velocidad de nucleo
    - Cuartiles: Divide los datos en 4 partes (25, 50%, 75 y 100%), suele indicar la variacion de datos
        En este caso, diferencia entre gpus lentos (Q1) y gpus rapidos (Q3) y nos permite ver en cuanto diferen
'''