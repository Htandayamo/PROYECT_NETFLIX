from login import iniciar_sesion, registrar_cuenta, crear_superusuario
from admin import ver_usuarios, gestionar_planes, agregar_pelicula_serie, actualizar_pelicula_serie, eliminar_pelicula_serie, editar_usuario, eliminar_usuario
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
        print("\n========= MENU PRINPIPAL ===========")
        print(f"¡Bienvenido, {usuario['NombreUsuario']}!")
        print("1. Gestionar perfiles")
        print("2. Gestionar planes")
        print("3. Gestionar dispositivos")
        print("4. Contenido")
        print("5. Consultar historial de visualizaciones")
        print("6. Consultar historial de pagos")
        print("7. Cerrar sesión")
        opcion = input("Selecciona una opción: ")

        match opcion:
            case "1":
                gestionar_perfiles(conexion, usuario['IdUsuario'])
            case "2":
                gestionar_planes(conexion, usuario)
            case "3":
                consultar_visualizaciones(conexion, usuario)
            case "4":
                calificar_contenido(conexion, usuario)
            case "5":
                gestionar_dispositivos(conexion, usuario)
            case "6":
                consultar_historial_pagos(conexion, usuario)
            case "7":
                cerrar_sesion()
                break
            case _:
                print("Opción inválida. Intenta nuevamente.")





def menu_superusuario(conexion):
    """
    Menú de Superusuario para gestionar usuarios, planes y películas/series,
    utilizando un diccionario para simular el comportamiento de un switch.
    """
    # Funciones mapeadas
    opciones = {
        "1": ver_usuarios,
        "2": editar_usuario,
        "3": eliminar_usuario,
        "4": gestionar_planes,
        "5": agregar_pelicula_serie,
        "6": actualizar_pelicula_serie,
        "7": eliminar_pelicula_serie,
        "8": salir_menu
    }

    while True:
        print("\n=== Menú de Superusuario ===")
        print("1. Ver todos los usuarios")
        print("2. Editar usuario")
        print("3. Eliminar usuario")
        print("4. Gestionar planes")
        print("5. Agregar nueva película o serie")
        print("6. Actualizar una película o serie")
        print("7. Eliminar una película o serie")
        print("8. Salir")

        opcion = input("Selecciona una opción: ").strip()

        # Ejecutar la opción seleccionada si es válida
        if opcion in opciones:
            if opcion == "8":
                opciones[opcion](conexion)  # Llamar a la función para salir
                break
            else:
                opciones[opcion](conexion)  # Ejecutar la función correspondiente
        else:
            print("Opción no válida. Intenta nuevamente.")

def salir_menu(conexion):
    """
    Función para salir del menú.
    """
    print("Saliendo del menú de Superusuario.")









# Placeholder de las funciones adicionales (a desarrollar después)


def gestionar_planes(conexion, usuario):
    print("\nFunción para gestionar planes (a implementar).")

def consultar_visualizaciones(conexion, usuario):
    print("\nFunción para consultar visualizaciones (a implementar).")

def calificar_contenido(conexion, usuario):
    print("\nFunción para calificar contenido (a implementar).")

def gestionar_dispositivos(conexion, usuario):
    print("\nFunción para gestionar dispositivos (a implementar).")

def consultar_historial_pagos(conexion, usuario):
    print("\nFunción para consultar historial de pagos (a implementar).")
