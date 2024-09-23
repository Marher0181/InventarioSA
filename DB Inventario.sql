CREATE DATABASE GestorInventario

USE GestorInventario

CREATE TABLE Categorias(
	idCategoria INT PRIMARY KEY IDENTITY(1,1),
	nombreCategoria VARCHAR(60)
)

CREATE TABLE Roles(
	idRol INT PRIMARY KEY IDENTITY(1,1),
	nombreRol VARCHAR(40) CHECK (nombreRol IN ('Administrador', 'Gerente', 'Operativo'))
)

CREATE TABLE Usuarios (
    idUsuario INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    password NVARCHAR(255) NOT NULL,
    idRol INT,
    fechaRegistro DATETIME DEFAULT GETDATE(),
    activo BIT DEFAULT 1
	CONSTRAINT fk_rol FOREIGN KEY (idRol) REFERENCES Roles(idRol)
);


CREATE TABLE Proveedores (
    idProveedor INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    contacto NVARCHAR(100),
    direccion NVARCHAR(255),
    telefono NVARCHAR(20),
    email NVARCHAR(100),
    fechaRegistro DATETIME DEFAULT GETDATE()
);

CREATE TABLE Productos (
    idProducto INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    descripcion NVARCHAR(255),
    sku NVARCHAR(50) UNIQUE NOT NULL,
    precioCosto DECIMAL(10,2) NOT NULL,
    precioVenta DECIMAL(10,2) NOT NULL,
    stockMinimo INT NOT NULL,
    cantidadEnStock INT NOT NULL,
    idProveedor INT FOREIGN KEY REFERENCES Proveedores(idProveedor),
    idCategoria INT FOREIGN KEY REFERENCES Categorias(idCategoria),
    fechaCreacion DATETIME DEFAULT GETDATE()
);

CREATE TABLE MovimientosInventario (
    idMovimiento INT PRIMARY KEY IDENTITY(1,1),
    idProducto INT FOREIGN KEY REFERENCES Productos(idProducto),
    tipoMovimiento NVARCHAR(20) CHECK (tipoMovimiento IN ('Entrada', 'Salida', 'Ajuste')),
    cantidad INT NOT NULL,
    idUsuario INT FOREIGN KEY REFERENCES Usuarios(idUsuario),
    fechaMovimiento DATETIME DEFAULT GETDATE(),
    motivo NVARCHAR(255) -- Descripción del motivo del movimiento (ej. Venta, Compra, Ajuste de stock)
);

CREATE TABLE Ventas (
    idVenta INT PRIMARY KEY IDENTITY(1,1),
    fechaVenta DATETIME DEFAULT GETDATE(),
    totalVenta DECIMAL(10,2) NOT NULL,
    idUsuario INT FOREIGN KEY REFERENCES Usuarios(idUsuario),
    metodoPago NVARCHAR(50),
    cliente NVARCHAR(100),
    estadoVenta NVARCHAR(20) DEFAULT 'Completada' CHECK (estadoVenta IN ('Completada', 'Cancelada')),
    observaciones NVARCHAR(255) NULL
);

CREATE TABLE DetalleVentas (
    idDetalleVenta INT PRIMARY KEY IDENTITY(1,1),
    idVenta INT FOREIGN KEY REFERENCES Ventas(idVenta),
    idProducto INT FOREIGN KEY REFERENCES Productos(idProducto),
    cantidad INT NOT NULL, 
    precioUnitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2)
);

CREATE OR ALTER PROCEDURE sp_Login(
@email varchar (100),
@password varchar(255)
)
as
begin
	if(exists(SELECT * FROM Usuarios where email = @email AND password = @password AND activo = 1))
		select idUsuario, nombre, idRol FROM Usuarios where email = @email AND password = @password AND activo = 1
	else
		Select '0'
end

CREATE OR ALTER PROCEDURE sp_AgregarUsuario
    @nombre NVARCHAR(100),
    @email NVARCHAR(100),
    @password NVARCHAR(255),
    @idRol INT,
    @activo BIT = 1
AS
BEGIN
    INSERT INTO Usuarios (nombre, email, password, idRol, activo)
    VALUES (@nombre, @email, @password, @idRol, @activo);
END

-- Modificar Usuario
CREATE OR ALTER PROCEDURE sp_ModificarUsuario
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

CREATE OR ALTER PROCEDURE sp_EliminarUsuario
    @idUsuario INT
AS
BEGIN
    UPDATE Usuarios
    SET activo = 0
    WHERE idUsuario = @idUsuario;
END

CREATE OR ALTER PROCEDURE sp_AgregarProveedor
    @nombre NVARCHAR(100),
    @contacto NVARCHAR(100),
    @direccion NVARCHAR(255),
    @telefono NVARCHAR(20),
    @email NVARCHAR(100)
AS
BEGIN
    INSERT INTO Proveedores (nombre, contacto, direccion, telefono, email)
    VALUES (@nombre, @contacto, @direccion, @telefono, @email);
END

-- Modificar Proveedor
CREATE OR ALTER PROCEDURE sp_ModificarProveedor
    @idProveedor INT,
    @nombre NVARCHAR(100),
    @contacto NVARCHAR(100),
    @direccion NVARCHAR(255),
    @telefono NVARCHAR(20),
    @email NVARCHAR(100)
AS
BEGIN
    UPDATE Proveedores
    SET nombre = @nombre, contacto = @contacto, direccion = @direccion, telefono = @telefono, email = @email
    WHERE idProveedor = @idProveedor;
END

-- Eliminar Proveedor
CREATE OR ALTER PROCEDURE sp_EliminarProveedor
    @idProveedor INT
AS
BEGIN
    DELETE FROM Proveedores WHERE idProveedor = @idProveedor;
END

CREATE OR ALTER PROCEDURE sp_AgregarProducto
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

CREATE OR ALTER PROCEDURE sp_ModificarProducto
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

-- Eliminar Producto
CREATE OR ALTER PROCEDURE sp_EliminarProducto
    @idProducto INT
AS
BEGIN
    DELETE FROM Productos WHERE idProducto = @idProducto;
END

CREATE OR ALTER PROCEDURE sp_AgregarMovimientoInventario
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

CREATE OR ALTER PROCEDURE sp_ModificarMovimientoInventario
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

CREATE OR ALTER PROCEDURE sp_EliminarMovimientoInventario
    @idMovimiento INT
AS
BEGIN
    DELETE FROM MovimientosInventario WHERE idMovimiento = @idMovimiento;
END

CREATE OR ALTER PROCEDURE sp_AgregarVenta
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

CREATE OR ALTER PROCEDURE sp_ModificarVenta
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

CREATE OR ALTER PROCEDURE sp_EliminarVenta
    @idVenta INT
AS
BEGIN
    DELETE FROM Ventas WHERE idVenta = @idVenta;
END

CREATE OR ALTER PROCEDURE sp_AgregarDetalleVenta
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

CREATE OR ALTER PROCEDURE sp_ModificarDetalleVenta
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

CREATE OR ALTER PROCEDURE sp_EliminarDetalleVenta
    @idDetalleVenta INT
AS
BEGIN
    DELETE FROM DetalleVentas WHERE idDetalleVenta = @idDetalleVenta;
END
