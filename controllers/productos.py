from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Productos, Proveedores, Categorias
from datetime import datetime
from sqlalchemy import text

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/producto', methods=['GET', 'POST'])
def gestionar_productos():
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('auth.login'))

    usuario = session['usuarioSesion']
    idUsuario = usuario['idUsuario']
    idRol = usuario['idRol']
    if idRol not in [1, 2]:
        return render_template('sin_permisos.html')
        
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if request.method == 'POST':
        if 'reabastecer' in request.form:
            idProducto_form = request.form.get('idProductoReabastecer')
            cantidad = request.form.get('cantidadReabastecer')

            sql = text("EXEC sp_ReabastecerProducto :idProducto, :cantidad, :idUsuario")
            db.session.execute(sql, {'idProducto': idProducto_form, 'cantidad': cantidad, 'idUsuario': idUsuario})
            db.session.commit()
            flash('Producto reabastecido correctamente')
            return redirect(url_for('productos.gestionar_productos'))

        elif 'guardarProducto' in request.form:
            idProducto_form = request.form.get('idProducto')
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            sku = request.form['sku']
            precioCosto = request.form['precioCosto']
            precioVenta = request.form['precioVenta']
            stockMinimo = request.form['stockMinimo']
            cantidadEnStock = request.form['cantidadEnStock']
            idProveedor = request.form['idProveedor']
            idCategoria = request.form['idCategoria']

            if idProducto_form: 
                producto = Productos.query.get(idProducto_form)
                if producto:
                    producto.nombre = nombre
                    producto.descripcion = descripcion
                    producto.sku = sku
                    producto.precioCosto = precioCosto
                    producto.precioVenta = precioVenta
                    producto.stockMinimo = stockMinimo
                    producto.cantidadEnStock = cantidadEnStock
                    producto.idProveedor = idProveedor
                    producto.idCategoria = idCategoria
                    flash('Producto actualizado correctamente')
                else:
                    flash('Producto no encontrado')
            else: 
                nuevo_producto = Productos(
                    nombre=nombre,
                    descripcion=descripcion,
                    sku=sku,
                    precioCosto=precioCosto,
                    precioVenta=precioVenta,
                    stockMinimo=stockMinimo,
                    cantidadEnStock=cantidadEnStock,
                    idProveedor=idProveedor,
                    idCategoria=idCategoria,
                    fechaCreacion=datetime.utcnow()
                )
                db.session.add(nuevo_producto)
                db.session.commit()
                flash('Producto agregado exitosamente')

            return redirect(url_for('productos.gestionar_productos'))

    proveedores = Proveedores.query.all()
    categorias = Categorias.query.all()
    productos = Productos.query.order_by(Productos.nombre).paginate(page=page, per_page=per_page)
    return render_template('gestionar_productos.html', productos=productos, proveedores=proveedores, categorias=categorias, idRol=idRol)
