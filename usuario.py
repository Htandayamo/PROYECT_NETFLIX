from prettytable import PrettyTable

def ver_perfil(conexion, usuario):
    """
    Muestra la información del perfil del usuario con formato de tabla.
    """
    cursor = conexion.cursor()
    print("\n=== PERFIL DE USUARIO ===")
    try:
        # Consulta para obtener el perfil del usuario
        query = """
        SELECT id, nombre_usuario, correo_electronico, plan_suscripcion, estado, rol, fecha_creacion 
        FROM usuarios 
        WHERE id = %s
        """
        cursor.execute(query, (usuario[0],))
        perfil = cursor.fetchone()

        if perfil:
            # Crear la tabla con PrettyTable
            tabla = PrettyTable()
            tabla.field_names = ["Campo", "Información"]
            
            # Agregar las filas de datos
            tabla.add_row(["ID", perfil[0]])
            tabla.add_row(["Nombre de usuario", perfil[1]])
            tabla.add_row(["Correo electrónico", perfil[2]])
            tabla.add_row(["Plan de suscripción", perfil[3]])
            tabla.add_row(["Estado", perfil[4]])
            tabla.add_row(["Rol", perfil[5]])
            tabla.add_row(["Fecha de creación", perfil[6]])

            # Mostrar la tabla
            print(tabla)
        else:
            print("No se encontró información del perfil.")

    except Exception as e:
        print(f"Error al obtener el perfil: {e}")

    finally:
        cursor.close()


def actualizar_perfil(conexion, usuario):
    """
    Permite al usuario actualizar la información de su perfil.
    """
    cursor = conexion.cursor()
    print("\n=== ACTUALIZAR PERFIL ===")
    try:
        # Solicitar al usuario los datos que desea actualizar
        nuevo_nombre = input("Nuevo nombre de usuario (opcional): ").strip()
        nuevo_correo = input("Nuevo correo electrónico (opcional): ").strip()
        nuevo_plan = input("Nuevo plan de suscripción (basico, estandar, premium) [opcional]: ").strip()

        # Consulta para obtener el perfil actual del usuario
        query_select = "SELECT nombre_usuario, correo_electronico, plan_suscripcion FROM usuarios WHERE id = %s"
        cursor.execute(query_select, (usuario[0],))
        perfil_actual = cursor.fetchone()

        if not perfil_actual:
            print("No se encontró el perfil del usuario.")
            return

        # Mantener los datos actuales si no se proporciona un valor nuevo
        nuevo_nombre = nuevo_nombre or perfil_actual[0]
        nuevo_correo = nuevo_correo or perfil_actual[1]
        nuevo_plan = nuevo_plan or perfil_actual[2]

        # Validar que el nuevo plan sea válido
        if nuevo_plan not in ('basico', 'estandar', 'premium'):
            print("El plan de suscripción ingresado no es válido.")
            return

        # Actualizar la información en la base de datos
        query_update = """
        UPDATE usuarios 
        SET nombre_usuario = %s, correo_electronico = %s, plan_suscripcion = %s 
        WHERE id = %s
        """
        cursor.execute(query_update, (nuevo_nombre, nuevo_correo, nuevo_plan, usuario[0]))
        conexion.commit()

        print("\n¡Perfil actualizado exitosamente!")

        # Mostrar la nueva información del perfil
        query_updated_profile = "SELECT id, nombre_usuario, correo_electronico, plan_suscripcion FROM usuarios WHERE id = %s"
        cursor.execute(query_updated_profile, (usuario[0],))
        perfil_actualizado = cursor.fetchone()

        if perfil_actualizado:
            tabla = PrettyTable()
            tabla.field_names = ["Campo", "Información"]
            tabla.add_row(["ID", perfil_actualizado[0]])
            tabla.add_row(["Nombre de usuario", perfil_actualizado[1]])
            tabla.add_row(["Correo electrónico", perfil_actualizado[2]])
            tabla.add_row(["Plan de suscripción", perfil_actualizado[3]])

            print("\n=== NUEVA INFORMACIÓN DEL PERFIL ===")
            print(tabla)

    except Exception as e:
        print(f"Error al actualizar el perfil: {e}")

    finally:
        cursor.close()


def agregar_resena(conexion, usuario):
    """
    Permite a un usuario agregar una reseña a una película o serie.
    """
    cursor = conexion.cursor()
    print("\n=== AGREGAR RESEÑA ===")
    try:
        # Solicitar al usuario el ID de la película o serie
        id_pelicula_serie = input("Ingresa el ID de la película o serie: ").strip()
        texto_resena = input("Escribe tu reseña: ").strip()
        calificacion = input("Calificación (1 a 5): ").strip()

        # Validar que la calificación esté en el rango permitido
        if not calificacion.isdigit() or not (1 <= int(calificacion) <= 5):
            print("La calificación debe ser un número entre 1 y 5.")
            return

        # Insertar la reseña en la base de datos
        query_insert = """
        INSERT INTO resenas (id_usuario, id_pelicula_serie, texto_resena, calificacion)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_insert, (usuario[0], id_pelicula_serie, texto_resena, int(calificacion)))
        conexion.commit()

        print("\n¡Reseña agregada exitosamente!")

        # Mostrar la reseña recién agregada
        query_new_review = """
        SELECT r.id, p.titulo, r.texto_resena, r.calificacion, r.fecha_creacion
        FROM resenas r
        INNER JOIN peliculas_series p ON r.id_pelicula_serie = p.id
        WHERE r.id_usuario = %s
        ORDER BY r.fecha_creacion DESC LIMIT 1
        """
        cursor.execute(query_new_review, (usuario[0],))
        nueva_resena = cursor.fetchone()

        if nueva_resena:
            tabla = PrettyTable()
            tabla.field_names = ["ID Reseña", "Película/Serie", "Reseña", "Calificación", "Fecha de Creación"]
            tabla.add_row([nueva_resena[0], nueva_resena[1], nueva_resena[2], nueva_resena[3], nueva_resena[4]])

            print("\n=== RESEÑA RECIÉN AGREGADA ===")
            print(tabla)
        else:
            print("No se pudo recuperar la reseña recién agregada.")

    except Exception as e:
        print(f"Error al agregar la reseña: {e}")

    finally:
        cursor.close()


def ver_resenas(conexion):
    """
    Permite ver todas las reseñas de una película o serie específica.
    """
    cursor = conexion.cursor()
    print("\n=== VER RESEÑAS ===")
    try:
        # Solicitar el ID de la película o serie
        id_pelicula_serie = input("Ingresa el ID de la película o serie para ver las reseñas: ").strip()

        # Consultar las reseñas relacionadas con la película o serie
        query = """
        SELECT r.id, u.nombre_usuario, r.texto_resena, r.calificacion, r.fecha_creacion
        FROM resenas r
        INNER JOIN usuarios u ON r.id_usuario = u.id
        WHERE r.id_pelicula_serie = %s
        ORDER BY r.fecha_creacion DESC
        """
        cursor.execute(query, (id_pelicula_serie,))
        resenas = cursor.fetchall()

        if resenas:
            # Crear la tabla con PrettyTable
            tabla = PrettyTable()
            tabla.field_names = ["ID Reseña", "Usuario", "Reseña", "Calificación", "Fecha de Creación"]

            # Agregar las filas con datos de las reseñas
            for resena in resenas:
                tabla.add_row([resena[0], resena[1], resena[2], resena[3], resena[4]])

            print("\n=== RESEÑAS PARA LA PELÍCULA/SERIE ===")
            print(tabla)
        else:
            print("No hay reseñas registradas para esta película o serie.")

    except Exception as e:
        print(f"Error al consultar las reseñas: {e}")

    finally:
        cursor.close()


def actualizar_resena(conexion, usuario_id):
    """
    Permite a un usuario actualizar una reseña existente que él mismo haya realizado.
    """
    cursor = conexion.cursor()
    print("\n=== ACTUALIZAR RESEÑA ===")

    try:
        # Obtener las reseñas del usuario
        query_resenas = """
        SELECT r.id, ps.titulo, r.texto_resena, r.calificacion, r.fecha_creacion
        FROM resenas r
        INNER JOIN peliculas_series ps ON r.id_pelicula_serie = ps.id
        WHERE r.id_usuario = %s
        ORDER BY r.fecha_creacion DESC
        """
        cursor.execute(query_resenas, (usuario_id,))
        resenas = cursor.fetchall()

        if not resenas:
            print("No tienes reseñas registradas para actualizar.")
            return

        # Mostrar las reseñas con PrettyTable
        tabla = PrettyTable()
        tabla.field_names = ["ID Reseña", "Título", "Reseña", "Calificación", "Fecha de Creación"]

        for resena in resenas:
            tabla.add_row([resena[0], resena[1], resena[2], resena[3], resena[4]])

        print("\n=== TUS RESEÑAS ===")
        print(tabla)

        # Solicitar el ID de la reseña a actualizar
        id_resena_input = input("Ingresa el ID de la reseña que deseas actualizar: ").strip()

        if not id_resena_input.isdigit():
            print("Error: El ID ingresado no es válido. Debe ser un número.")
            return

        id_resena = int(id_resena_input)

        # Validar que el ID pertenece al usuario
        ids_resenas_usuario = [resena[0] for resena in resenas]
        if id_resena not in ids_resenas_usuario:
            print("Error: No puedes actualizar una reseña que no te pertenece.")
            return

        # Obtener los datos actuales de la reseña
        query_resena_actual = """
        SELECT texto_resena, calificacion
        FROM resenas
        WHERE id = %s AND id_usuario = %s
        """
        cursor.execute(query_resena_actual, (id_resena, usuario_id))
        resena_actual = cursor.fetchone()

        if not resena_actual:
            print("Error: No se encontró la reseña seleccionada.")
            return

        # Mostrar los datos actuales al usuario
        texto_actual, calificacion_actual = resena_actual
        print(f"\nTexto actual: {texto_actual}")
        print(f"Calificación actual: {calificacion_actual}")

        # Solicitar los nuevos valores
        nuevo_texto = input("Ingresa el nuevo texto de la reseña (opcional, deja vacío para mantener el actual): ").strip()
        nueva_calificacion = input("Ingresa la nueva calificación (1-5, opcional, deja vacío para mantener la actual): ").strip()

        # Validar y mantener valores actuales si no se proporciona algo nuevo
        nuevo_texto = nuevo_texto if nuevo_texto else texto_actual
        nueva_calificacion = int(nueva_calificacion) if nueva_calificacion.isdigit() and 1 <= int(nueva_calificacion) <= 5 else calificacion_actual

        # Actualizar la reseña en la base de datos
        query_update = """
        UPDATE resenas
        SET texto_resena = %s, calificacion = %s
        WHERE id = %s AND id_usuario = %s
        """
        cursor.execute(query_update, (nuevo_texto, nueva_calificacion, id_resena, usuario_id))
        conexion.commit()

        # Confirmar cambios
        if cursor.rowcount > 0:
            print("\nReseña actualizada correctamente.")
        else:
            print("\nNo se pudo actualizar la reseña. Verifica los datos ingresados.")

        # Mostrar la reseña actualizada
        query_updated = """
        SELECT r.id, ps.titulo, r.texto_resena, r.calificacion, r.fecha_creacion
        FROM resenas r
        INNER JOIN peliculas_series ps ON r.id_pelicula_serie = ps.id
        WHERE r.id = %s
        """
        cursor.execute(query_updated, (id_resena,))
        reseña_actualizada = cursor.fetchone()

        if reseña_actualizada:
            tabla_actualizada = PrettyTable()
            tabla_actualizada.field_names = ["ID Reseña", "Título", "Reseña", "Calificación", "Fecha de Creación"]
            tabla_actualizada.add_row(reseña_actualizada)
            print("\n=== RESEÑA ACTUALIZADA ===")
            print(tabla_actualizada)

    except Exception as e:
        print(f"Error al actualizar la reseña: {e}")

    finally:
        cursor.close()



def eliminar_resena(conexion, usuario_id):
    """
    Permite a un usuario eliminar una reseña que haya realizado en una película o serie.
    """
    cursor = conexion.cursor()
    print("\n=== ELIMINAR RESEÑA ===")

    try:
        # Mostrar todas las reseñas del usuario
        query_resenas = """
        SELECT r.id, ps.titulo, r.texto_resena, r.calificacion, r.fecha_creacion
        FROM resenas r
        INNER JOIN peliculas_series ps ON r.id_pelicula_serie = ps.id
        WHERE r.id_usuario = %s
        ORDER BY r.fecha_creacion DESC
        """
        cursor.execute(query_resenas, (usuario_id,))
        resenas = cursor.fetchall()

        if not resenas:
            print("No tienes reseñas registradas para eliminar.")
            return

        # Mostrar las reseñas disponibles para eliminar
        tabla = PrettyTable()
        tabla.field_names = ["ID Reseña", "Título", "Reseña", "Calificación", "Fecha de Creación"]

        for resena in resenas:
            tabla.add_row([resena[0], resena[1], resena[2], resena[3], resena[4]])

        print("\n=== TUS RESEÑAS ===")
        print(tabla)

        # Solicitar el ID de la reseña a eliminar
        id_resena_input = input("Ingresa el ID de la reseña que deseas eliminar: ").strip()

        # Validar que el ID sea un número
        if not id_resena_input.isdigit():
            print("Error: El ID ingresado no es válido. Debe ser un número.")
            return

        id_resena = int(id_resena_input)

        # Validar que el ID de la reseña pertenece al usuario
        ids_resenas_usuario = [resena[0] for resena in resenas]
        if id_resena not in ids_resenas_usuario:
            print("Error: No puedes eliminar una reseña que no te pertenece.")
            return

        # Confirmación antes de eliminar
        confirmacion = input(f"¿Estás seguro de que deseas eliminar la reseña con ID {id_resena}? (s/n): ").strip().lower()
        if confirmacion != 's':
            print("Operación cancelada.")
            return

        # Eliminar la reseña de la base de datos
        query_delete = "DELETE FROM resenas WHERE id = %s AND id_usuario = %s"
        cursor.execute(query_delete, (id_resena, usuario_id))
        conexion.commit()

        # Confirmar eliminación
        if cursor.rowcount > 0:
            print(f"\nReseña con ID {id_resena} eliminada correctamente.")
        else:
            print(f"\nNo se encontró la reseña con ID {id_resena}. Verifica los datos ingresados.")

    except Exception as e:
        print(f"Error al eliminar la reseña: {e}")

    finally:
        cursor.close()


def eliminar_cuenta(conexion, usuario_id):
    """
    Permite a un usuario eliminar su cuenta de la aplicación.
    """
    cursor = conexion.cursor()
    print("\n=== ELIMINAR CUENTA ===")

    try:
        # Confirmar que el usuario desea eliminar su cuenta
        confirmacion = input("¿Estás seguro de que deseas eliminar tu cuenta? Esta acción no se puede deshacer. (s/n): ").strip().lower()
        if confirmacion != 's':
            print("Operación cancelada.")
            return

        # Confirmar el ID del usuario
        confirmacion_id = input(f"Por favor, confirma tu ID de usuario ({usuario_id}) para proceder: ").strip()
        if not confirmacion_id.isdigit() or int(confirmacion_id) != usuario_id:
            print("Error: El ID ingresado no coincide con tu cuenta.")
            return

        # Eliminar todas las reseñas del usuario (clave foránea en la tabla reseñas)
        query_delete_resenas = "DELETE FROM resenas WHERE id_usuario = %s"
        cursor.execute(query_delete_resenas, (usuario_id,))
        conexion.commit()

        # Eliminar la cuenta del usuario
        query_delete_usuario = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(query_delete_usuario, (usuario_id,))
        conexion.commit()

        # Verificar si se eliminó el usuario
        if cursor.rowcount > 0:
            print(f"\nCuenta con ID {usuario_id} eliminada correctamente. Lamentamos verte partir.")
        else:
            print("\nError: No se encontró una cuenta asociada a tu ID. Verifica los datos ingresados.")

    except Exception as e:
        print(f"Error al eliminar la cuenta: {e}")

    finally:
        cursor.close()

