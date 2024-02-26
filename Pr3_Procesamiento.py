# En este problema trabajaremos con el archivo llamado reactiva.xlsx

# Deberá realizar lo siguiente:
# - Cree un archivo llamado procesamiento .py

# LIMPIAR DATOS
# - Genere una función de limpieza que permita el renombre de las columnas 
#   eliminando espacios, tildes y convirtiendo los nombres de columna a minúscula. 
#   De ser necesario cambie el nombre de columna a uno que le sea de más ayuda.
# - Elimine la columna ID y TipoMoneda que se encuentre repetida. 
# - De la columna “DISPOSITIVO LEGAL” elimine el carácter coma ‘,’ del texto.

# DOLARIZAR MONTOS
# - Empleando el api de sunat de la pc4. Dolarice los valores de montos de inversión y 
# montos de transferencia de acuerdo con el valor actual del dólar. Deberá mostrar 
# estos montos en dos nuevas columnas.

#  MAPEAR ESTADO
# - Para la columna “Estado” cambie los valores a: Actos Previos, Concluido, 
#   Resuelto y Ejecucion
# - Cree una nueva columna que puntue el estado según: ActosPrevios -> 1, 
#   Resuelto->0, Ejecución 2 y Concluido 3

#  GENERACIÓN DE REPORTES
# - Almacene en una base de datos una tabla de ubigeos a partir de los datos sin 
# duplicados de las columnas “ubigeo”, “Region”, “Provincia”, “Distrito”
# - Por cada región genere un Excel con el top 5 costo inversión de las obras de tipo 
# Urbano en estado 1,2,3. En caso no haber datos en alguna de las regiones, no se 
# generará el reporte

# ENVÍO DE CORREO:
# - Cree un modulo envio_correo.py que se encargue de la parte de envio de correo. 

# Puede emplear funciones y/o clases
# Integrar los módulos y tomar captura al menos de uno de los correos enviados mediante 
# código


import pandas as pd
df_procesamiento_procesamiento = pd.read_excel("./data/reactiva.xlsx")

import sqlite3
import os

from sqlite3 import requests

def limpiar_datos(df_procesamiento):
    # Renombrar columnas
    df_procesamiento.columns = df_procesamiento.columns.str.lower().str.replace(' ', '_').str.replace('á', 'a').str.replace('é', 'e').str.replace('í', 'i').str.replace('ó', 'o').str.replace('ú', 'u')
    
    # Eliminar columnas duplicadas
    df_procesamiento = df_procesamiento.loc[:,~df_procesamiento.columns.duplicated()]
    
    # Eliminar coma del texto en la columna "DISPOSITIVO_LEGAL"
    df_procesamiento_procesamiento['dispositivo_legal'] = df_procesamiento['dispositivo_legal'].str.replace(',', '')
    
    return df_procesamiento


def dolarizar_montos(df_procesamiento):
    # Obtener el valor actual del dólar desde la API de Sunat
    response = requests.get('https://api.apis.net.pe/v1/tipo-cambio-sunat')
    valor_dolar = response.json()['compra']  # Suponiendo que la API devuelve el valor del dólar
    
    # Dolarizar los montos de inversión y transferencia
    df_procesamiento['montoinversion_dolares'] = df_procesamiento['montoinversion'] / valor_dolar
    df_procesamiento['montotransferencia_dolares'] = df_procesamiento['montotransferencia'] / valor_dolar
    
    return df_procesamiento


def mapear_estado(df_procesamiento):
    # Mapear valores de la columna "Estado"
    estado_mapping = {
        'ActosPrevios': 1,
        'Resuelto': 0,
        'Ejecucion': 2,
        'Concluido': 3
    }
    df_procesamiento['estado_puntuado'] = df_procesamiento['estado'].map(estado_mapping)
    
    return df_procesamiento


 # Almacena los ubigeos sin duplicados en la base de datos

def almacenar_ubigeos(df_procesamiento):
    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('ubigeos.db')

    # Si existe una tabla de ubigeos, se elimina
    conn.execute("DROP TABLE IF EXISTS Ubigeos")

    # Crear la tabla de ubigeos
    conn.execute('''CREATE TABLE Ubigeos (
                        ubigeo TEXT PRIMARY KEY,
                        region TEXT,
                        provincia TEXT,
                        distrito TEXT)''')

    # Insertar los datos sin duplicados en la tabla
    df_procesamiento[['ubigeo', 'Region', 'Provincia', 'Distrito']].drop_duplicates().to_sql('Ubigeos', conn, index=False, if_exists='replace')

    # Cerrar la conexión a la base de datos
    conn.close()

    return df_procesamiento


def generar_reportes_por_region(df_procesamiento):

    
    # Agrupa el DataFrame por región
    for region, datos_region in df_procesamiento.groupby('Region'):
        # Filtra las obras de tipo Urbano y en estado 1, 2 y 3
        obras_urbanas = datos_region[(datos_region['Tipo'] == 'Urbano') & (datos_region['estado'].isin([1, 2, 3]))]
        
        # Si no hay datos de obras urbanas en alguno de los estados, no se genera el reporte
        if obras_urbanas.empty:
            print(f"No hay datos de obras urbanas en los estados 1, 2 o 3 para la región {region}")
            continue
        
        # Genera el top 5 de obras urbanas por costo de inversión
        top_5_obras = obras_urbanas.nlargest(5, 'monto_inversion')
        
        # Guarda el reporte en un archivo Excel
        nombre_archivo = f"reporte_{region}.xlsx"
        top_5_obras.to_excel(nombre_archivo, index=False)
        print(f"Reporte generado para la región {region} en el archivo {nombre_archivo}")



def main():
    # Cargar el archivo de Excel
    df_procesamiento = pd.read_excel('reactiva.xlsx')
    
    # Realizar limpieza de datos
    df_procesamiento_limpiado = limpiar_datos(df_procesamiento)
    
    # Almacenar tabla de ubigeos en una base de datos
    almacenar_ubigeos(df_procesamiento_limpiado)
    
    # Generar reportes por región en archivos Excel
    generar_reportes_por_region(df_procesamiento_limpiado)


if __name__ == "__main__":
    main()
