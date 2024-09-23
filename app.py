from flask  import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Categorias, Roles, Usuarios, Proveedores, Productos, MovimientosInventario, Ventas, Productos, DetalleVentas
from config import Config
from datetime import datetime
from sqlalchemy import text
import bcrypt
from flask_mail import Mail, Message
from twilio.rest import Client  # Importa Twilio Client

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #password = password.encode('utf-8')
        #sal = bcrypt.gensalt()
        #hashed_password = bcrypt.hashpw(password, sal)
        #password = hashed_password
        sql = db.text("EXEC sp_Login :email, :password")
        print(password)
        try:
            result = db.session.execute(sql, {'email': email, 'password': password})
            rows = result.fetchall()

            if rows:
                user = rows[0]._asdict() 
                rol = user.get('idRol') 
                session['usuarioSesion'] = user
                print(user)
                print(rol, "este es el ROL")
                if rol == 1:
                    return redirect(url_for('dashboardAdmin'))
                elif rol == 2:
                    return redirect(url_for('gestionar_ventas'))
            else:
                flash("No se encontraron resultados o credenciales incorrectas.")

        except Exception as e:
            flash(f"Error: {e}")

    return render_template('Login.html')

@app.route('/logout')
def logout():
    session.pop('usuarioSesion', None)
    return redirect(url_for('login'))

@app.route('/dashboardAdmin')
def dashboardAdmin():
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('login'))
    
    usuario = session['usuarioSesion']
    idRol = usuario['idRol']
    
    if idRol == 1:
        sql = db.text("SELECT COUNT(*) FROM Alertas")
        alertas = db.session.execute(sql).fetchall()
        sql = db.text("SELECT COUNT(*) FROM Ventas")
        ventas = db.session.execute(sql).fetchall()
        sql = db.text("SELECT COUNT(*) FROM Proveedores")
        proveedores = db.session.execute(sql).fetchall()
        sql = db.text("SELECT COUNT(*) FROM MovimientosInventario")
        movimientos = db.session.execute(sql).fetchall()
        sql = db.text("SELECT COUNT(*) FROM Usuarios")
        usuarios = db.session.execute(sql).fetchall()
        return render_template('DashboardAdmin.html', alertas=alertas, ventas=ventas, proveedores=proveedores, usuarios=usuarios, movimientos=movimientos)
    

@app.route('/usuarios', methods=['GET', 'POST'])
def gestionar_usuarios():
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('login'))

    usuario = session['usuarioSesion']
    idRol = usuario['idRol']

    if request.method == 'POST':
        if idRol == 1:
            action = request.form.get('action')

            if action == 'Agregar':
                nombre = request.form.get('nombre')
                email = request.form.get('email')
                password = request.form.get('password')
                idRol = request.form.get('idRol')
                password = password.encode('utf-8')
                sal = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password, sal)
                password = hashed_password
                sql = text("EXEC sp_AgregarUsuario :nombre, :email, :password, :idRol")
                try:
                    db.session.execute(sql, {'nombre': nombre, 'email': email, 'password': password, 'idRol': idRol})
                    db.session.commit()
                    flash("Usuario agregado correctamente.")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error al agregar usuario: {e}")

            elif action == 'Modificar':
                idUsuario = request.form.get('idUsuario')
                nombre = request.form.get('nombre')
                email = request.form.get('email')
                password = request.form.get('password')
                idRol = request.form.get('idRol')

                sql = text("EXEC sp_ModificarUsuario :idUsuario, :nombre, :email, :password, :idRol")
                try:
                    db.session.execute(sql, {'idUsuario': idUsuario, 'nombre': nombre, 'email': email, 'password': password, 'idRol': idRol})
                    db.session.commit()
                    flash("Usuario modificado correctamente.")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error al modificar usuario: {e}")

        elif idRol == 1 and request.form.get('action') == 'Eliminar':
            idUsuario = request.form.get('idUsuario')

            sql = text("EXEC sp_EliminarUsuario :idUsuario")
            try:
                db.session.execute(sql, {'idUsuario': idUsuario})
                db.session.commit()
                flash("Usuario eliminado correctamente.")
            except Exception as e:
                db.session.rollback()
                flash(f"Error al eliminar usuario: {e}")

    usuarios = db.session.execute(text("SELECT * FROM Usuarios")).fetchall()
    roles = db.session.execute(text("SELECT * FROM Roles")).fetchall()

    return render_template('gestionar_usuarios.html', usuarios=usuarios, idRol=idRol, roles=roles)

@app.route('/gestionar_alertas', methods=['GET', 'POST'])
def gestionar_alertas():
    alertas = db.session.execute(text("SELECT * FROM ALERTAS")).fetchall()

    destinatarios = db.session.execute(text("""
        SELECT * from dbo.vw_ProveedoresReqAbas
    """)).fetchall()

    if request.method == 'POST' and request.form.get('action') == 'enviarcorreo': 
        for destinatario in destinatarios:
            email = destinatario[0]
            msg = Message(
                subject="Solicitud de reabastecimiento de producto",
                recipients=[email],
                body="Estimado proveedor,\n\n"
                     "Nos dirigimos a usted para informarle que uno de sus productos, más especificamente el producto: " + destinatario[3] + " ha alcanzado niveles mínimos de inventario. Confiamos en su excelente servicio para gestionar el reabastecimiento de este artículo a la mayor brevedad posible.\n\n"
                     "Agradecemos su atención y quedamos a su disposición para coordinar la entrega.\n\n"
                     "Atentamente,\n"
                     "Inventario S.A.",
                html="""
                    <h1>Reabastecimiento de Producto</h1>
                    <p>Estimado proveedor,</p>
                    <p>Le informamos que uno de sus productos, más especificamente el producto: <strong>""" + destinatario[3] + """ </strong> ha alcanzado niveles críticos en nuestro inventario.</p>
                    <p>Confiamos en su capacidad para suministrarnos el artículo en cuestión lo antes posible, asegurando la continuidad de nuestras operaciones.</p>
                    <p>Quedamos atentos a cualquier consulta o coordinación que necesite realizar.</p>
                    <p>Atentamente,</p>
                    <p><strong>Inventario S.A.</strong></p>
                """
            )
            mail.send(msg)
            idAlerta = destinatario[2]
            print('este es el id alerta', idAlerta)
            sql = text("EXEC sp_EliminarAlerta :idAlerta")
            try:
                db.session.execute(sql, {'idAlerta': idAlerta})
                db.session.commit()
                return render_template('gestionar_alertas.html', alertas=alertas)
            
            except Exception as e:
                db.session.rollback()
                flash(f"Error al eliminar Email: {e}")
                
            
    if request.method == 'POST' and request.form.get('action') == 'enviarwhatsapp':
        for destinatario in destinatarios:
            telefono = destinatario[1]
            mensaje = Client.messages.create(
                body="Estimado proveedor, uno de sus productos ha alcanzado niveles mínimos. Agradecemos el reabastecimiento pronto.",
                from_=app.config['TWILIO_WHATSAPP_FROM'],
                to=f'whatsapp:{telefono}'
            )
            print(f"Mensaje enviado a {telefono}")

    return render_template('gestionar_alertas.html', alertas=alertas)


@app.route('/proveedores', methods=['POST', 'GET'])
def gestionar_proveedores():
    # Verifica si el usuario está autenticado
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('login'))
    
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

    if request.method == 'POST':
        proveedor_id = request.form.get('proveedor_id')
        proveedor = Proveedores.query.get(proveedor_id)
        if proveedor:
            db.session.delete(proveedor)
            db.session.commit()
            flash("Proveedor eliminado exitosamente.")
        else:
            flash("Proveedor no encontrado.")

    usuario = session['usuarioSesion']
    
    return render_template('gestionar_proveedores.html', proveedores=proveedores)

@app.route('/editar_proveedor/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('login'))

    proveedor = Proveedores.query.get_or_404(id)

    if request.method == 'POST':
        proveedor.nombre = request.form['nombre']
        proveedor.direccion = request.form['direccion']
        db.session.commit()
        flash("Proveedor actualizado exitosamente.")
        return redirect(url_for('gestionar_proveedores'))

    return render_template('editar_proveedor.html', proveedor=proveedor)

    

@app.route('/ventas', methods=['GET', 'POST'])
def gestionar_ventas():
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('login'))

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
                return redirect(url_for('gestionar_ventas'))

            subtotal = producto.precioVenta * cantidad
            total_venta += subtotal

            sql = text("INSERT INTO DetalleVentas VALUES (:idVenta, :idProducto, :cantidad, :precioUnitario, :subtotal)")
            db.session.execute(sql, {'idVenta': venta.idVenta, 'idProducto': idProducto, 'cantidad': cantidad, 'precioUnitario': producto.precioVenta, 'subtotal': subtotal})
            db.session.commit()
            flash("Usuario modificado correctamente.")

        venta.totalVenta = total_venta
        db.session.commit()

        flash("Venta realizada con éxito.")
        return redirect(url_for('gestionar_ventas'))

    return render_template('gestionar_ventas.html', productos=productos)


