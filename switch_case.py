from login import iniciar_sesion, registrar_cuenta, crear_superusuario
from admin import ver_usuarios, gestionar_planes, agregar_pelicula_serie, actualizar_pelicula_serie, eliminar_pelicula_serie, editar_usuario, eliminar_usuario, ver_peliculas_series
from usuario import ver_perfil, actualizar_perfil, agregar_resena, ver_resenas, actualizar_resena, eliminar_resena, eliminar_cuenta
from prettytable import PrettyTable
import sys

def menu_login(conexion):
    """
    Menú inicial para registrar una cuenta o iniciar sesión.
    """
    while True:
        print("\n=== Inicio ===")
        print("1. Iniciar sesión")
        print("2. Registrar nueva cuenta")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        match opcion:
            case "1":
                usuario = iniciar_sesion(conexion)
                if usuario:
                    menu_principal(conexion, usuario)
            case "2":
                registrar_cuenta(conexion)
            case "2024":
                crear_superusuario(conexion, menu_login)
                break
            case "3":
                cerrar_sesion()
                break
            case _:
                print("Opción inválida. Intenta nuevamente.")


def cerrar_sesion():
    """
    Función para cerrar sesión y regresar al menú inicial.
    """
    print("\nCerrando sesión...")
    sys.exit(0)


def menu_principal(conexion, usuario):
    """
    Menú principal que se muestra después de que el usuario inicia sesión correctamente.
    """
    while True:
        print("\n========= MENÚ PRINCIPAL ===========")
        print(f"¡Bienvenido, {usuario[1]}!")  # usuario[1] es el nombre de usuario.
        print("1. Ver Perfil")
        print("2. Actualizar Perfil")
        print("3. Ver Películas y Series")
        print("4. Agregar Reseña")
        print("5. Ver Reseñas")
        print("6. Actualizar Reseña")
        print("7. Eliminar Reseña")
        print("8. Eliminar Cuenta")
        print("9. Cerrar Sesión")
        opcion = input("Selecciona una opción: ")

        match opcion:
            case "1":
                ver_perfil(conexion, usuario)
            case "2":
                actualizar_perfil(conexion, usuario)
            case "3":
                ver_peliculas_series(conexion)
            case "4":
                agregar_resena(conexion, usuario)
            case "5":
                ver_resenas(conexion)
            case "6":
                actualizar_resena(conexion, usuario[0])
            case "7":
                eliminar_resena(conexion, usuario[0])
            case "8":
                eliminar_cuenta(conexion, usuario[0])
                break  # Salir del menú si la cuenta se elimina.
            case "9":
                print("¡Hasta luego!")
                break
            case _:
                print("Opción inválida. Intenta nuevamente.")



def menu_superusuario(conexion):

    """
    Menú de Superusuario para gestionar usuarios, planes y películas/series.
    """
    while True:
        print("\n========= MENÚ DE SUPERUSUARIO ===========")
        print("1. Ver todos los usuarios")
        print("2. Editar usuario")
        print("3. Eliminar usuario")
        print("4. Gestionar planes")
        print("5. Ver todas las Peliculas o Series")
        print("6. Agregar nueva película o serie")
        print("7. Actualizar una película o serie")
        print("8. Eliminar una película o serie")
        print("9. Salir")

        opcion = input("Selecciona una opción: ").strip()

        match opcion:
            case "1":
                ver_usuarios(conexion)
            case "2":
                editar_usuario(conexion)
            case "3":
                eliminar_usuario(conexion)
            case "4":
                gestionar_planes(conexion)
            case "5":
                ver_peliculas_series(conexion)
            case "6":
                agregar_pelicula_serie(conexion)
            case "7":
                actualizar_pelicula_serie(conexion)
            case "8":
                eliminar_pelicula_serie(conexion)
            case "9":
                break
            case _:
                print("opcion incorrecta. Intenta nuevamente.")