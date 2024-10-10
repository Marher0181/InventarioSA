from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models import db, Usuarios
import bcrypt

auth_bp = Blueprint('auth', __name__)

def cifrar_contraseña(contraseña):
    contraseña = contraseña.encode('utf-8')
    sal = bcrypt.gensalt()
    contraseña_cifrada = bcrypt.hashpw(contraseña, sal)
    return contraseña_cifrada

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password').encode('utf-8')

        sql = db.text("EXEC sp_Login :email")
        try:
            result = db.session.execute(sql, {'email': email})
            rows = result.fetchall()
            print(rows)
            if rows:
                user = rows[0]._asdict()
                password_hash = user.get('password').encode('utf-8')
                des = bcrypt.checkpw(password, password_hash)
                if des:
                    rol = user.get('idRol')
                    session['usuarioSesion'] = user
                    flash("Inicio de sesión exitoso.")
                    
                    if rol == 1:
                        return redirect(url_for('dashboards.dashboardAdmin'))
                    elif rol == 2:
                        return redirect(url_for('dashboards.dashboardOperador'))
                else:
                    flash("Error al iniciar sesión.")
            else:
                flash("Error al iniciar Sesión.")
        
        except Exception as e:
            flash(f"Error: {e}")
    
    return render_template('Login.html')



@auth_bp.route('/logout')
def logout():
    session.pop('usuarioSesion', None)
    return redirect(url_for('auth.login'))
