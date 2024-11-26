from hashlib import sha256

def registrar_cuenta(conexion):
    cursor = conexion.cursor()
    print("\n=== Registrar Nueva Cuenta ===")
    
    nombre = input("Nombre: ")
    apellido = input("Apellido (opcional): ")
    correo = input("Correo: ")
    contrasena = input("Contraseña: ")
    confirmar_contrasena = input("Confirma la Contraseña: ")

    if contrasena != confirmar_contrasena:
        print("\nError: Las contraseñas no coinciden. Intenta nuevamente.")
        return

    # Hashear la contraseña ingresada
    contrasena_hash = sha256(contrasena.encode()).hexdigest()

    try:
        # Obtener el IdPlan para el plan por defecto (por ejemplo, "No Premium")
        query_plan = "SELECT IdPlan FROM Plan WHERE TipoPlan = 'No Premium' LIMIT 1"
        cursor.execute(query_plan)
        plan_resultado = cursor.fetchone()

        if not plan_resultado:
            print("\nError: No se encontró el plan por defecto ('No Premium').")
            return

        id_plan = plan_resultado[0]

        # Insertar datos en la tabla Usuario
        query_usuario = """
        INSERT INTO Usuario (Nombre, Apellido, Correo, IdPlan)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_usuario, (nombre, apellido, correo, id_plan))
        id_usuario = cursor.lastrowid

        # Insertar datos en la tabla Login
        query_login = """
        INSERT INTO Login (IdUsuario, ContrasenaHash)
        VALUES (%s, %s)
        """
        cursor.execute(query_login, (id_usuario, contrasena_hash))

        conexion.commit()
        print(f"\n¡Cuenta creada exitosamente! Ahora puedes iniciar sesión, {nombre}.")

    except Exception as e:
        print(f"\nError al registrar la cuenta: {e}")
        conexion.rollback()
    finally:
        cursor.close()












def iniciar_sesion(conexion):
    """
    Función para iniciar sesión.
    """
    try:
        correo = input("Introduce tu correo: ")
        contrasena = input("Introduce tu contraseña: ")

        # Hashear la contraseña ingresada
        contrasena_hash = sha256(contrasena.encode()).hexdigest()

        cursor = conexion.cursor()
        query = """
        SELECT L.IdUsuario, U.Nombre, U.Apellido, P.TipoPlan 
        FROM Login L
        JOIN Usuario U ON L.IdUsuario = U.IdUsuario
        JOIN Plan P ON U.IdPlan = P.IdPlan
        WHERE U.Correo = %s AND L.ContrasenaHash = %s
        """
        cursor.execute(query, (correo, contrasena_hash))
        usuario = cursor.fetchone()

        if usuario:
            return {"IdUsuario": usuario[0], "Nombre": usuario[1], "Apellido": usuario[2], "TipoPlan": usuario[3]}
        else:
            print("Correo o contraseña incorrectos.")
            return None
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return None
    finally:
        cursor.close()

