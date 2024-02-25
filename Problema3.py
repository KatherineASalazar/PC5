# En este problema trabajaremos con el archivo llamado reactiva.xlsx
# Deberá realizar lo siguiente:
# - Cree un archivo llamado procesamiento .py
# - Genere una función de limpieza que permita el renombre de las columnas 
#   eliminando espacios, tildes y convirtiendo los nombres de columna a minúscula. 
#   De ser necesario cambie el nombre de columna a uno que le sea de más ayuda.
# - Elimine la columna ID y TipoMoneda que se encuentre repetida. 
# - De la columna “DISPOSITIVO LEGAL” elimine el carácter coma ‘,’ del texto.
# - Empleando el api de sunat de la pc4. Dolarice los valores de montos de inversión y 
# montos de transferencia de acuerdo con el valor actual del dólar. Deberá mostrar 
# estos montos en dos nuevas columnas.
# - Para la columna “Estado” cambie los valores a: Actos Previos, Concluido, 
#   Resuelto y Ejecucion
# - Cree una nueva columna que puntue el estado según: ActosPrevios -> 1, 
#   Resuelto->0, Ejecución 2 y Concluido 3

# Genere los siguientes reportes
# - Almacene en una base de datos una tabla de ubigeos a partir de los datos sin 
# duplicados de las columnas “ubigeo”, “Region”, “Provincia”, “Distrito”
# - Por cada región genere un Excel con el top 5 costo inversión de las obras de tipo 
# Urbano en estado 1,2,3. En caso no haber datos en alguna de las regiones, no se 
# generará el reporte

# Generación envio de correo:
# - Cree un modulo envio_correo.py que se encargue de la parte de envio de correo. 
# Puede emplear funciones y/o clases
# Integrar los módulos y tomar captura al menos de uno de los correos enviados mediante 
# código


import pandas as pd
from sqlalchemy import create_engine

def limpiar_datos(df):
    # Renombrar columnas
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('á', 'a').str.replace('é', 'e').str.replace('í', 'i').str.replace('ó', 'o').str.replace('ú', 'u')
    
    # Eliminar columnas duplicadas
    df = df.loc[:,~df.columns.duplicated()]
    
    # Eliminar coma del texto en la columna "DISPOSITIVO_LEGAL"
    df['dispositivo_legal'] = df['dispositivo_legal'].str.replace(',', '')
    
    # Dolarizar los montos de inversión y transferencia
    
    # Cambiar valores de la columna "Estado"
    
    # Crear nueva columna de puntuación del estado
    
    return df



def almacenar_ubigeos(df):
    # Almacenar tabla de ubigeos en una base de datos
    engine = create_engine('sqlite:///ubigeos.db', echo=False)
    df_ubigeos = df[['ubigeo', 'region', 'provincia', 'distrito']].drop_duplicates()
    df_ubigeos.to_sql('ubigeos', con=engine, if_exists='replace', index=False)

def generar_reportes_por_region(df):
    # Generar reportes por región en archivos Excel
    regiones = df['region'].unique()
    for region in regiones:
        df_region = df[df['region'] == region]
        # Realizar el procesamiento para obtener el top 5 de costos de inversión y generar el Excel

def main():
    # Cargar el archivo de Excel
    df = pd.read_excel('reactiva.xlsx')
    
    # Realizar limpieza de datos
    df_limpiado = limpiar_datos(df)
    
    # Almacenar tabla de ubigeos en una base de datos
    almacenar_ubigeos(df_limpiado)
    
    # Generar reportes por región en archivos Excel
    generar_reportes_por_region(df_limpiado)

if __name__ == "__main__":
    main()
