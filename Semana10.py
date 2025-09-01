from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    productos = [
        {
            "nombre": "Dron agrícola",
            "imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRd0r9tV2Zsk7wxCKYD1WyMlWYA0j_2fBTCCw&s",
            "descripcion": "Drones para monitoreo y análisis de cultivos.",
            "video": "https://www.w3schools.com/html/mov_bbb.mp4"
        },
        {
            "nombre": "Sensor de riego inteligente",
            "imagen": "https://minkafab.com/wp-content/uploads/2020/09/diagrama.jpg",
            "descripcion": "Sensores para optimizar el uso del agua en la agricultura.",
            "video": "https://www.w3schools.com/html/movie.mp4"
        },
        {
            "nombre": "Tablet en campo",
            "imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQin6tsI5ZTo6FNz35H82XAwCW3f-8nJW8fvQ&s",
            "descripcion": "Gestión digital de la producción agrícola.",
            "video": ""
        },
        {
            "nombre": "Tractor moderno",
            "imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQX_NDGGrpCJ_nj73ZiIDsV3ixPhNBvBy1bsg&s",
            "descripcion": "Tractores equipados con tecnología GPS y sensores.",
            "video": ""
        }
    ]
    return render_template('index.html', title='Inicio', productos=productos)

@app.route('/comprar', methods=['POST'])
def comprar():
    producto = request.form.get('producto')
    return render_template('compra_confirmacion.html', producto=producto)

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}'

@app.route('/about/')
def about():
    return render_template('about.html', title='Acerca de')

@app.route('/contact/')
def contact():
    return render_template('contacto.html', title='Contacto')

if __name__ == '__main__':
    app.run(debug=True)

