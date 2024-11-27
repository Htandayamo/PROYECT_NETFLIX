from hashlib import sha256


def crear_superusuario(conexion, menu_login):
    """
    Función para crear una cuenta de superusuario. Solo ejecutada por desarrolladores o en una configuración inicial.
    """
    cursor = conexion.cursor()
    print("\n=== Crear Superusuario ===")
    
    # Solicitar datos del superusuario
    nombre_usuario = input("Nombre del superusuario: ").strip()
    correo = input("Correo del superusuario: ").strip()
    contrasena = input("Contraseña: ").strip()
    confirmar_contrasena = input("Confirma la contraseña: ").strip()

    # Validar contraseñas
    if contrasena != confirmar_contrasena:
        print("\nError: Las contraseñas no coinciden. Intenta nuevamente.")
        return

    # Hashear la contraseña
    contrasena_hash = sha256(contrasena.encode()).hexdigest()

    try:
        # Insertar datos en la tabla usuarios con rol 'superusuario'
        query_superusuario = """
        INSERT INTO usuarios (nombre_usuario, correo_electronico, contrasena, plan_suscripcion, rol)
        VALUES (%s, %s, %s, 'premium', 'admin')
        """
        cursor.execute(query_superusuario, (nombre_usuario, correo, contrasena_hash))
        conexion.commit()

        print(f"\nSuperusuario {nombre_usuario} creado exitosamente.")

        # Redirigir al menú de inicio de sesión
        print("\nRedirigiendo al menú de inicio de sesión...")
        menu_login(conexion)

    except Exception as e:
        print(f"\nError al crear el superusuario: {e}")
        conexion.rollback()

    finally:
        cursor.close()



def registrar_cuenta(conexion):
    """
    Función para registrar una nueva cuenta con el plan 'básico' por defecto.
    """
    cursor = conexion.cursor()
    print("\n=== Registrar Nueva Cuenta ===")
    
    # Solicitar datos al usuario
    nombre_usuario = input("Nombre de usuario: ").strip()
    correo = input("Correo electrónico: ").strip()
    contrasena = input("Contraseña: ").strip()
    confirmar_contrasena = input("Confirma la Contraseña: ").strip()

    # Validar que las contraseñas coincidan
    if contrasena != confirmar_contrasena:
        print("\nError: Las contraseñas no coinciden. Intenta nuevamente.")
        return

    # Hashear la contraseña ingresada (usando SHA256 en lugar de MD5 por seguridad)
    contrasena_hash = sha256(contrasena.encode()).hexdigest()

    try:
        # Verificar si el correo ya está registrado
        query_correo = "SELECT id FROM usuarios WHERE correo_electronico = %s"
        cursor.execute(query_correo, (correo,))
        if cursor.fetchone():
            print("\nError: Este correo ya fue registrado previamente. Por favor, utiliza otro correo electrónico.")
            return

        # Insertar los datos del nuevo usuario con plan básico por defecto
        query_usuario = """
        INSERT INTO usuarios (nombre_usuario, correo_electronico, contrasena, plan_suscripcion, estado, rol)
        VALUES (%s, %s, %s, 'basico', 'activa', 'usuario')
        """
        cursor.execute(query_usuario, (nombre_usuario, correo, contrasena_hash))
        conexion.commit()

        print(f"\n¡Cuenta creada exitosamente! Ahora puedes iniciar sesión, {nombre_usuario}.")

    except Exception as e:
        print(f"\nError al registrar la cuenta: {e}")
        conexion.rollback()

    finally:
        cursor.close()





def iniciar_sesion(conexion):
    """
    Función para iniciar sesión.
    """
    from hashlib import sha256
    from switch_case import menu_principal, menu_superusuario

    try:
        correo = input("Introduce tu correo: ").strip()
        contrasena = input("Introduce tu contraseña: ").strip()

        # Hashear la contraseña ingresada
        contrasena_hash = sha256(contrasena.encode()).hexdigest()

        cursor = conexion.cursor()  # Usamos el cursor normal
        query = """
        SELECT id, nombre_usuario, plan_suscripcion, rol 
        FROM usuarios 
        WHERE correo_electronico = %s AND contrasena = %s
        """
        cursor.execute(query, (correo, contrasena_hash))
        usuario = cursor.fetchone()

        if usuario:
            # Acceder a los elementos usando índices de la tupla
            print(f"\n¡Bienvenido {usuario[1]}! Tu plan es {usuario[2]} y tu rol es {usuario[3]}.")

            # Verificar el rol y redirigir al menú correspondiente
            if usuario[3] == "usuario":  
                print("\nAccediendo al menú de usuario normal...")
                menu_principal(conexion, usuario)  
            elif usuario[3] == "admin":  # Si el rol es 'admin'
                print("\nAccediendo al menú de Superusuario...")
                menu_superusuario(conexion)  # Llamar al menú de superusuario# Llamar al menú de usuario normal

            return {
                "IdUsuario": usuario[0],
                "NombreUsuario": usuario[1],
                "Plan": usuario[2],
                "Rol": usuario[3]
            }
        else:
            print("\nCorreo o contraseña incorrectos.")
            return None
    except Exception as e:
        print(f"\nError al iniciar sesión: {e}")
        return None
    finally:
        cursor.close()



