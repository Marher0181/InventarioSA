
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Categorias, Roles, Usuarios, Proveedores, Productos, MovimientosInventario, Ventas, Productos, DetalleVentas
from sqlalchemy import text
proveedores_bp = Blueprint('proveedores', __name__)

@proveedores_bp.route('/proveedores', methods=['POST', 'GET'])
def gestionar_proveedores():
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('auth.login'))

    query = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if query:
        proveedores = Proveedores.query.filter(
            Proveedores.nombre.ilike(f'%{query}%') |
            Proveedores.direccion.ilike(f'%{query}%')
        ).order_by(Proveedores.nombre).paginate(page=page, per_page=per_page)
    else:
        proveedores = Proveedores.query.order_by(Proveedores.nombre).paginate(page=page, per_page=per_page)

    proveedor_seleccionado = None

    if request.method == 'POST':
        if 'agregar' in request.form:
            # Agregar un nuevo proveedor
            nombre = request.form['nombre']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            email = request.form['email']

            sql = text("EXEC sp_AgregarProveedor :nombre, :direccion, :telefono, :email")
            try:
                db.session.execute(sql, {'nombre': nombre, 'direccion': direccion, 'telefono': telefono, 'email': email})
                db.session.commit()
                flash("Proveedor agregado correctamente.")
                return redirect(url_for('proveedores.gestionar_proveedores'))
            except Exception as e:
                db.session.rollback()
                flash(f"Error al agregar proveedor: {e}")

        elif 'modificar' in request.form:
            proveedor_id = request.form['proveedor_id']
            proveedor = Proveedores.query.get(proveedor_id)
            if proveedor:
                proveedor.nombre = request.form['nombre']
                proveedor.direccion = request.form['direccion']
                proveedor.telefono = request.form['telefono']
                proveedor.email = request.form['email']
                db.session.commit()
                flash("Proveedor modificado exitosamente.")
                return redirect(url_for('proveedores.gestionar_proveedores'))
            else:
                flash("Proveedor no encontrado.")

        elif 'eliminar' in request.form:
            proveedor_id = request.form['proveedor_id']
            proveedor = Proveedores.query.get(proveedor_id)
            if proveedor:
                db.session.delete(proveedor)
                db.session.commit()
                flash("Proveedor eliminado exitosamente.")
                return redirect(url_for('proveedores.gestionar_proveedores'))
            else:
                flash("Proveedor no encontrado.")
        

    return render_template('gestionar_proveedores.html', proveedores=proveedores, proveedor_seleccionado=proveedor_seleccionado)
