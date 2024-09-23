from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Categorias(db.Model):
    __tablename__ = 'Categorias'
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombreCategoria = db.Column(db.String(60), nullable=False)

class Roles(db.Model):
    __tablename__ = 'Roles'
    idRol = db.Column(db.Integer, primary_key=True)
    nombreRol = db.Column(db.String(40), nullable=False)

class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    idRol = db.Column(db.Integer, db.ForeignKey('Roles.idRol'), nullable=False)
    fechaRegistro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

class Proveedores(db.Model):
    __tablename__ = 'Proveedores'
    idProveedor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    fechaRegistro = db.Column(db.DateTime, default=datetime.utcnow)

class Productos(db.Model):
    __tablename__ = 'Productos'
    idProducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    sku = db.Column(db.String(50), unique=True, nullable=False)
    precioCosto = db.Column(db.Numeric(10, 2), nullable=False)
    precioVenta = db.Column(db.Numeric(10, 2), nullable=False)
    stockMinimo = db.Column(db.Integer, nullable=False)
    cantidadEnStock = db.Column(db.Integer, nullable=False)
    idProveedor = db.Column(db.Integer, db.ForeignKey('Proveedores.idProveedor'), nullable=False)
    idCategoria = db.Column(db.Integer, db.ForeignKey('Categorias.idCategoria'), nullable=False)
    fechaCreacion = db.Column(db.DateTime, default=datetime.utcnow)

class MovimientosInventario(db.Model):
    __tablename__ = 'MovimientosInventario'
    idMovimiento = db.Column(db.Integer, primary_key=True)
    idProducto = db.Column(db.Integer, db.ForeignKey('Productos.idProducto'), nullable=False)
    tipoMovimiento = db.Column(db.String(20), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuarios.idUsuario'), nullable=False)
    fechaMovimiento = db.Column(db.DateTime, default=datetime.utcnow)
    motivo = db.Column(db.String(255))

class Ventas(db.Model):
    __tablename__ = 'Ventas'
    idVenta = db.Column(db.Integer, primary_key=True)
    fechaVenta = db.Column(db.DateTime, default=datetime.utcnow)
    totalVenta = db.Column(db.Numeric(10, 2), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuarios.idUsuario'), nullable=False)
    metodoPago = db.Column(db.String(50))
    cliente = db.Column(db.String(100))
    estadoVenta = db.Column(db.String(20), default='Completada')
    observaciones = db.Column(db.String(255))

class DetalleVentas(db.Model):
    __tablename__ = 'DetalleVentas'
    idDetalleVenta = db.Column(db.Integer, primary_key=True)
    idVenta = db.Column(db.Integer, db.ForeignKey('Ventas.idVenta'), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey('Productos.idProducto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precioUnitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2))

class Alertas(db.Model):
    __tablename__ = 'Alertas'
    idAlerta = db.Column(db.Integer, primary_key=True)
    idProducto = db.Column(db.Integer, db.ForeignKey('Productos.idProducto'), nullable=False)
    nivelMinimo = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime)