#campos skippeados: Power_Connector

def ParseFields(dataFrame):
    df = dataFrame.copy()
    
    df_stringified = df.astype(str) # afecta a cada columna
    df = df_stringified.apply(lambda x: x.str.strip()) #por cada columna, le eliminamos espacios redundantes

    #! reemplazar strings
    df['Best_Resolution'] = df['Best_Resolution'].str.replace(' ', '')


    #! columnas numericas
    # Medidas en MHz
    df[['Boost_Clock', 'Core_Speed', "Memory_Speed"]] = df[['Boost_Clock', 'Core_Speed','Memory_Speed']] \
        .apply(lambda x:  pd.to_numeric(x.str.replace(' MHz', ''), errors='coerce').astype('Int64')) # son todos medidos en MHz

    #direct_x
    df['Direct_X'] = pd.to_numeric(
        df['Direct_X'].str.replace('DX ', ''),  # medido en DX (redundante)
        errors='coerce'
    )
    #cache
    L2_CacheSplit = df['L2_Cache'].str.split('(', n=1, expand=True) # 1024KB(x2) -> ['1024KB', 'x2)']

    df['L2_Cache'] = L2_CacheSplit[0].str.strip() \
        .replace('KB','') \
        .astype('Int64', errors='ignore') # '1024KB' -> 1024

    df["L2_CacheQuantity"] = L2_CacheSplit[1].str.strip() \
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
    df['Memory'] = df['Memory'].astype("Int64", errors="ignore")

    # memory bandwidth
    df['Memory_Bandwidth_GBps'] = df['Memory_Bandwidth'].str.replace('GB/sec', '').str.replace('MB/sec', '').str.strip()
    df['Memory_Bandwidth_GBps'] =  df['Memory_Bandwidth_GBps'].astype("Int64", errors="ignore")

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

    df[['PSU_W','PSU_Amps']] = pd.to_numeric(df[['PSU_W', 'PSU_Amps']], errors='coerce')

    #pixel rate
    df['Pixel_Rate'] = df['Pixel_Rate'].str.replace('GPixels/s', '').str.strip()
    df['Pixel_Rate'] = pd.to_numeric(df['Pixel_Rate'], errors='coerce')

    #process
    df['Process'] = df['Process'].str.replace('nm', '').str.strip()
    df['Process'] = pd.to_numeric(df['Process'], errors='coerce')
    df['Process'] = pd.to_numeric(df['Process'], errors='coerce')

    #ROPS
    #Los valores de ROPs pueden ser por ejemplo: 8 (x2),32,
    #es decir, puede haber o no, una cantidad entre parentesis que indica la cantidad de bloques  por lo tanto, creamos dos nuevas columnas "ROPs" y "ROPs_Blocks"
    df[['ROPs', 'ROPs_Blocks']] = df['ROPs'].str.split('(', n=1, expand=True) # 8 (x2) -> ['8 ', 'x2)']
    df['ROPs'] = df['ROPs'].str.strip()
    df['ROPs'] = pd.to_numeric(df['ROPs'], errors='coerce')
    df['ROPs_Blocks'] = df['ROPs_Blocks'].str.strip().str.replace('x', '').str.replace(')', '')
    df['ROPs_Blocks'] = df['ROPs_Blocks'].fillna('1') # si no tiene bloques, es 1

    df.loc[df['ROPs'] == pd.NA, 'ROPs_Blocks'] = 0 # 0 -> 0 en vez de 1


    #Release_Price
    df['Release_Price'] = df['Release_Price'].str.replace('$', '').str.strip()
    df['Release_Price'] = pd.to_numeric(df['Release_Price'], errors='coerce')

    #texture Rate
    df['Texture_Rate'] = df['Texture_Rate'].str.replace('GTexels/s', '').str.strip()
    df['Texture_Rate'] = pd.to_numeric(df['Texture_Rate'], errors='coerce')

    # infer floats
    df[['Open_GL', 'Shader']] = pd.to_numeric(df[['Open_GL', 'Shader']], errors='coerce')

    # extras, making them numbers 
    transformToNumber = df[['DVI_Connection', 'DisplayPort_Connection','HDMI_Connection', 'TMUs', 'VGA_Connection']]
    transformToNumber = transformToNumber.astype('Int16', errors='ignore')

    ##! Categories
    UNKNOWN = "Unknown"

    # Dedicated_GPU, Integrated_GPU, Notebook_GPU y SLI_Crossfire
    BOOLEAN_CATS = ["Yes", "No"]
    
    df[["Dedicated", "Integrated", "Notebook_GPU", "SLI_Crossfire"]] = df[["Dedicated", "Integrated", "Notebook_GPU", "SLI_Crossfire"]].replace({ 
    np.nan: UNKNOWN, pd.NA: UNKNOWN, "": UNKNOWN, " ": UNKNOWN
    })

    df[["Dedicated", "Integrated", "Notebook_GPU", "SLI_Crossfire"]] = df[["Dedicated", "Integrated", "Notebook_GPU", "SLI_Crossfire"]].astype(CategoricalDtype(categories=BOOLEAN_CATS + [UNKNOWN]))

    # Manufacturer
    MANUFACTURER_CATS = ["AMD", "Nvidia", "Intel", "ATI"]

    df['Manufacturer'] = df['Manufacturer'].replace({ 
        np.nan: UNKNOWN, pd.NA: UNKNOWN, "": UNKNOWN, " ": UNKNOWN
    })

    df['Manufacturer'] = df['Manufacturer'].astype(CategoricalDtype(categories=MANUFACTURER_CATS + [UNKNOWN]))

    # Memory_Type
    MEMTYPE_CATS = ['GDDR3', 'GDDR4', 'GDDR5', 'DDR', 'DDR3', 'DDR4', 'GDDR5X', 'HBM-2', 'DDR2', 'eDRAM', 'HBM-1', 'GDDR2']

    df['Memory_Type'] = df['Memory_Type'].replace({ 
        np.nan: UNKNOWN, pd.NA: UNKNOWN, "": UNKNOWN, " ": UNKNOWN
    })

    df['Memory_Type'] = df['Memory_Type'].astype(CategoricalDtype(categories=MEMTYPE_CATS + [UNKNOWN]))

    #! Dates
    df['Release_Date'] = pd.to_datetime(
        df['Release_Date'], 
        format='%d-%b-%Y', 
        errors='coerce'
    )
    df['Release_Date'] = df['Release_Date'].dt.strftime('%d/%m/%Y')

    return df