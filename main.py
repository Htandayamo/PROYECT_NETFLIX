from conexion import conectar, cerrar_conexion
from switch_case import menu_login

def main():
    # Establecer conexión a la base de datos
    conexion = conectar()
    if conexion:
        try:
            # Ejecutar el menú de login donde el usuario puede iniciar sesión o registrar una nueva cuenta
            menu_login(conexion)
        except Exception as e:
            print(f"Ocurrio un error : {e}")
        finally:
            # Cerrar la conexión una vez que se haya terminado con el programa
            cerrar_conexion(conexion)

if __name__ == "__main__":
    main()

