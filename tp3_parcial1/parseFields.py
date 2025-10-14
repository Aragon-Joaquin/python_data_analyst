import pandas as pd
from pandas.api.types import CategoricalDtype

def ParseFields(dataFrame):
    df = dataFrame.copy()
    
    df_stringified = df.astype(str) # afecta a cada columna
    df = df_stringified.apply(lambda x: x.str.strip()) #por cada columna, le eliminamos espacios redundantes

    #! reemplazar strings
    df[['Best_Resolution','Resolution_WxH']] = df[['Best_Resolution', 'Resolution_WxH']].apply(
        lambda x: x.str.replace(' ', '').str.replace('nan', '').replace('', pd.NA)
    )

    #! columnas numericas
    # Medidas en MHz
    df[['Boost_Clock', 'Core_Speed', "Memory_Speed"]] = df[['Boost_Clock', 'Core_Speed','Memory_Speed']] \
        .apply(lambda x: pd.to_numeric(x.str.replace(' MHz', ''), errors='coerce').astype('Int32')) # son todos medidos en MHz

    #direct_x
    df['Direct_X'] = pd.to_numeric(
        df['Direct_X'].str.replace('DX ', ''),  # medido en DX (redundante)
        errors='coerce'
    ).astype('float32')

    #cache
    L2_CacheSplit = df['L2_Cache'].str.split('KB', n=1, expand=True) # 1024KB(x2) -> ['1024', '(x2)']

    df['L2_Cache'] = L2_CacheSplit[0].str.strip() \
        .astype('Int64', errors='ignore') # '1024' -> 1024

    #TODO: una regex puede ayudar
    df["L2_CacheQuantity"] = L2_CacheSplit[1].str.strip() \
        .str.replace('(', '') \
        .str.replace('x', '') \
        .str.replace(')', '') \
        .fillna('1') \
        .astype('Int64', errors='ignore') # 'x2)' -> '2'

    df.loc[df['L2_Cache'] == pd.NA, 'L2_CacheQuantity'] = 0 # 0 -> 0 en vez de 1

    # max power
    df['Max_Power'] = df['Max_Power'].str.replace('Watts', '').str.strip()
    df['Max_Power'].astype('Int64', errors='ignore')

    # memory
    df['Memory'] = df['Memory'].str.replace('MB', '').str.replace('MB', '').str.strip()
    df['Memory'] =  pd.to_numeric(df['Memory'], errors="coerce").astype("Int64", errors="ignore")

    # memory bandwidth
    df['Memory_Bandwidth_GBps'] = df['Memory_Bandwidth'].str.replace('GB/sec', '').str.replace('MB/sec', '').str.strip()
    df['Memory_Bandwidth_GBps'] = pd.to_numeric(df['Memory_Bandwidth_GBps'], errors='coerce').astype('float32')

    mask_MBps = df['Memory_Bandwidth'].str.contains('MB/sec', na=False)
    df.loc[mask_MBps, 'Memory_Bandwidth_GBps'] = df.loc[mask_MBps, 'Memory_Bandwidth_GBps'] / 1024

    df.rename(columns={'Memory_Bandwidth_GBps': 'Memory_Bandwidth'}, inplace=True) # sobreescribimos los cambios

    # memory bus
    df['Memory_Bus'] = df['Memory_Bus'].str.replace('bit', '').str.strip()
    df['Memory_Bus'] =  df['Memory_Bus'].astype("Int64", errors="ignore")

    # psu
    #Creamos dos nuevas columnas "PSU_W" Y "PSU_Amps" en base a PSU. Ejemplo: 450 Watt & 38 Amps -> PSU_W = 450, PSU_Amps = 38
    df[['PSU_W', 'PSU_Amps']] = df['PSU'].str.split('&', expand=True)
    df['PSU_W'] = df['PSU_W'].str.replace('Watts', '').str.strip()
    df['PSU_Amps'] = df['PSU_Amps'].str.replace('Amps', '').str.strip()

    df[['PSU_W', 'PSU_Amps']] = df[['PSU_W', 'PSU_Amps']].apply(
        lambda col: pd.to_numeric(col, errors='coerce')
    ).astype('Int32')

    #pixel rate
    df['Pixel_Rate'] = df['Pixel_Rate'].str.replace('GPixels/s', '').str.strip()
    df['Pixel_Rate'] = pd.to_numeric(df['Pixel_Rate'], errors='coerce').astype('Int32')

    #process
    df['Process'] = df['Process'].str.replace('nm', '').str.strip()
    df['Process'] = pd.to_numeric(df['Process'], errors='coerce').astype('Int32')

    #ROPS
    #Los valores de ROPs pueden ser, por ejemplo: 8 (x2),32...
    #Es decir, puede haber o no una cantidad entre parentesis que indica la cantidad de bloques, por lo tanto creamos dos nuevas columnas, "ROPs" y "ROPs_Blocks"
    df[['ROPs', 'ROPs_Blocks']] = df['ROPs'].str.split('(', n=1, expand=True) # 8 (x2) -> ['8 ', 'x2)']
    df['ROPs'] = df['ROPs'].str.strip()
    df['ROPs'] = pd.to_numeric(df['ROPs'], errors='coerce').astype('Int32')
    df['ROPs_Blocks'] = df['ROPs_Blocks'].str.strip().str.replace('x', '').str.replace(')', '')
    df['ROPs_Blocks'] = df['ROPs_Blocks'].fillna('1') # si no tiene bloques, es 1

    df.loc[df['ROPs'] == pd.NA, 'ROPs_Blocks'] = 0 # 0 -> 0 en vez de 1


    #Release_Price
    df['Release_Price'] = df['Release_Price'].str.replace('$', '').str.strip()
    df['Release_Price'] = pd.to_numeric(df['Release_Price'], errors='coerce').astype('float32')

    #texture Rate
    df['Texture_Rate'] = df['Texture_Rate'].str.replace('GTexels/s', '').str.strip()
    df['Texture_Rate'] = pd.to_numeric(df['Texture_Rate'], errors='coerce').astype('Int64')

    # infer floats
    df[['Open_GL', 'Shader']] = df[['Open_GL', 'Shader']].apply(
        lambda col: pd.to_numeric(col, errors='coerce')
    ).astype('float64')

    # extras, making them numbers 
    df[['DVI_Connection', 'DisplayPort_Connection','HDMI_Connection', 'TMUs', 'VGA_Connection']] = df[['DVI_Connection', 'DisplayPort_Connection','HDMI_Connection', 'TMUs', 'VGA_Connection']].apply(
        lambda col: pd.to_numeric(col, errors='coerce')
    ).astype('Int64')

    ##! Categories
    UNKNOWN = "Unknown"

    # Dedicated_GPU, Integrated_GPU, Notebook_GPU y SLI_Crossfire
    BOOLEAN_CATS = ["Yes", "No"]
    df[["Dedicated", "Integrated", "Notebook_GPU", "SLI_Crossfire"]] = df[["Dedicated", "Integrated", "Notebook_GPU", "SLI_Crossfire"]].apply(
    lambda x: x.str.replace(' ', '', regex=False).str.replace('nan', '', regex=False).replace('', pd.NA)).fillna(UNKNOWN)

    df[["Dedicated", "Integrated", "Notebook_GPU", "SLI_Crossfire"]] = df[["Dedicated", "Integrated", "Notebook_GPU", "SLI_Crossfire"]].astype(CategoricalDtype(categories=BOOLEAN_CATS + [UNKNOWN]))

    # Manufacturer
    MANUFACTURER_CATS = ["AMD", "Nvidia", "Intel", "ATI"]

    df['Manufacturer'] = df['Manufacturer'].str.replace('nan', '', regex=False).replace('', pd.NA).fillna(UNKNOWN)

    df['Manufacturer'] = df['Manufacturer'].astype(CategoricalDtype(categories=MANUFACTURER_CATS + [UNKNOWN]))

    # Memory_Type
    MEMTYPE_CATS = ['GDDR3', 'GDDR4', 'GDDR5', 'DDR', 'DDR3', 'DDR4', 'GDDR5X', 'HBM-2', 'DDR2', 'eDRAM', 'HBM-1', 'GDDR2']

    df['Memory_Type'] = df['Memory_Type'].str.replace('nan', '', regex=False).replace('', pd.NA).fillna(UNKNOWN)

    df['Memory_Type'] = df['Memory_Type'].astype(CategoricalDtype(categories=MEMTYPE_CATS + [UNKNOWN]))
    
    # Power_Connector
    POWER_CONNECTOR_CATS = ['2x 6-pin', '1x 6-pin + 1x 8-pin','1x 6-pin', '2x 8-pin', '1x 8-pin', '3x 8-pin', '4x 6-pin']

    df['Power_Connector'] = df['Power_Connector'].str.replace('nan', '', regex=False).replace('None', '', regex=False).replace('', pd.NA).fillna(UNKNOWN)

    df['Power_Connector'] = df['Power_Connector'].astype(CategoricalDtype(categories=POWER_CONNECTOR_CATS + [UNKNOWN]))
    
    #! Dates
    df['Release_Date'] = pd.to_datetime(
        df['Release_Date'], 
        format='%d-%b-%Y', 
        errors='coerce'
    )
    
    df['Release_Date'] = pd.to_datetime(
        df['Release_Date'].dt.strftime('%d/%m/%Y'), 
        errors='coerce'
    )

    return df