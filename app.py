from flask  import Flask, render_template, request, redirect, url_for, session, flash, send_file
from models import db, Categorias, Roles, Usuarios, Proveedores, Productos, MovimientosInventario, Ventas, Productos, DetalleVentas
from config import Config
from datetime import datetime
from sqlalchemy import text, func
import pandas as pd
import bcrypt
from io import BytesIO
import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter
from flask_mail import Mail, Message
from twilio.rest import Client  # Importa Twilio Client

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
mail = Mail(app)

def cifrar_contraseña(contraseña):
    contraseña = contraseña.encode('utf-8')
    sal = bcrypt.gensalt()
    contraseña_cifrada = bcrypt.hashpw(contraseña, sal)
    return contraseña_cifrada

@app.route('/', methods=['GET', 'POST'])
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
                print("este es des  ", des)
                if des:
                    rol = user.get('idRol')
                    session['usuarioSesion'] = user
                    flash("Inicio de sesión exitoso.")
                    
                    if rol == 1:
                        return redirect(url_for('dashboardAdmin'))
                    elif rol == 2:
                        return redirect(url_for('gestionar_ventas'))
                else:
                    flash("Contraseña incorrecta.", "warning")

            else:
                flash("No se encontró el usuario o está inactivo.", "warning")


        except db.exc.OperationalError as e:
            error_code = e.orig.args[0]
            flash(f"Error de conexión. Inténtalo de nuevo más tarde. Código de error: {error_code}", "danger")

        except Exception as e:
            error_code = getattr(e, 'code', 'N/A')
            flash(f"Ha ocurrido un error inesperado. Por favor, intenta más tarde. Código {error_code} {e}",
              "danger")
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
        sql = db.text("SELECT COUNT(*) FROM Productos")
        productos = db.session.execute(sql).fetchall()
        return render_template('DashboardAdmin.html', alertas=alertas, ventas=ventas, proveedores=proveedores, usuarios=usuarios, movimientos=movimientos, productos=productos)
    

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
            print(destinatario[0])
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
                    <p>Estimados Sres """ + destinatario[4]+ """: </p>
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
                
            
            except Exception as e:
                db.session.rollback()
                flash(f"Error al eliminar Email: {e}")
                
        return render_template('gestionar_alertas.html', alertas=alertas)
    
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
                return redirect(url_for('gestionar_proveedores'))
            except Exception as e:
                db.session.rollback()
                flash(f"Error al agregar proveedor: {e}")

        elif 'modificar' in request.form:
            # Modificar un proveedor existente
            proveedor_id = request.form['proveedor_id']
            proveedor = Proveedores.query.get(proveedor_id)
            if proveedor:
                proveedor.nombre = request.form['nombre']
                proveedor.direccion = request.form['direccion']
                proveedor.telefono = request.form['telefono']
                proveedor.email = request.form['email']
                db.session.commit()
                flash("Proveedor modificado exitosamente.")
                return redirect(url_for('gestionar_proveedores'))
            else:
                flash("Proveedor no encontrado.")

        elif 'eliminar' in request.form:
            # Eliminar un proveedor
            proveedor_id = request.form['proveedor_id']
            proveedor = Proveedores.query.get(proveedor_id)
            if proveedor:
                db.session.delete(proveedor)
                db.session.commit()
                flash("Proveedor eliminado exitosamente.")
                return redirect(url_for('gestionar_proveedores'))
            else:
                flash("Proveedor no encontrado.")
        

    return render_template('gestionar_proveedores.html', proveedores=proveedores, proveedor_seleccionado=proveedor_seleccionado)



@app.route('/producto', methods=['GET', 'POST'])
def gestionar_productos():
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('login'))

    usuario = session['usuarioSesion']
    idUsuario = usuario['idUsuario']

    page = request.args.get('page', 1, type=int)
    per_page = 5

    # Reabastecer producto
    if request.method == 'POST' and 'reabastecer' in request.form:
        idProducto_form = request.form.get('idProductoReabastecer')
        cantidad = request.form.get('cantidadReabastecer')

        sql = text("EXEC sp_ReabastecerProducto :idProducto, :cantidad, :idUsuario")
        db.session.execute(sql, {'idProducto': idProducto_form, 'cantidad': cantidad, 'idUsuario': idUsuario})
        db.session.commit()
        flash('Producto reabastecido correctamente')
        return redirect(url_for('gestionar_productos'))

    # Agregar o modificar producto
    if request.method == 'POST' and 'guardarProducto' in request.form:
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
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.sku = sku
            producto.precioCosto = precioCosto
            producto.precioVenta = precioVenta
            producto.stockMinimo = stockMinimo
            producto.cantidadEnStock = cantidadEnStock
            producto.idProveedor = idProveedor
            producto.idCategoria = idCategoria
            db.session.commit()
            flash('Producto actualizado correctamente')
        else:  # Si no hay ID, es un nuevo producto
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
        return redirect(url_for('gestionar_productos'))

    productos = Productos.query.order_by(Productos.nombre).paginate(page=page, per_page=per_page)
    return render_template('gestionar_productos.html', productos=productos)


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



@app.route('/registrar_usuario', methods=['GET', 'POST'])
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
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar usuario: {e}")
    roles = db.session.execute(text("SELECT * FROM Roles")).fetchall()

    return render_template('registrar_usuario.html', roles=roles)


@app.route('/movimientos', methods=['GET'])
def gestionar_movimientos():
    movimientos = db.session.execute(text("SELECT * FROM MovimientosInventario")).fetchall()
    return render_template('gestionar_movimientos.html', movimientos=movimientos)

@app.route('/reporte-productos-mas-vendidos')
def reporte_productos_mas_vendidos():
    productos = [
        {'nombre': 'Producto A', 'cantidad_vendida': 150},
        {'nombre': 'Producto B', 'cantidad_vendida': 100},
        {'nombre': 'Producto C', 'cantidad_vendida': 50},
        {'nombre': 'Producto D', 'cantidad_vendida': 200},
        {'nombre': 'Producto E', 'cantidad_vendida': 75}
    ]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Productos Más Vendidos"

    ws.append(["Producto", "Cantidad Vendida"])

    for producto in productos:
        ws.append([producto['nombre'], producto['cantidad_vendida']])

    chart = BarChart()
    chart.title = "Productos Más Vendidos"
    chart.x_axis.title = "Producto"
    chart.y_axis.title = "Cantidad Vendida"

    data = Reference(ws, min_col=2, min_row=1, max_row=len(productos) + 1)
    categorias = Reference(ws, min_col=1, min_row=2, max_row=len(productos) + 1)

    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categorias)

    ws.add_chart(chart, "E5")


    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="reporte_productos_mas_vendidos.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == '__main__':
    app.run(debug=True)

