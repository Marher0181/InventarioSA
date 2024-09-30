from flask  import Flask, render_template, request, redirect, url_for, session, flash, send_file, Blueprint
from models import db, Categorias, Roles, Usuarios, Proveedores, Productos, MovimientosInventario, Ventas, Productos, DetalleVentas
from io import BytesIO
import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter
from sqlalchemy import text, func

movimientos_bp = Blueprint('movimientos', __name__)

@movimientos_bp.route('/movimientos', methods=['GET'])
def gestionar_movimientos():
    movimientos = db.session.execute(text("SELECT * FROM MovimientosInventario")).fetchall()
    return render_template('gestionar_movimientos.html', movimientos=movimientos)

@movimientos_bp.route('/reporte-productos-mas-vendidos')
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
