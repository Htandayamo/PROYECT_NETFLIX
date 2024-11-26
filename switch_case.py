from login import iniciar_sesion, registrar_cuenta
from perfiles import ver_perfiles, eliminar_perfil, actualizar_perfil, crear_perfil
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
        print("\n=== Menú Principal ===")
        print(f"¡Bienvenido, {usuario['Nombre']} {usuario['Apellido']}!")
        print("1. Gestionar perfiles")
        print("2. Gestionar planes")
        print("3. Consultar historial de visualizaciones")
        print("4. Calificar contenido")
        print("5. Gestionar dispositivos")
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


def gestionar_perfiles(conexion, usuario_id):
    """
    Función para gestionar los perfiles (ver, eliminar, actualizar).
    """
    while True:
        print("\n=== Gestionar Perfiles ===")
        print("1. Crear perfil")
        print("2. Ver perfil")
        print("3. Eliminar perfil")
        print("4. Actualizar perfil")
        print("5. Regresar al menú principal")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            crear_perfil(conexion, usuario_id)
        elif opcion == "2":
            ver_perfiles(conexion, usuario_id)
        elif opcion == "3":
            eliminar_perfil(conexion, usuario_id)
        elif opcion == "4":
            actualizar_perfil(conexion, usuario_id)
        elif opcion == "5":
            return  # Regresar al menú principal
        else:
            print("Opción inválida. Intenta nuevamente.")




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
