#-----------ELIMINAR LA BASE DE DATOS---------
DROP DATABASE Netflix;

#-----------CREAR LA BASE DE DATOS------------
CREATE DATABASE Netflix;
USE Netflix;   

CREATE TABLE Plan(
IdPlan BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
TipoPlan VARCHAR(50),
Caracteristicas VARCHAR(100),
Precio FLOAT
);

#CADA USUARIO TIENE UN PLAN (muchos a uno )= M->1
CREATE TABLE Usuario(
IdUsuario BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
IdPlan  BIGINT UNSIGNED NOT NULL,
Correo VARCHAR(50),
Contrasena VARCHAR(50),
FechaRegistro DATETIME,
FOREIGN KEY(IdPlan)REFERENCES Plan(IdPlan)
)ENGINE=InnoDB;


#UN USUARIO PUEDE TENER MULTIPLES PERFILES (uno a muchos) 1->M
CREATE TABLE Perfil(
IdPerfil BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
IdUsuario BIGINT UNSIGNED NOT NULL,
Ci INT UNIQUE,
Nombre VARCHAR(25),
ApellidoPaterno VARCHAR(25),
ApellidoMaterno VARCHAR(25),
FechaNacimiento DATE,
Telefono INT,
FOREIGN KEY(IdUsuario)REFERENCES Usuario(IdUsuario)
);

CREATE TABLE Categoria(
IdCategoria BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
Nombre VARCHAR(25)
);


#CADA CONTENIDO PERTENECE A UNA CATEGORIA
CREATE TABLE Contenido(
IdContenido BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
IdCategoria BIGINT UNSIGNED NOT NULL,
Titulo VARCHAR(50),
Descripcion VARCHAR(250),
NombreCategoria VARCHAR(25),
Anio YEAR,
FOREIGN KEY(IdCategoria)REFERENCES Categoria(IdCategoria)
);

#LOS ESPISODIOS ESTAN VINCULADOS A UN CONTENIDO
CREATE TABLE Episodio(
IdEpisodio BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
IdContenido BIGINT UNSIGNED NOT NULL,
Titulo VARCHAR(25),
Duracion TIME,
FOREIGN KEY(IdContenido)REFERENCES Contenido(IdContenido)
);

#LOS PPERFILES TIENEN UN HISTORIAL DE VIZUALICION DE CONTENIDO(muchos a muchos) M->M
CREATE TABLE Visualizacion(
IdVisualizacion BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
IdPerfil BIGINT UNSIGNED NOT NULL,
IdContenido BIGINT UNSIGNED NOT NULL,
FechaVisualizacion DATE,
TiempoVisto TIME,
FOREIGN KEY(IdPerfil)REFERENCES Perfil(IdPerfil),
FOREIGN KEY(IdContenido)REFERENCES Contenido(IdContenido)
);


#LOS PERFILES PUEDEN DAR CALIFICACIONES ADIFRENTES CONTENIDOS
CREATE TABLE Calificacion(
IdCalificacion BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
IdPerfil BIGINT UNSIGNED NOT NULL,
IdContenido BIGINT UNSIGNED NOT NULL,
Puntuacion INT,
FOREIGN KEY(IdPerfil)REFERENCES Perfil(IdPerfil),
FOREIGN KEY(IdContenido)REFERENCES Contenido(IdContenido)
);

#UN USUARIO PUEDE ACCEDER A LA PLATAFORMA DESDE MULTIPLES DISPOSITIVOS 
CREATE TABLE Dispositivo(
IdDispositivo BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
IdUsuario BIGINT UNSIGNED NOT NULL,
TipoDispositivo VARCHAR(25),
FechaAcceso DATETIME,
FOREIGN KEY(IdUsuario)REFERENCES Usuario(IdUsuario)
);

#LOS PAGOS DE SUSCRIPCION DE CADA USUARIO SE REGISTRAN EN ESTA TABLA 
CREATE TABLE HistorialPago(
IdHistorialPago BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
IdUsuario BIGINT UNSIGNED NOT NULL,
Fecha DATETIME,
Monto FLOAT,
FOREIGN KEY(IdUsuario)REFERENCES Usuario(IdUsuario)
);

show tables;


#------------INSERTANDO DATOS---------------------------
INSERT INTO Plan(TipoPlan,Caracteristicas,Precio)
VALUES('Basico','Puedes ver contenido en 1 dispositivo a la vez',3.99),
      ('Estandar','Puedes ver contenido en 2 dispositivo a la vez',5.99),
      ('Premium','Puedes ver contenido en 4 dispositivo a la vez',7.99);
select *from plan;

INSERT INTO Usuario(IdPlan,Correo,Contrasena,FechaRegistro)
VALUES(1,'graciela.mamani@gmail.com','12345gm','2024/01/01-10:00:00'),
      (2,'efren.duran@gmail.com','123ed','2024/02/01-14:00:00'),
      (3,'henry.tandamayo@gmail.com','12565ht','2024/03/01-13:00:00');
 select *from Usuario;

INSERT INTO Perfil(IdUsuario,Ci,Nombre,ApellidoPaterno,ApellidoMaterno,FechaNacimiento,Telefono)
VALUES(1,'9157838','Graciela','Mamani','Quispe','2000/08/04',63148862),
	  (2,'7474733','Efren','Duran','Mamani','2000/06/03',71424850),
      (3,'6347894','Henry','Tandamayo','Imbago','2001/03/04',72008543);
select *from Perfil;

INSERT INTO Categoria(Nombre)
VALUES('Anime'),
	  ('Comedia'),
      ('Terror');
select *from Categoria;

INSERT INTO Contenido(IdCategoria,Titulo,Descripcion,NombreCategoria,Anio)
VALUES(1,'Amor de Gata','Cuando una chica peculiar se transforma en una gata para llamar la atencion de un amigo','Anime',2000),
	  (2,'Una Pareja de Idiotas','La vida de Lloyd y Harry dos amigos de una estupidez,es un autentico desastre','Comedia',1994),
      (1,'La Masacre de Texas','Un grupo de jovenes se pierden en texas y termina encontrandose con asesinos que los persiguen con motosierra','anime',1974);
select *from Contenido;

INSERT INTO Episodio(IdContenido,Titulo,Duracion)
VALUES(1,'Amor de Gata','01:12:00'),
      (2,'La vida es Bella','01:12:00'),
      (3,'La Reina Del Sur','01:12:00');
select *from Episodio;

INSERT INTO Visualizacion(IdPerfil,IdContenido,FechaVisualizacion,TiempoVisto)
VALUES(1,1,'2024/01/02','20:12'),
      (2,2,'2024/02/15','14:20'),
      (3,3,'2024/03/20','11:00:');
select *from Visualizacion;

INSERT INTO Calificacion(IdPerfil,IdContenido,Puntuacion)
VALUES(1,1,5),
      (2,2,4),
      (3,3,3);
select *from Calificacion;

INSERT INTO Dispositivo(IdUsuario,TipoDispositivo,FechaAcceso)
VALUES(1,'Google Chrome(Windows)','2024/01/03-05:58'),
      (2,'Google Chrome(Windows)','2024/02/12-14:58'),
      (3,'Google Chrome(Windows)','2024/02/14-10:58');
select *from Dispositivo;

INSERT INTO HistorialPago(IdUsuario,Fecha,Monto)
VALUES(1,'2024/01/02-12:54:08',3.99),
      (2,'2024/02/02-11:54:08',5.99),
      (3,'2024/03/02-23:54:08',7.99);
select *from HistorialPago;


#------------CONSULTAS--------------
#obtenga el contenido al que pertenece un episodio
select c.Titulo,c.Descripcion
from Contenido c inner join Episodio e
#on c.IdContenido=e.IdContenido
on e.IdContenido=c.IdContenido
where e.IdEpisodio=3;

#obtener todos los episodios de un contenido
select e.Titulo,e.Duracion
from Episodio e inner join Contenido c
on e.IdContenido=c.IdContenido
where c.Titulo='Amor de Gata';

#leer el Usuario       
SELECT u.IdUsuario,pl.IdPlan, u.Correo, u.Contrasena, u.FechaRegistro, pl.TipoPlan as Plan
FROM Usuario u
JOIN Plan pl
ON u.IdPlan = pl.IdPlan
ORDER BY  u.IdUsuario ASC;

#leer perfil
SELECT p.IdPerfil,u.IdUsuario, p.Ci, p.Nombre, p.ApellidoPaterno, p.ApellidoMaterno,p.FechaNacimiento,p.Telefono
FROM Perfil p
JOIN Usuario u
ON p.IdUsuario = u.IdUsuario;

#leer contenido
SELECT c.IdContenido,c.Titulo,c.Descripcion,c.NombreCategoria,c.Anio,ca.Nombre
    FROM Contenido c
    JOIN Categoria ca
    ON c.IdCategoria = ca.IdCategoria;
    
#------------------------UPDATE--------------------------
#CONTENIDO
UPDATE Contenido 
SET Titulo = 'BlancaNieves', NombreCategoria ='Terror', Anio =2001
WHERE IdContenido =3;

#PERFIL Y USUARIO
UPDATE Usuario u
JOIN Perfil p 
ON p.IdUsuario = u.IdUsuario
SET p.Nombre = 'Pablo', u.Correo = 'Pablo@gmail.com'
WHERE u.IdUsuario = 4;

#mostrar usuario y perfil actualizado
SELECT u.IdUsuario,p.Nombre, u.Correo
FROM Perfil p
JOIN Usuario u
ON p.IdUsuario = u.IdUsuario;
#--------------------------------DELETE---------------------------------









select *from Perfil;
select *from Usuario;




