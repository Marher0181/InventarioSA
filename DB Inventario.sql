USE [master]
GO
/****** Object:  Database [GestorInventario]    Script Date: 30/09/2024 09:57:00 p. m. ******/
CREATE DATABASE [GestorInventario]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'GestorInventario', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\GestorInventario.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'GestorInventario_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\GestorInventario_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [GestorInventario] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [GestorInventario].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [GestorInventario] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [GestorInventario] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [GestorInventario] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [GestorInventario] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [GestorInventario] SET ARITHABORT OFF 
GO
ALTER DATABASE [GestorInventario] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [GestorInventario] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [GestorInventario] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [GestorInventario] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [GestorInventario] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [GestorInventario] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [GestorInventario] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [GestorInventario] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [GestorInventario] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [GestorInventario] SET  ENABLE_BROKER 
GO
ALTER DATABASE [GestorInventario] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [GestorInventario] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [GestorInventario] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [GestorInventario] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [GestorInventario] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [GestorInventario] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [GestorInventario] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [GestorInventario] SET RECOVERY FULL 
GO
ALTER DATABASE [GestorInventario] SET  MULTI_USER 
GO
ALTER DATABASE [GestorInventario] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [GestorInventario] SET DB_CHAINING OFF 
GO
ALTER DATABASE [GestorInventario] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [GestorInventario] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [GestorInventario] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [GestorInventario] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'GestorInventario', N'ON'
GO
ALTER DATABASE [GestorInventario] SET QUERY_STORE = ON
GO
ALTER DATABASE [GestorInventario] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [GestorInventario]
GO
/****** Object:  User [ADMINMH]    Script Date: 30/09/2024 09:57:00 p. m. ******/
CREATE USER [ADMINMH] FOR LOGIN [ADMINMH] WITH DEFAULT_SCHEMA=[dbo]
GO
ALTER ROLE [db_owner] ADD MEMBER [ADMINMH]
GO
/****** Object:  Table [dbo].[Alertas]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Alertas](
	[idAlerta] [int] IDENTITY(1,1) NOT NULL,
	[idProducto] [int] NULL,
	[nivelMinimo] [int] NULL,
	[fecha] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[idAlerta] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Proveedores]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Proveedores](
	[idProveedor] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [nvarchar](100) NOT NULL,
	[direccion] [nvarchar](255) NULL,
	[telefono] [nvarchar](20) NULL,
	[email] [nvarchar](100) NULL,
	[fechaRegistro] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[idProveedor] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Productos]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Productos](
	[idProducto] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [nvarchar](100) NOT NULL,
	[descripcion] [nvarchar](255) NULL,
	[sku] [nvarchar](50) NOT NULL,
	[precioCosto] [decimal](10, 2) NOT NULL,
	[precioVenta] [decimal](10, 2) NOT NULL,
	[stockMinimo] [int] NOT NULL,
	[cantidadEnStock] [int] NOT NULL,
	[idProveedor] [int] NULL,
	[idCategoria] [int] NULL,
	[fechaCreacion] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[idProducto] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[sku] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  View [dbo].[vw_DestinatariosAlerta]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[vw_DestinatariosAlerta]
AS
SELECT p.email FROM Alertas
INNER JOIN Productos ON Productos.idProducto = Alertas.idProducto
INNER JOIN Proveedores p ON p.idProveedor = Productos.idProducto
GO
/****** Object:  Table [dbo].[MovimientosInventario]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[MovimientosInventario](
	[idMovimiento] [int] IDENTITY(1,1) NOT NULL,
	[idProducto] [int] NULL,
	[tipoMovimiento] [nvarchar](20) NULL,
	[cantidad] [int] NOT NULL,
	[idUsuario] [int] NULL,
	[fechaMovimiento] [datetime] NULL,
	[motivo] [nvarchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[idMovimiento] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  View [dbo].[vw_ProductosMenosVendidos]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[vw_ProductosMenosVendidos]
AS
SELECT TOP(10) p.nombre, SUM(mi.cantidad) as cantidad_vendida
        FROM MovimientosInventario mi
        JOIN Productos p ON mi.idProducto = p.idProducto
        WHERE mi.tipoMovimiento = 'Salida'
        GROUP BY p.nombre
        ORDER BY cantidad_vendida ASC
GO
/****** Object:  View [dbo].[vw_ProductosMasVendidos]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[vw_ProductosMasVendidos]
AS
SELECT TOP(10) p.nombre, SUM(mi.cantidad) as cantidad_vendida
        FROM MovimientosInventario mi
        JOIN Productos p ON mi.idProducto = p.idProducto
        WHERE mi.tipoMovimiento = 'Salida'
        GROUP BY p.nombre
        ORDER BY cantidad_vendida DESC
GO
/****** Object:  Table [dbo].[Usuarios]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Usuarios](
	[idUsuario] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [nvarchar](100) NOT NULL,
	[email] [nvarchar](100) NOT NULL,
	[password] [varchar](max) NULL,
	[idRol] [int] NULL,
	[fechaRegistro] [datetime] NULL,
	[activo] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[idUsuario] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  View [dbo].[vw_Top10Operadores]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[vw_Top10Operadores]
AS
select TOP(10) u.nombre, count(*) as Ventas_Realizadas from MovimientosInventario
INNER JOIN Usuarios u ON MovimientosInventario.idUsuario = u.idUsuario
WHERE tipoMovimiento = 'Salida'
GROUP BY u.nombre
GO
/****** Object:  View [dbo].[vw_ProveedoresReqAbas]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[vw_ProveedoresReqAbas]
AS
    SELECT Proveedores.email, Proveedores.telefono, alertas.idAlerta, productos.nombre, Proveedores.nombre AS Nombre_Proveedor
    FROM Alertas
    INNER JOIN Productos ON Alertas.idProducto = Productos.idProducto
    INNER JOIN Proveedores ON Productos.idProveedor = Proveedores.idProveedor;
GO
/****** Object:  Table [dbo].[Categorias]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Categorias](
	[idCategoria] [int] IDENTITY(1,1) NOT NULL,
	[nombreCategoria] [varchar](60) NULL,
PRIMARY KEY CLUSTERED 
(
	[idCategoria] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[DetalleVentas]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DetalleVentas](
	[idDetalleVenta] [int] IDENTITY(1,1) NOT NULL,
	[idVenta] [int] NULL,
	[idProducto] [int] NULL,
	[cantidad] [int] NOT NULL,
	[precioUnitario] [decimal](10, 2) NOT NULL,
	[subtotal] [decimal](10, 2) NULL,
PRIMARY KEY CLUSTERED 
(
	[idDetalleVenta] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Roles]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Roles](
	[idRol] [int] IDENTITY(1,1) NOT NULL,
	[nombreRol] [varchar](40) NULL,
PRIMARY KEY CLUSTERED 
(
	[idRol] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Ventas]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Ventas](
	[idVenta] [int] IDENTITY(1,1) NOT NULL,
	[fechaVenta] [datetime] NULL,
	[totalVenta] [decimal](10, 2) NOT NULL,
	[idUsuario] [int] NULL,
	[metodoPago] [nvarchar](50) NULL,
	[cliente] [nvarchar](100) NULL,
	[estadoVenta] [nvarchar](20) NULL,
	[observaciones] [nvarchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[idVenta] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Alertas] ADD  DEFAULT ((10)) FOR [nivelMinimo]
GO
ALTER TABLE [dbo].[Alertas] ADD  DEFAULT (getdate()) FOR [fecha]
GO
ALTER TABLE [dbo].[MovimientosInventario] ADD  DEFAULT (getdate()) FOR [fechaMovimiento]
GO
ALTER TABLE [dbo].[Productos] ADD  DEFAULT (getdate()) FOR [fechaCreacion]
GO
ALTER TABLE [dbo].[Proveedores] ADD  DEFAULT (getdate()) FOR [fechaRegistro]
GO
ALTER TABLE [dbo].[Usuarios] ADD  DEFAULT (getdate()) FOR [fechaRegistro]
GO
ALTER TABLE [dbo].[Usuarios] ADD  DEFAULT ((1)) FOR [activo]
GO
ALTER TABLE [dbo].[Ventas] ADD  DEFAULT (getdate()) FOR [fechaVenta]
GO
ALTER TABLE [dbo].[Ventas] ADD  DEFAULT ('Completada') FOR [estadoVenta]
GO
ALTER TABLE [dbo].[Alertas]  WITH CHECK ADD  CONSTRAINT [fk_producto] FOREIGN KEY([idProducto])
REFERENCES [dbo].[Productos] ([idProducto])
GO
ALTER TABLE [dbo].[Alertas] CHECK CONSTRAINT [fk_producto]
GO
ALTER TABLE [dbo].[DetalleVentas]  WITH CHECK ADD FOREIGN KEY([idProducto])
REFERENCES [dbo].[Productos] ([idProducto])
GO
ALTER TABLE [dbo].[DetalleVentas]  WITH CHECK ADD FOREIGN KEY([idVenta])
REFERENCES [dbo].[Ventas] ([idVenta])
GO
ALTER TABLE [dbo].[MovimientosInventario]  WITH CHECK ADD FOREIGN KEY([idProducto])
REFERENCES [dbo].[Productos] ([idProducto])
GO
ALTER TABLE [dbo].[MovimientosInventario]  WITH CHECK ADD FOREIGN KEY([idUsuario])
REFERENCES [dbo].[Usuarios] ([idUsuario])
GO
ALTER TABLE [dbo].[Productos]  WITH CHECK ADD FOREIGN KEY([idCategoria])
REFERENCES [dbo].[Categorias] ([idCategoria])
GO
ALTER TABLE [dbo].[Productos]  WITH CHECK ADD FOREIGN KEY([idProveedor])
REFERENCES [dbo].[Proveedores] ([idProveedor])
GO
ALTER TABLE [dbo].[Usuarios]  WITH CHECK ADD  CONSTRAINT [fk_rol] FOREIGN KEY([idRol])
REFERENCES [dbo].[Roles] ([idRol])
GO
ALTER TABLE [dbo].[Usuarios] CHECK CONSTRAINT [fk_rol]
GO
ALTER TABLE [dbo].[Ventas]  WITH CHECK ADD FOREIGN KEY([idUsuario])
REFERENCES [dbo].[Usuarios] ([idUsuario])
GO
ALTER TABLE [dbo].[MovimientosInventario]  WITH CHECK ADD CHECK  (([tipoMovimiento]='Ajuste' OR [tipoMovimiento]='Salida' OR [tipoMovimiento]='Entrada'))
GO
ALTER TABLE [dbo].[Roles]  WITH CHECK ADD CHECK  (([nombreRol]='Operativo' OR [nombreRol]='Gerente' OR [nombreRol]='Administrador'))
GO
ALTER TABLE [dbo].[Ventas]  WITH CHECK ADD CHECK  (([estadoVenta]='Cancelada' OR [estadoVenta]='Completada'))
GO
/****** Object:  StoredProcedure [dbo].[sp_AgregarDetalleVenta]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[sp_AgregarDetalleVenta]
    @idVenta INT,
    @idProducto INT,
    @cantidad INT,
    @precioUnitario DECIMAL(10, 2),
    @subtotal DECIMAL(10, 2)
AS
BEGIN
    INSERT INTO DetalleVentas (idVenta, idProducto, cantidad, precioUnitario, subtotal)
    VALUES (@idVenta, @idProducto, @cantidad, @precioUnitario, @subtotal);
END
GO
/****** Object:  StoredProcedure [dbo].[sp_AgregarMovimientoInventario]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[sp_AgregarMovimientoInventario]
    @idProducto INT,
    @tipoMovimiento NVARCHAR(20),
    @cantidad INT,
    @idUsuario INT,
    @motivo NVARCHAR(255)
AS
BEGIN
    INSERT INTO MovimientosInventario (idProducto, tipoMovimiento, cantidad, idUsuario, motivo)
    VALUES (@idProducto, @tipoMovimiento, @cantidad, @idUsuario, @motivo);
END
GO
/****** Object:  StoredProcedure [dbo].[sp_AgregarProducto]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[sp_AgregarProducto]
    @nombre NVARCHAR(100),
    @descripcion NVARCHAR(255),
    @sku NVARCHAR(50),
    @precioCosto DECIMAL(10, 2),
    @precioVenta DECIMAL(10, 2),
    @stockMinimo INT,
    @cantidadEnStock INT,
    @idProveedor INT,
    @idCategoria INT
AS
BEGIN
    INSERT INTO Productos (nombre, descripcion, sku, precioCosto, precioVenta, stockMinimo, cantidadEnStock, idProveedor, idCategoria)
    VALUES (@nombre, @descripcion, @sku, @precioCosto, @precioVenta, @stockMinimo, @cantidadEnStock, @idProveedor, @idCategoria);
END
GO
/****** Object:  StoredProcedure [dbo].[sp_AgregarProveedor]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[sp_AgregarProveedor]
    @nombre NVARCHAR(100),
    @direccion NVARCHAR(255),
    @telefono NVARCHAR(20),
    @email NVARCHAR(100)
AS
BEGIN
    INSERT INTO Proveedores (nombre, direccion, telefono, email)
    VALUES (@nombre, @direccion, @telefono, @email);
END
GO
/****** Object:  StoredProcedure [dbo].[sp_AgregarUsuario]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[sp_AgregarUsuario]
    @nombre NVARCHAR(100),
    @email NVARCHAR(100),
    @password NVARCHAR(max),
    @idRol INT,
    @activo BIT = 1
AS
BEGIN
    INSERT INTO Usuarios (nombre, email, password, idRol, activo)
    VALUES (@nombre, @email, @password, @idRol, @activo);
END
GO
/****** Object:  StoredProcedure [dbo].[sp_AgregarVenta]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[sp_AgregarVenta]
    @totalVenta DECIMAL(10, 2),
    @idUsuario INT,
    @metodoPago NVARCHAR(50),
    @cliente NVARCHAR(100),
    @estadoVenta NVARCHAR(20),
    @observaciones NVARCHAR(255)
AS
BEGIN
    INSERT INTO Ventas (totalVenta, idUsuario, metodoPago, cliente, estadoVenta, observaciones)
    VALUES (@totalVenta, @idUsuario, @metodoPago, @cliente, @estadoVenta, @observaciones);
END
GO
/****** Object:  StoredProcedure [dbo].[sp_EliminarAlerta]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[sp_EliminarAlerta]
@idAlerta INT
AS
BEGIN 
DELETE FROM Alertas 
WHERE idAlerta = @idAlerta
END
GO
/****** Object:  StoredProcedure [dbo].[sp_EliminarDetalleVenta]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[sp_EliminarDetalleVenta]
    @idDetalleVenta INT
AS
BEGIN
    DELETE FROM DetalleVentas WHERE idDetalleVenta = @idDetalleVenta;
END
GO
/****** Object:  StoredProcedure [dbo].[sp_EliminarMovimientoInventario]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[sp_EliminarMovimientoInventario]
    @idMovimiento INT
AS
BEGIN
    DELETE FROM MovimientosInventario WHERE idMovimiento = @idMovimiento;
END
GO
/****** Object:  StoredProcedure [dbo].[sp_EliminarProducto]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- Eliminar Producto
CREATE   PROCEDURE [dbo].[sp_EliminarProducto]
    @idProducto INT
AS
BEGIN
    DELETE FROM Productos WHERE idProducto = @idProducto;
END
GO
/****** Object:  StoredProcedure [dbo].[sp_EliminarUsuario]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[sp_EliminarUsuario]
    @idUsuario INT
AS
BEGIN
    UPDATE Usuarios
    SET activo = 0
    WHERE idUsuario = @idUsuario;
END
GO
/****** Object:  StoredProcedure [dbo].[sp_EliminarVenta]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[sp_EliminarVenta]
    @idVenta INT
AS
BEGIN
    DELETE FROM Ventas WHERE idVenta = @idVenta;
END
GO
/****** Object:  StoredProcedure [dbo].[sp_Login]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[sp_Login]
    @Email NVARCHAR(100)
AS
BEGIN
    SELECT idUsuario, nombre, idRol, password 
    FROM Usuarios 
    WHERE email = @Email AND activo = 1
END
GO
/****** Object:  StoredProcedure [dbo].[sp_ModificarDetalleVenta]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[sp_ModificarDetalleVenta]
    @idDetalleVenta INT,
    @idVenta INT,
    @idProducto INT,
    @cantidad INT,
    @precioUnitario DECIMAL(10, 2),
    @subtotal DECIMAL(10, 2)
AS
BEGIN
    UPDATE DetalleVentas
    SET idVenta = @idVenta, idProducto = @idProducto, cantidad = @cantidad, precioUnitario = @precioUnitario, subtotal = @subtotal
    WHERE idDetalleVenta = @idDetalleVenta;
END
GO
/****** Object:  StoredProcedure [dbo].[sp_ModificarMovimientoInventario]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[sp_ModificarMovimientoInventario]
    @idMovimiento INT,
    @idProducto INT,
    @tipoMovimiento NVARCHAR(20),
    @cantidad INT,
    @idUsuario INT,
    @motivo NVARCHAR(255)
AS
BEGIN
    UPDATE MovimientosInventario
    SET idProducto = @idProducto, tipoMovimiento = @tipoMovimiento, cantidad = @cantidad, idUsuario = @idUsuario, motivo = @motivo
    WHERE idMovimiento = @idMovimiento;
END
GO
/****** Object:  StoredProcedure [dbo].[sp_ModificarProducto]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[sp_ModificarProducto]
    @idProducto INT,
    @nombre NVARCHAR(100),
    @descripcion NVARCHAR(255),
    @sku NVARCHAR(50),
    @precioCosto DECIMAL(10, 2),
    @precioVenta DECIMAL(10, 2),
    @stockMinimo INT,
    @cantidadEnStock INT,
    @idProveedor INT,
    @idCategoria INT
AS
BEGIN
    UPDATE Productos
    SET nombre = @nombre, descripcion = @descripcion, sku = @sku, precioCosto = @precioCosto, precioVenta = @precioVenta, stockMinimo = @stockMinimo, cantidadEnStock = @cantidadEnStock, idProveedor = @idProveedor, idCategoria = @idCategoria
    WHERE idProducto = @idProducto;
END
GO
/****** Object:  StoredProcedure [dbo].[sp_ModificarProveedor]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[sp_ModificarProveedor]
    @idProveedor INT,
    @nombre NVARCHAR(100),
    @direccion NVARCHAR(255),
    @telefono NVARCHAR(20),
    @email NVARCHAR(100)
AS
BEGIN
    UPDATE Proveedores
    SET nombre = @nombre, direccion = @direccion, telefono = @telefono, email = @email
    WHERE idProveedor = @idProveedor;
END
GO
/****** Object:  StoredProcedure [dbo].[sp_ModificarUsuario]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[sp_ModificarUsuario]
    @idUsuario INT,
    @nombre NVARCHAR(100),
    @email NVARCHAR(100),
    @password NVARCHAR(255),
    @idRol INT,
    @activo BIT = 1
AS
BEGIN
    UPDATE Usuarios
    SET nombre = @nombre, email = @email, password = @password, idRol = @idRol, activo = @activo
    WHERE idUsuario = @idUsuario;
END
GO
/****** Object:  StoredProcedure [dbo].[sp_ModificarVenta]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[sp_ModificarVenta]
    @idVenta INT,
    @totalVenta DECIMAL(10, 2),
    @idUsuario INT,
    @metodoPago NVARCHAR(50),
    @cliente NVARCHAR(100),
    @estadoVenta NVARCHAR(20),
    @observaciones NVARCHAR(255)
AS
BEGIN
    UPDATE Ventas
    SET totalVenta = @totalVenta, idUsuario = @idUsuario, metodoPago = @metodoPago, cliente = @cliente, estadoVenta = @estadoVenta, observaciones = @observaciones
    WHERE idVenta = @idVenta;
END
GO
/****** Object:  StoredProcedure [dbo].[sp_ReabastecerProducto]    Script Date: 30/09/2024 09:57:00 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [dbo].[sp_ReabastecerProducto]
    @idProducto INT,
    @cantidad INT,
    @idUsuario INT
AS
BEGIN
    -- Inicia una transacción
    BEGIN TRANSACTION;

    BEGIN TRY
        UPDATE Productos
        SET cantidadEnStock = cantidadEnStock + @cantidad
        WHERE idProducto = @idProducto;

        INSERT INTO MovimientosInventario (idProducto, tipoMovimiento, cantidad, idUsuario, fechaMovimiento, motivo)
        VALUES (@idProducto, 'ENTRADA', @cantidad, @idUsuario, GETDATE(), 'Reabastecimiento Producto');

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
		PRINT 'ERROR AL REABASTECER PRODUCTO'
    END CATCH;
END;
GO
USE [master]
GO
ALTER DATABASE [GestorInventario] SET  READ_WRITE 
GO
