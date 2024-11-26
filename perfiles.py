from prettytable import PrettyTable


def ver_perfiles(conexion, usuario_id):
    """
    Función para ver los perfiles del usuario.
    """
    try:
        cursor = conexion.cursor()
        query = """
        SELECT Nombre, ApellidoPaterno, ApellidoMaterno, FechaNacimiento, Telefono
        FROM Perfil
        WHERE IdUsuario = %s
        """
        cursor.execute(query, (usuario_id,))
        perfiles = cursor.fetchall()

        if perfiles:
            print("\n=== Perfiles ===")
            table = PrettyTable(["Nombre", "Apellido Paterno", "Apellido Materno", "Fecha de Nacimiento", "Teléfono"])
            for perfil in perfiles:
                table.add_row([perfil[0], perfil[1], perfil[2], perfil[3], perfil[4]])
            print(table)
        else:
            print("No tienes perfiles registrados.")
    except Exception as e:
        print(f"Error al ver perfiles: {e}")




def crear_perfil(conexion, id_usuario):
    """
    Función para crear o completar un perfil de usuario con la información adicional.
    """
    cursor = conexion.cursor()
    print("\n=== Crear o Completar Perfil ===")

    # Solicitar la información del perfil
    nombre = input("Nombre (opcional, se usará el que ya está registrado): ")
    apellido_paterno = input("Apellido Paterno (opcional): ")
    apellido_materno = input("Apellido Materno (opcional): ")
    fecha_nacimiento = input("Fecha de Nacimiento (YYYY-MM-DD): ")
    telefono = input("Teléfono (opcional): ")

    # Si no se ingresa un nombre, se utilizará el nombre del registro del usuario
    if not nombre:
        nombre = ""  # Usar vacío si no se proporciona nombre (puedes decidir otra lógica)

    try:
        # Insertar los datos en la tabla Perfil
        query_perfil = """
        INSERT INTO Perfil (IdUsuario, Nombre, ApellidoPaterno, ApellidoMaterno, FechaNacimiento, Telefono)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_perfil, (id_usuario, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, telefono))

        # Confirmar la inserción en la base de datos
        conexion.commit()

        print("\n¡Perfil creado o actualizado exitosamente!")

    except Exception as e:
        print(f"\nError al crear o actualizar el perfil: {e}")
        conexion.rollback()

    finally:
        cursor.close()




def eliminar_perfil(conexion, usuario_id):
    """
    Función para eliminar un perfil asociado al usuario.
    """
    try:
        # Preguntar si el usuario está seguro de eliminar su perfil
        confirmacion = input("¿Estás seguro de eliminar tu perfil? (si/no): ").strip().lower()
        
        if confirmacion != "si":
            print("Operación cancelada. No se eliminó el perfil.")
            return

        # Verificar si el usuario tiene un perfil asociado
        cursor = conexion.cursor()
        query_verificar = "SELECT IdPerfil FROM Perfil WHERE IdUsuario = %s"
        cursor.execute(query_verificar, (usuario_id,))
        perfil = cursor.fetchone()

        if perfil:
            perfil_id = perfil[0]
            # Eliminar el perfil
            query = "DELETE FROM Perfil WHERE IdPerfil = %s AND IdUsuario = %s"
            cursor.execute(query, (perfil_id, usuario_id))
            conexion.commit()

            if cursor.rowcount > 0:
                print("Perfil eliminado exitosamente.")
            else:
                print("No se pudo eliminar el perfil. Verifica que el perfil exista.")
        else:
            print("No se encontró un perfil asociado a tu usuario.")
    
    except Exception as e:
        print(f"Error al eliminar perfil: {e}")


def actualizar_perfil(conexion, usuario_id):
    """
    Función para actualizar un perfil utilizando el ID del usuario.
    """
    try:
        # Pedir los nuevos valores para los campos del perfil
        nuevo_nombre = input("Nuevo nombre: ")
        nuevo_apellido_paterno = input("Nuevo apellido paterno: ")
        nuevo_apellido_materno = input("Nuevo apellido materno: ")
        nueva_fecha_nacimiento = input("Nueva fecha de nacimiento (YYYY-MM-DD): ")
        nuevo_telefono = input("Nuevo teléfono: ")

        # Validar que la fecha de nacimiento esté en el formato correcto
        try:
            from datetime import datetime
            nueva_fecha_nacimiento = datetime.strptime(nueva_fecha_nacimiento, '%Y-%m-%d').date()
        except ValueError:
            print("Error: El formato de la fecha de nacimiento es incorrecto. Asegúrate de usar el formato YYYY-MM-DD.")
            return

        cursor = conexion.cursor()

        # Verificar si el usuario tiene un perfil
        query_verificar = """
        SELECT IdPerfil FROM Perfil WHERE IdUsuario = %s
        """
        cursor.execute(query_verificar, (usuario_id,))
        perfil = cursor.fetchone()

        if perfil:
            perfil_id = perfil[0]
            
            # Realizar la actualización del perfil en la base de datos
            query = """
            UPDATE Perfil
            SET Nombre = %s, ApellidoPaterno = %s, ApellidoMaterno = %s, FechaNacimiento = %s, Telefono = %s
            WHERE IdPerfil = %s
            """
            cursor.execute(query, (nuevo_nombre, nuevo_apellido_paterno, nuevo_apellido_materno, nueva_fecha_nacimiento, nuevo_telefono, perfil_id))
            conexion.commit()

            # Verificar si la actualización fue exitosa
            if cursor.rowcount > 0:
                print("Perfil actualizado exitosamente.")
            else:
                print("No se pudo actualizar el perfil. Verifica que los datos sean correctos.")
        else:
            print("No se encontró un perfil asociado a tu usuario.")
    
    except Exception as e:
        print(f"Error al actualizar perfil: {e}")

