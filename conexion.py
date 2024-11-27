import mysql.connector
from mysql.connector import Error

def conectar():
    """Establece una conexión a la base de datos y la retorna."""
    try:
        conexion = mysql.connector.connect(
            host="localhost",       # Cambiar según tu configuración
            user="root",
            #password="", #en caso de que la base de datos tenga una contraseña            
            database="Netflix"  # Nombre de tu base de datos
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos.")
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def cerrar_conexion(conexion):
    """Cierra la conexión a la base de datos."""
    if conexion.is_connected():
        conexion.close()
        print("Conexión cerrada.")

