from flask import Flask
from models import db
from config import Config
from flask_mail import Mail
from controllers.auth import auth_bp
from controllers.usuarios import usuarios_bp
from controllers.categorias import categorias_bp
from controllers.dashboards import dashboards_bp
from controllers.movimientos import movimientos_bp
from controllers.productos import productos_bp
from controllers.proveedores import proveedores_bp
from controllers.alertas import alertas_bp
from controllers.ventas import ventas_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

mail = Mail(app)
app.register_blueprint(auth_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(proveedores_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(dashboards_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(movimientos_bp)
app.register_blueprint(alertas_bp)
app.register_blueprint(ventas_bp)

if __name__ == '__main__':
    app.run(debug=True)
