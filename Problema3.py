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