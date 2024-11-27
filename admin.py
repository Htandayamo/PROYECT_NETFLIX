from prettytable import PrettyTable

def ver_usuarios(conexion):
    """
    Muestra una lista de todos los usuarios con formato de tabla.
    """
    cursor = conexion.cursor()
    print("\n=== Lista de Usuarios ===")
    try:
        query = "SELECT id, nombre_usuario, correo_electronico, plan_suscripcion, rol, estado  FROM usuarios"
        cursor.execute(query)
        usuarios = cursor.fetchall()

        if usuarios:
            # Crear la tabla con PrettyTable
            tabla = PrettyTable()
            tabla.field_names = ["ID", "Nombre", "Correo", "Plan", "Rol","Estado" ]

            # Agregar las filas de datos
            for usuario in usuarios:
                tabla.add_row([usuario[0], usuario[1], usuario[2], usuario[3], usuario[4], usuario[5]])

            # Mostrar la tabla
            print(tabla)
        else:
            print("No hay usuarios registrados.")

    except Exception as e:
        print(f"Error al obtener la lista de usuarios: {e}")

    finally:
        cursor.close()


def editar_usuario(conexion):
    """
    Permite editar los detalles de un usuario existente.
    """
    cursor = conexion.cursor()
    try:
        # Solicitar al administrador el ID del usuario a editar
        id_usuario = int(input("Ingresa el ID del usuario a editar: ").strip())

        # Solicitar los nuevos datos para el usuario
        nuevo_nombre = input("Nuevo nombre de usuario: ").strip()
        nuevo_correo = input("Nuevo correo electrónico: ").strip()
        nuevo_rol = input("Nuevo rol (admin, usuario): ").strip()
        nuevo_estado = input("Nuevo estado ('activa o inactiva'): ").strip()
        # Actualizar los datos del usuario en la base de datos
        query = """
        UPDATE usuarios
        SET nombre_usuario = %s, correo_electronico = %s, rol = %s, estado = %s
        WHERE id = %s
        """
        cursor.execute(query, (nuevo_nombre, nuevo_correo, nuevo_rol, nuevo_estado, id_usuario))
        conexion.commit()

        print("Usuario actualizado exitosamente.")

    except Exception as e:
        print(f"Error al editar el usuario: {e}")

    finally:
        cursor.close()


def eliminar_usuario(conexion):
    """
    Permite eliminar un usuario de la base de datos.
    """
    cursor = conexion.cursor()
    try:
        # Solicitar al administrador el ID del usuario a eliminar
        id_usuario = int(input("Ingresa el ID del usuario a eliminar: ").strip())

        # Confirmar la eliminación
        confirmacion = input(f"¿Estás seguro de eliminar al usuario con ID {id_usuario}? (s/n): ").strip().lower()

        if confirmacion == "s":
            # Eliminar el usuario de la base de datos
            query = "DELETE FROM usuarios WHERE id = %s"
            cursor.execute(query, (id_usuario,))
            conexion.commit()

            print("Usuario eliminado exitosamente.")
        else:
            print("Eliminación cancelada.")

    except Exception as e:
        print(f"Error al eliminar el usuario: {e}")

    finally:
        cursor.close()



    """
    Menú para gestionar planes y asignar uno nuevo a los usuarios.
    """
    cursor = conexion.cursor()
    while True:
        print("\n=== Gestión de Planes ===")
        print("1. Ver usuarios y sus planes")
        print("2. Asignar un nuevo plan a un usuario")
        print("3. Regresar")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            try:
                # Mostrar los usuarios con sus planes
                query = "SELECT id, plan_suscripcion FROM usuarios"
                cursor.execute(query)
                usuarios = cursor.fetchall()

                if usuarios:
                    print("\nUsuarios y sus planes asignados:")
                    print(f"{'ID Usuario':<12}{'Nombre':<20}{'Plan Asignado'}")
                    print("-" * 50)
                    for usuario in usuarios:
                        print(f"{usuario[0]:<12}{usuario[1]:<20}{usuario[2]}")
                else:
                    print("No hay usuarios registrados.")
            except Exception as e:
                print(f"Error al obtener los usuarios: {e}")
        elif opcion == "2":
            try:
                # Mostrar los planes disponibles
                query = "SELECT id, tipo_plan FROM planes"
                cursor.execute(query)
                planes = cursor.fetchall()

                if planes:
                    print("\nPlanes disponibles:")
                    print(f"{'ID Plan':<10}{'Tipo de Plan'}")
                    print("-" * 30)
                    for plan in planes:
                        print(f"{plan[0]:<10}{plan[1]}")
                    
                    id_usuario = int(input("\nID del usuario para asignar el nuevo plan: ").strip())
                    nuevo_plan_id = int(input("ID del nuevo plan a asignar: ").strip())

                    # Verificar si el usuario existe y si el plan es válido
                    query_usuario = "SELECT id FROM usuarios WHERE id = %s"
                    cursor.execute(query_usuario, (id_usuario,))
                    if cursor.fetchone():
                        query_plan = "SELECT id FROM planes WHERE id = %s"
                        cursor.execute(query_plan, (nuevo_plan_id,))
                        if cursor.fetchone():
                            # Asignar el nuevo plan al usuario
                            query_update = "UPDATE usuarios SET id_plan = %s WHERE id = %s"
                            cursor.execute(query_update, (nuevo_plan_id, id_usuario))
                            conexion.commit()
                            print("Plan asignado exitosamente.")
                        else:
                            print("ID de plan no válido.")
                    else:
                        print("ID de usuario no válido.")
            except Exception as e:
                print(f"Error al asignar el plan: {e}")
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intenta nuevamente.")
    cursor.close()

def gestionar_planes(conexion):
    """
    Menú para gestionar planes y asignar uno nuevo a los usuarios.
    """
    cursor = conexion.cursor()
    while True:
        print("\n=== Gestión de Planes ===")
        print("1. Ver usuarios y sus planes")
        print("2. Asignar un nuevo plan a un usuario")
        print("3. Regresar")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            try:
                # Mostrar los usuarios con sus planes asignados
                query = """
                SELECT id, nombre_usuario, plan_suscripcion
                FROM usuarios
                """
                cursor.execute(query)
                usuarios = cursor.fetchall()

                if usuarios:
                    # Crear la tabla con PrettyTable
                    tabla = PrettyTable()
                    tabla.field_names = ["ID Usuario", "Nombre de Usuario", "Plan Asignado"]

                    # Agregar las filas de datos
                    for usuario in usuarios:
                        tabla.add_row([usuario[0], usuario[1], usuario[2]])

                    # Mostrar la tabla
                    print(tabla)
                else:
                    print("No hay usuarios registrados.")
            except Exception as e:
                print(f"Error al obtener los usuarios: {e}")
        
        elif opcion == "2":
            try:
                # Planes disponibles para asignar
                planes_disponibles = ['basico', 'estandar', 'premium']
                print("\nPlanes disponibles para asignar:")
                for idx, plan in enumerate(planes_disponibles, 1):
                    print(f"{idx}. {plan}")

                # Solicitar al administrador el ID del usuario y el plan
                id_usuario = int(input("\nID del usuario para asignar el nuevo plan: ").strip())
                nuevo_plan_idx = int(input(f"Selecciona el número del nuevo plan a asignar (1-{len(planes_disponibles)}): ").strip())

                # Validar la selección del plan
                if 1 <= nuevo_plan_idx <= len(planes_disponibles):
                    nuevo_plan = planes_disponibles[nuevo_plan_idx - 1]

                    # Verificar si el usuario existe
                    query_usuario = "SELECT id FROM usuarios WHERE id = %s"
                    cursor.execute(query_usuario, (id_usuario,))
                    if cursor.fetchone():
                        # Asignar el nuevo plan al usuario
                        query_update = "UPDATE usuarios SET plan_suscripcion = %s WHERE id = %s"
                        cursor.execute(query_update, (nuevo_plan, id_usuario))
                        conexion.commit()
                        print(f"Plan '{nuevo_plan}' asignado exitosamente al usuario con ID {id_usuario}.")
                    else:
                        print("ID de usuario no válido.")
                else:
                    print("Selección de plan no válida.")
            except Exception as e:
                print(f"Error al asignar el plan: {e}")
        
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intenta nuevamente.")
    
    cursor.close()

def agregar_pelicula_serie(conexion):
    """
    Permite al administrador agregar una nueva película o serie.
    """
    cursor = conexion.cursor()

    print("\n=== Agregar Nueva Película o Serie ===")
    
    # Solicitar datos de la película o serie
    titulo = input("Título: ").strip()
    descripcion = input("Descripción: ").strip()
    genero = input("Género (acción, comedia, drama, etc.): ").strip()
    ano_lanzamiento = int(input("Año de lanzamiento: "))
    clasificacion = input("Clasificación (G, PG, R, etc.): ").strip()
    url_portada = input("URL de la portada: ").strip()

    try:
        # Insertar la nueva película o serie en la base de datos
        query = """
        INSERT INTO peliculas_series (titulo, descripcion, genero, ano_lanzamiento, clasificacion, url_portada)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (titulo, descripcion, genero, ano_lanzamiento, clasificacion, url_portada))
        conexion.commit()
        print("Película/Serie agregada exitosamente.")
    except Exception as e:
        print(f"Error al agregar la película/serie: {e}")
    finally:
        cursor.close()


def actualizar_pelicula_serie(conexion):
    """
    Permite al administrador actualizar los detalles de una película o serie existente.
    """
    cursor = conexion.cursor()

    print("\n=== Actualizar Película o Serie ===")

    # Solicitar el ID de la película o serie que desea actualizar
    id_pelicula = int(input("ID de la película o serie a actualizar: "))
    
    # Solicitar nuevos detalles (opcionales)
    nuevo_titulo = input("Nuevo título (opcional): ").strip()
    nueva_descripcion = input("Nueva descripción (opcional): ").strip()
    nuevo_genero = input("Nuevo género (opcional): ").strip()
    nuevo_ano = input("Nuevo año de lanzamiento (opcional): ").strip()
    nueva_clasificacion = input("Nueva clasificación (opcional): ").strip()
    nueva_url_portada = input("Nueva URL de la portada (opcional): ").strip()

    # Crear una lista con los valores a actualizar
    valores = [nuevo_titulo or None, nueva_descripcion or None, nuevo_genero or None, 
               nuevo_ano or None, nueva_clasificacion or None, nueva_url_portada or None, id_pelicula]
    
    try:
        # Query para actualizar los detalles de la película o serie
        query = """
        UPDATE peliculas_series
        SET titulo = COALESCE(%s, titulo),
            descripcion = COALESCE(%s, descripcion),
            genero = COALESCE(%s, genero),
            ano_lanzamiento = COALESCE(%s, ano_lanzamiento),
            clasificacion = COALESCE(%s, clasificacion),
            url_portada = COALESCE(%s, url_portada)
        WHERE id = %s
        """
        cursor.execute(query, valores)
        conexion.commit()
        print("Película/Serie actualizada exitosamente.")
    except Exception as e:
        print(f"Error al actualizar la película/serie: {e}")
    finally:
        cursor.close()


def eliminar_pelicula_serie(conexion):
    """
    Permite al administrador eliminar una película o serie de la biblioteca.
    """
    cursor = conexion.cursor()

    print("\n=== Eliminar Película o Serie ===")

    # Solicitar el ID de la película o serie que desea eliminar
    id_pelicula = int(input("ID de la película o serie a eliminar: "))

    try:
        # Query para eliminar la película o serie
        query = "DELETE FROM peliculas_series WHERE id = %s"
        cursor.execute(query, (id_pelicula,))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Película/Serie eliminada exitosamente.")
        else:
            print("No se encontró una película/serie con ese ID.")
    except Exception as e:
        print(f"Error al eliminar la película/serie: {e}")
    finally:
        cursor.close()




