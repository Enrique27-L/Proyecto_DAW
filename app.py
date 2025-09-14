# app.py conectar mysql.connectro via conexion/conexion.py
from flask import Flask, render_template, request, redirect, url_for, flash
from conexion.conexion import conexion, cerrar_conexion
from forms import ProductoForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'  # en producción usa variable de entorno

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

@app.route('/')
def index():
    return render_template('index.html', title='Inicio')

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}'

@app.route('/about/')
def about():
    return render_template('about.html', title='Acerca de')

# ---- Productos ----
@app.route('/productos')
def listar_productos():
    q = request.args.get('q', '').strip()
    conn = conexion()
    cur = conn.cursor(dictionary=True)
    if q:
        cur.execute("SELECT id, nombre, cantidad, precio FROM productos WHERE nombre LIKE %s", (f"%{q}%",))
    else:
        cur.execute("SELECT id, nombre, cantidad, precio FROM productos")
    productos = cur.fetchall()
    cerrar_conexion(conn)
    return render_template('productos/list.html', title='Productos', productos=productos, q=q)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def crear_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = conexion()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)",
                (form.nombre.data, form.cantidad.data, float(form.precio.data))
            )
            conn.commit()
            flash('Producto agregado correctamente.', 'success')
            return redirect(url_for('listar_productos'))
        except Exception as e:
            conn.rollback()
            form.nombre.errors.append('No se pudo guardar: ' + str(e))
        finally:
            cerrar_conexion(conn)
    return render_template('productos/formulario.html', title='Nuevo producto', form=form, modo='crear')

@app.route('/productos/<int:pid>/editar', methods=['GET', 'POST'])
def editar_producto(pid):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, cantidad, precio FROM productos WHERE id = %s", (pid,))
    prod = cursor.fetchone()
    if not prod:
        cerrar_conexion(conn)
        return "Producto no encontrado", 404
    form = ProductoForm(data={'nombre': prod['nombre'], 'cantidad': prod['cantidad'], 'precio': prod['precio']})
    if form.validate_on_submit():
        nombre = form.nombre.data.strip()
        cantidad = form.cantidad.data
        precio = form.precio.data
        try:
            cursor2 = conn.cursor()
            cursor2.execute("UPDATE productos SET nombre=%s, cantidad=%s, precio=%s WHERE id=%s", 
                            (nombre, cantidad, precio, pid))
            conn.commit()
            flash('Producto actualizado correctamente.', 'success')
            return redirect(url_for('listar_productos'))
        except Exception as e:
            conn.rollback()
            form.nombre.errors.append('Error al actualizar el producto. Puede que ya exista otro con ese nombre.')
        finally:
            cerrar_conexion(conn)
    cerrar_conexion(conn)
    return render_template('productos/formulario.html', title='Editar producto', form=form, modo='editar', pid=pid)

@app.route('/productos/<int:pid>/eliminar', methods=['POST'])
def eliminar_producto(pid):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (pid,))
    if cursor.rowcount > 0:
        conn.commit()
        flash('Producto eliminado correctamente.', 'success')
    else:
        flash('Producto no encontrado.', 'warning')
    cerrar_conexion(conn)
    return redirect(url_for('listar_productos'))

# Rutas adicionales
@app.route('/clientes')
def clientes():
    return render_template('clientes.html', title='Clientes')

@app.route('/inventario')
def inventario():
    return render_template('inventario.html', title='Inventario')

@app.route('/ventas')
def ventas():
    return render_template('ventas.html', title='Ventas')

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html', title='Proveedores')

if __name__ == '__main__':
    app.run(debug=True)

# Install Flask
# .\venv\Scripts\activate
# pip install flask
# Port: 3307 para conectar  mysql.connector
# pip install flask_sqlalchemy