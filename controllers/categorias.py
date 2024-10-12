from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import db, Categorias
from sqlalchemy import text
categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/categorias', methods=['GET', 'POST'])
def gestionar_categorias():
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('auth.login'))

    usuario = session['usuarioSesion']
    idRol = usuario['idRol']
    
    if idRol not in [1, 2]:
        return render_template('sin_permisos.html')

    query = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if query:
        categorias = Categorias.query.filter(
            Categorias.nombreCategoria.ilike(f'%{query}%')
        ).order_by(Categorias.nombreCategoria).paginate(page=page, per_page=per_page)
    else:
        categorias = Categorias.query.order_by(Categorias.nombreCategoria).paginate(page=page, per_page=per_page)

    if request.method == 'POST':
        if 'agregar' in request.form:
            nueva_categoria = request.form['Categorias']
            sql = text("EXEC sp_AgregarCategoria :Categorias")
            try:
                db.session.execute(sql, {'Categorias': nueva_categoria})
                db.session.commit()
                flash("Categoría agregada correctamente.")
            except Exception as e:
                db.session.rollback()
                flash(f"Error al agregar categoría: {e}")
            return redirect(url_for('categorias.gestionar_categorias'))

        elif 'modificar' in request.form:
            categoria_id = request.form['categoria_id']
            categoria = Categorias.query.get(categoria_id)
            if categoria:
                categoria.nombreCategoria = request.form['nombreCategoria']
                db.session.commit()
                flash("Categoría modificada exitosamente.")
            else:
                flash("Categoría no encontrada.")
            return redirect(url_for('categorias.gestionar_categorias'))

        elif 'eliminar' in request.form:
            categoria_id = request.form['categoria_id']
            categoria = Categorias.query.get(categoria_id)
            if categoria:
                db.session.delete(categoria)
                db.session.commit()
                flash("Categoría eliminada exitosamente.")
            else:
                flash("Categoría no encontrada.")
            return redirect(url_for('categorias.gestionar_categorias'))

    return render_template('gestionar_categorias.html', categorias=categorias, idRol=idRol)