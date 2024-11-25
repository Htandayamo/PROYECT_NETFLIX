import mysql.connector
from prettytable import PrettyTable
from datetime import datetime

# Conexión a la base de datos
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="Netflix"
    )

#----------------------------------------------------------CREATE-----------------------------------------------------------------------

#Define una función llamada crear_plan() 
#que no recibe argumentos. Esta función será la encargada de crear un nuevo plan en la base de datos.
def crear_plan():
    #Solicita al usuario que ingrese el nombre o tipo del plan mediante el comando input().
    #El valor que el usuario ingrese será almacenado en la variable TipoPlan.
    TipoPlan = input("Plan: ")
    Caracteristicas = input("Caracteristicas: ")
    Precio=float(input("Precio:"))
    #Llama a la función conectar()
    conexion = conectar()
    #Crea un objeto cursor utilizando el método .cursor(),
    #se utiliza para ejecutar comando en la base de datos
    cursor = conexion.cursor()
    #ejecutamos la consulta para creae un nuevo registro 
    cursor.execute("INSERT INTO Plan (TipoPlan, Caracteristicas,Precio) VALUES (%s, %s, %s)", (TipoPlan,Caracteristicas,Precio))
    #para guardar los cambios en la base de datos 
    conexion.commit()
    print("Plan creado exitosamente.")
    #cierre de la conexion
    cursor.close()
    conexion.close()

def leer_plan():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT *FROM Plan")
    tabla = PrettyTable()
    tabla.field_names= ["ID", "TipoPlan", "Caracteristicas", "Precio"]

    for (IdPlan, TipoPlan, Caracteristicas, Precio) in cursor.fetchall():
        tabla.add_row([IdPlan, TipoPlan, Caracteristicas, f"${Precio:,.2f}"])
    print(tabla)
    cursor.close()
    conexion.close()


#funcion para crear Usuario
def crear_usuario():
    IdPlan=int(input("IdPlan:"))
    Correo= input("Correo:")
    Contrasena = input("Contrasena:")
    #FechaRegistro=datetime.now(input("FechaRegistro:"))
    FechaRegistro=datetime.now()
    
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO Usuario (IdPlan, Correo, Contrasena, FechaRegistro) VALUES (%s, %s, %s, %s)", (IdPlan,Correo,Contrasena,FechaRegistro))
    conexion.commit()
    print("Usuario creado exitosamente.")
    cursor.close()
    conexion.close()



def leer_usuario():
    conexion = conectar()
    cursor = conexion.cursor()
    # Realizar consulta para obtener todos los usuarios 
    cursor.execute("""SELECT u.IdUsuario,pl.IdPlan, u.Correo, u.Contrasena, u.FechaRegistro, pl.TipoPlan as Plan
    FROM Usuario u
    JOIN Plan pl
    ON u.IdPlan = pl.IdPlan
    ORDER BY u.IdUsuario ASC""")
    # Crear una tabla con PrettyTable
    tabla = PrettyTable()
    # Definir los nombres de las columnas
    tabla.field_names= ["IdUsuario", "IdPlan", "Correo", "Contrasena","FechaRegistro", "Plan"]
    # Agregar las filas de los empleados
    for (IdUsuario, IdPlan, Correo, Contrasena,FechaRegistro,Plan) in cursor.fetchall():
        tabla.add_row([IdUsuario, IdPlan, Correo, Contrasena,FechaRegistro, Plan])
    # Mostrar la tabla
    print(tabla)
    cursor.close()
    conexion.close()


#crear Perfil
def crear_perfil():
    IdUsuario=int(input("IdUsuario:"))
    Ci= input("Ci:")
    Nombre = input("Nombre:")
    ApellidoPaterno=input("ApellidoPaterno:")
    ApellidoMaterno=input("ApellidoMaterno:")
    FechaNacimiento=input("FechaNacimiento:")
    FechaNacimiento=datetime.strptime(FechaNacimiento,"%Y-%m-%d").date()
    Telefono=input("Telefono:")

    conexion=conectar()
    cursor=conexion.cursor()
    cursor.execute("INSERT INTO Perfil (IdUsuario, Ci, Nombre, ApellidoPaterno, ApellidoMaterno,FechaNacimiento,Telefono) VALUES (%s, %s, %s, %s, %s, %s, %s)", (IdUsuario,Ci,Nombre,ApellidoPaterno,ApellidoMaterno,FechaNacimiento,Telefono))
    conexion.commit()
    print("Perfil creado exitosamente.")
    cursor.close()
    conexion.close()

#leer perfil
def leer_perfil():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(""" SELECT p.IdPerfil,u.IdUsuario, p.Ci, p.Nombre, p.ApellidoPaterno, p.ApellidoMaterno,p.FechaNacimiento,p.Telefono
    FROM Perfil p
    JOIN Usuario u
    ON p.IdUsuario = u.IdUsuario""")

    tabla = PrettyTable()
    tabla.field_names= ["IdPerfil", "IdUsuario", "Ci", "Nombre","ApellidoPaterno", "ApellidoMaterno", "FechaNacimiento", "Telefono"]

    for (IdPerfil, IdUsuario, Ci, Nombre,ApellidoPaterno, ApellidoMaterno, FechaNacimiento, Telefono) in cursor.fetchall():
        tabla.add_row([IdPerfil, IdUsuario, Ci, Nombre,ApellidoPaterno, ApellidoMaterno, FechaNacimiento, Telefono])
    print(tabla)
    cursor.close()
    conexion.close()


#crear Categoria
def crear_categoria():
    IdCategoria=int(input("IdCategoria"))
    Nombre= input("Nombre:")
    
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO Categoria (IdCategoria,Nombre) VALUES (%s, %s)", (IdCategoria,Nombre))
    conexion.commit()
    print("Categoria creado exitosamente.")
    cursor.close()
    conexion.close()

#leer Categoria
def leer_categoria():
    conexion=conectar()
    cursor=conexion.cursor()
    cursor.execute("SELECT *FROM Categoria")
    tabla=PrettyTable()
    tabla.field_names=["ID","Nombre"]

    for(IdCategoria,Nombre) in cursor.fetchall():
        tabla.add_row([IdCategoria,Nombre])

    print(tabla)
    cursor.close()
    conexion.close()

#crear Contenido
def crear_contenido():
    IdCategoria=int(input("IdCategoria:"))
    Titulo=input("Titulo:")
    Descripcion=input("Descripcion:")
    NombreCategoria=input("NombreCategoria")
    Anio=int(input("Anio:"))

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO Contenido (IdCategoria,Titulo,Descripcion,NombreCategoria,Anio) VALUES (%s, %s, %s, %s, %s)", (IdCategoria,Titulo,Descripcion,NombreCategoria,Anio))
    conexion.commit()
    print("Contenido creado exitosamente.")
    cursor.close()
    conexion.close()

#leer_contenido
def leer_contenido():
    conexion=conectar()
    cursor=conexion.cursor()
    cursor.execute(""" SELECT c.IdContenido,ca.IdCategoria,c.Titulo,c.Descripcion,c.NombreCategoria,c.Anio,ca.Nombre
    FROM Contenido c
    JOIN Categoria ca
    ON c.IdCategoria = Ca.IdCategoria""")

    tabla = PrettyTable()
    tabla.field_names= ["IdContenido","IdCategoria", "Titulo", "Descripcion", "NombreCategoria","Anio","Nombre"]

    for (IdContenido, IdCategoria,Titulo, Descripcion, NombreCategoria,Anio,Nombre) in cursor.fetchall():
        tabla.add_row([IdContenido,IdCategoria, Titulo, Descripcion, NombreCategoria,Anio,Nombre])

    print(tabla)
    cursor.close()
    conexion.close()

#--------------------------------------------------------UPDATE-----------------------------------------------------------------------
# Función para actualizar un contenido

def actualizar_contenido():
    IdContenido = int(input("IdContenido: "))
    Titulo=input("Titulo:")
    NombreCategoria = input("NombreCategoria: ")
    Anio = int(input("Anio: "))
    
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("UPDATE Contenido SET Titulo = %s, NombreCategoria = %s, Anio = %s WHERE IdContenido = %s", (Titulo,NombreCategoria,Anio,IdContenido))
    conexion.commit()
    
    if cursor.rowcount > 0:
        print("contenido actualizado exitosamente.")
    else:
        print("No se encontró un contenido con ese ID.")
    cursor.close()
    conexion.close()

# Función para actualizar Usuario y perfl
def actualizar_usuario_perfil():
    IdUsuario = int(input("IdUsuario: "))
    Nombre=input("Nombre")
    Correo=input("Correo:")
    
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("UPDATE Usuario u JOIN Perfil p ON p.IdUsuario=u.IdUsuario SET p.Nombre = %s, u.Correo = %s WHERE u.IdUsuario = %s", (Nombre,Correo,IdUsuario))
    conexion.commit()
    
    if cursor.rowcount > 0:
        print("Usuario actualizado exitosamente.")
    else:
        print("No se encontró un Usuario con ese ID.")
    cursor.close()
    conexion.close()


#-----------------------------------------------------------------DELETE--------------------------------------------------------------
# Función para eliminar un usuario
def eliminar_contenido():
    IdContenido = int(input("IdContenido: "))
    
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Contenido WHERE id = %s", (IdContenido,))
    conexion.commit()
    
    if cursor.rowcount > 0:
        print("Contenido eliminado exitosamente.")
    else:
        print("No se encontró un Contenido con ese ID.")
    
    cursor.close()
    conexion.close()

# Función para mostrar el menú
def mostrar_menu():
    while True:
        print("\n-------- NETFLIX -------")
        print("1. Crear plan")
        print("2. Leer plan")
        print("3. Crear Usuario")
        print("4. Leer Usuario")
        print("5. Crear Perfil")
        print("6. Leer Perfil")
        print("7. crear Categoria")
        print("8. Leer Categoria")
        print("9. Crear Contenido")
        print("10. Leer Contenido")
        print("11. Actualizar Contenido")
        print("12. Actualizar UsuarioPerfil")
        print("13. Eliminar Contenido")
        print("14. Eliminar Usuario")
        print("15. Salir")
        
        opcion = input("Elige una opcion ")
        
        if opcion == '1':
            crear_plan()
        elif opcion == '2':
            leer_plan()
        elif opcion == '3':
            crear_usuario()
        elif opcion == '4':
            leer_usuario()
        elif opcion == '5':
            crear_perfil()
        elif opcion == '6':
            leer_perfil()
        elif opcion == '7':
            crear_categoria()
        elif opcion == '8':
            leer_categoria()
        elif opcion == '9':
            crear_contenido()
        elif opcion == '10':
            leer_contenido()    
        elif opcion == '11':
            actualizar_contenido()
        elif opcion == '12':
            actualizar_usuario_perfil()
        elif opcion == '13':
            eliminar_contenido()
        elif opcion == '14':
            print("Saliendo del programa.")
            
        else:
            print("Opción no válida. Intenta nuevamente.")
# Iniciar el menú
if __name__ == "__main__":
    mostrar_menu()

