# clase de conexion a BD sin sqlalchemy 
import mysql.connector


# conexion a la base de datos

def conexion():
    return mysql.connector.connect(
        host='localhost',
        database='tienda',
        user='root',  # luego en producción usa variable de entorno
        password='Nonis.1997' # luego en producción usa variable de entorno
    )

# cerrar conexion a la base de datos

def cerrar_conexion(conn):
    if conn.is_connected():
        conn.close()
        print("Conexion a la base de datos cerrada.")

# probar conexion a la base de datos
def probar_conexion():
    conn = conexion()
    if conn.is_connected():
        print("Conexion a la base de datos exitosa.")
    else:
        print("Error en la conexion a la base de datos.")
    cerrar_conexion(conn)