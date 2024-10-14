from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, Blueprint
from models import db
from sqlalchemy import text, func
dashboards_bp = Blueprint('dashboards', __name__)

@dashboards_bp.route('/dashboardAdmin')
def dashboardAdmin():
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('login'))
    
    usuario = session['usuarioSesion']
    idRol = usuario['idRol']
    if idRol not in [1]:
        return render_template('sin_permisos.html')

    if idRol == 1:
        sql = db.text("SELECT COUNT(*) FROM Alertas")
        alertas = db.session.execute(sql).fetchall()
        sql = db.text("SELECT COUNT(*) FROM Ventas")
        ventas = db.session.execute(sql).fetchall()
        sql = db.text("SELECT COUNT(*) FROM Proveedores")
        proveedores = db.session.execute(sql).fetchall()
        sql = db.text("SELECT COUNT(*) FROM MovimientosInventario")
        movimientos = db.session.execute(sql).fetchall()
        sql = db.text("SELECT COUNT(*) FROM Usuarios where Activo = 1")
        usuarios = db.session.execute(sql).fetchall()
        sql = db.text("SELECT COUNT(*) FROM Productos")
        productos = db.session.execute(sql).fetchall()
        sql = db.text("SELECT COUNT(*) FROM Categorias")
        categorias = db.session.execute(sql).fetchall()

        return render_template('DashboardAdmin.html', alertas=alertas, ventas=ventas, proveedores=proveedores, usuarios=usuarios, movimientos=movimientos, productos=productos, categorias=categorias, idRol=idRol)

@dashboards_bp.route('/dashboardGerente')
def dashboardGerente():
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('login'))

    usuario = session['usuarioSesion']
    idRol = usuario['idRol']
    
    if idRol not in [1, 2]:
        return render_template('sin_permisos.html')

    if idRol == 2:
        sql = db.text("SELECT COUNT(*) FROM Ventas")
        ventas = db.session.execute(sql).fetchall()
        sql = db.text("SELECT COUNT(*) FROM Proveedores")
        proveedores = db.session.execute(sql).fetchall()
        sql = db.text("SELECT COUNT(*) FROM Productos")
        productos = db.session.execute(sql).fetchall()
        sql = db.text("SELECT COUNT(*) FROM Categorias")
        categorias = db.session.execute(sql).fetchall()
        return render_template('DashboardGerente.html', ventas=ventas,
                               proveedores=proveedores, productos=productos, idRol=idRol, categorias=categorias)