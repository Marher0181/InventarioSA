from models import db, Productos, Ventas, Productos
from flask  import render_template, request, redirect, url_for, session, flash, Blueprint
from sqlalchemy import text, func

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/ventas', methods=['GET', 'POST'])
def gestionar_ventas():
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('auth.login'))

    usuario = session['usuarioSesion']
    idRol = usuario['idRol']
    query = request.args.get('q')
    page = request.args.get('page', 1, type=int) 
    per_page = 5  

    if query and query != None and query != 'None' :
        productos = Productos.query.filter(
            Productos.nombre.ilike(f'%{query}%') | Productos.descripcion.ilike(f'%{query}%')
        ).order_by(Productos.nombre).paginate(page=page, per_page=per_page) 
    else:
        productos = Productos.query.order_by(Productos.nombre).paginate(page=page, per_page=per_page) 

    usuario = session['usuarioSesion']

    if request.method == 'POST':
        productos_seleccionados = request.form.getlist('productos[]')
        cantidades = request.form.getlist('cantidades[]')
        total_venta = 0

        venta = Ventas(
            idUsuario=usuario['idUsuario'],
            metodoPago=request.form.get('metodoPago'),
            cliente=request.form.get('cliente'),
            observaciones=request.form.get('observaciones'),
            totalVenta=0
        )
        db.session.add(venta)
        db.session.commit()

        for i, idProducto in enumerate(productos_seleccionados):
            producto = Productos.query.get(idProducto)
            cantidad = int(cantidades[i])

            if cantidad > producto.cantidadEnStock:
                flash(f"La cantidad solicitada para {producto.nombre} excede el stock disponible.")
                return redirect(url_for('ventas.gestionar_ventas'))

            subtotal = producto.precioVenta * cantidad
            total_venta += subtotal

            sql = text("INSERT INTO DetalleVentas VALUES (:idVenta, :idProducto, :cantidad, :precioUnitario, :subtotal)")
            db.session.execute(sql, {'idVenta': venta.idVenta, 'idProducto': idProducto, 'cantidad': cantidad, 'precioUnitario': producto.precioVenta, 'subtotal': subtotal})
            print('idVenta', venta.idVenta, 'idProducto', idProducto, 'cantidad', cantidad, 'precioUnitario', producto.precioVenta, 'subtotal', subtotal)
            db.session.commit()
            flash("Usuario modificado correctamente.")

        venta.totalVenta = total_venta
        db.session.commit()

        flash("Venta realizada con éxito.")
        return redirect(url_for('ventas.gestionar_ventas'))

    return render_template('gestionar_ventas.html', productos=productos, idRol=idRol)