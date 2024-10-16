from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import db, Usuarios, Roles
from sqlalchemy import text, func
import bcrypt

usuarios_bp = Blueprint('usuarios', __name__)

def cifrar_contraseña(contraseña):
    contraseña = contraseña.encode('utf-8')
    sal = bcrypt.gensalt()
    contraseña_cifrada = bcrypt.hashpw(contraseña, sal)
    return contraseña_cifrada

@usuarios_bp.route('/usuarios', methods=['GET', 'POST'])
def gestionar_usuarios():
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('auth.login'))

    usuario = session['usuarioSesion']
    idRol = usuario['idRol']
    if idRol not in [1, 2]:
        return render_template('sin_permisos.html')
        
    if request.method == 'POST':
        if idRol == 1:
            action = request.form.get('action')

            if action == 'Agregar':
                nombre = request.form.get('nombre')
                email = request.form.get('email')
                password = request.form.get('password')
                idRol = request.form.get('idRol')
                password_cifrada = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            
                sql = db.text("EXEC sp_AgregarUsuario :nombre, :email, :password, :idRol")
    
                try:
                    db.session.execute(sql, {'nombre': nombre, 'email': email, 'password': password_cifrada, 'idRol': idRol})
                    db.session.commit()
                    flash("Usuario registrado correctamente.")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error al registrar usuario: {e}")

            elif action == 'Modificar':
                idUsuario = request.form.get('idUsuario')
                nombre = request.form.get('nombre')
                email = request.form.get('email')
                password = request.form.get('password')
                idRol = request.form.get('idRol')

                if password:
                    password_cifrada = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    sql = text("EXEC sp_ModificarUsuario :idUsuario, :nombre, :email, :password, :idRol")
                    params = {'idUsuario': idUsuario, 'nombre': nombre, 'email': email, 'password': password_cifrada, 'idRol': idRol}
                else:
                    sql = text("EXEC sp_ModificarUsuarioSinPassword :idUsuario, :nombre, :email, :idRol")
                    params = {'idUsuario': idUsuario, 'nombre': nombre, 'email': email, 'idRol': idRol}

                try:
                    db.session.execute(sql, params)
                    db.session.commit()
                    flash("Usuario modificado correctamente.")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error al modificar usuario: {e}")

            elif idRol == 1 and request.form.get('action') == 'Eliminar':
                idUsuario = request.form.get('idUsuario')
                print(f"ID de usuario a eliminar: {idUsuario}")  # Para depuración

                sql = text("EXEC sp_EliminarUsuario :idUsuario")
                try:
                    db.session.execute(sql, {'idUsuario': idUsuario})
                    db.session.commit()
                    flash("Usuario eliminado correctamente.")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error al eliminar usuario: {e}")

    usuarios = db.session.execute(text("SELECT * FROM Usuarios where Activo != 0")).fetchall()
    roles = db.session.execute(text("SELECT * FROM Roles")).fetchall()

    return render_template('gestionar_usuarios.html', usuarios=usuarios, idRol=idRol, roles=roles)


@usuarios_bp.route('/registrar_usuario', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        password = password.encode('utf-8')  
        sal = bcrypt.gensalt() 
        hashed_password = bcrypt.hashpw(password, sal)
        sql = text("EXEC sp_AgregarUsuario :nombre, :email, :password, :idRol")
        try:
            db.session.execute(sql, {
                'nombre': nombre,
                'email': email,
                'password': hashed_password.decode('utf-8'), 
                'idRol': 1
            })
            db.session.commit()
            flash("Usuario registrado correctamente.")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar usuario: {e}")
    roles = db.session.execute(text("SELECT * FROM Roles")).fetchall()

    return render_template('registrar_usuario.html', roles=roles)

