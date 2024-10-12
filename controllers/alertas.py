from models import db
from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for, session
from sqlalchemy import text
from flask_mail import Message
from twilio.rest import Client  

alertas_bp = Blueprint('alertas', __name__)


@alertas_bp.route('/gestionar_alertas', methods=['GET', 'POST'])
def gestionar_alertas():
    if 'usuarioSesion' not in session:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('auth.login'))

    usuario = session['usuarioSesion']
    idRol = usuario['idRol']

    if idRol != 1:
        return render_template('sin_permisos.html') 

    alertas = db.session.execute(text("SELECT * FROM ALERTAS")).fetchall()
    destinatarios = db.session.execute(text("SELECT * FROM dbo.vw_ProveedoresReqAbas")).fetchall()

    if request.method == 'POST' and request.form.get('action') == 'enviarcorreo':
        from app import mail
        for destinatario in destinatarios:
            email = destinatario[0]
            msg = Message(
                subject="Solicitud de reabastecimiento de producto",
                recipients=[email],
                body=f"Estimado proveedor,\n\n"
                     f"Nos dirigimos a usted para informarle que uno de sus productos, más especificamente el producto: {destinatario[3]} ha alcanzado niveles mínimos de inventario. Confiamos en su excelente servicio para gestionar el reabastecimiento de este artículo a la mayor brevedad posible.\n\n"
                     "Agradecemos su atención y quedamos a su disposición para coordinar la entrega.\n\n"
                     "Atentamente,\n"
                     "Inventario S.A.",
                html=f"""
                    <h1>Reabastecimiento de Producto</h1>
                    <p>Estimados Sres {destinatario[4]}:</p>
                    <p>Le informamos que uno de sus productos, más especificamente el producto: <strong>{destinatario[3]}</strong> ha alcanzado niveles críticos en nuestro inventario.</p>
                    <p>Confiamos en su capacidad para suministrarnos el artículo en cuestión lo antes posible, asegurando la continuidad de nuestras operaciones.</p>
                    <p>Quedamos atentos a cualquier consulta o coordinación que necesite realizar.</p>
                    <p>Atentamente,</p>
                    <p><strong>Inventario S.A.</strong></p>
                """
            )
            try:
                mail.send(msg)
            except Exception as e:
                print(f"Error al enviar el correo a {email}: {e}")

            idAlerta = destinatario[2]
            sql = text("EXEC sp_EliminarAlerta :idAlerta")
            try:
                db.session.execute(sql, {'idAlerta': idAlerta})
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(f"Error al eliminar la alerta: {e}")

        alertas = db.session.execute(text("SELECT * FROM ALERTAS")).fetchall()
        return render_template('gestionar_alertas.html', alertas=alertas, idRol=idRol)

    return render_template('gestionar_alertas.html', alertas=alertas, idRol=idRol)

