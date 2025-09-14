import sqlite3

miConexion=sqlite3.connect("productos.db")

miCursor=miConexion.cursor()

miCursor.execute('''
CREATE TABLE productos (
    id VARCHAR (20) PRIMARY KEY,
    nombre VARCHAR (100),
    cantidad INTEGER,
    precio VARCHAR (100)
)
''')
AñadirProductos=[
    ('011','Camisa',10,'15.99'),
    ('012','Pantalon',20,'25.50'),
    ('013','Zapatos',15,'45.00'),
    ('014','Sombrero',5,'12.75'),
    ('015','Chaqueta',8,'60.00')
]

miCursor.executemany('''
INSERT INTO productos (id, nombre, cantidad, precio)
VALUES (?, ?, ?, ?)
''', AñadirProductos)

miConexion.commit()

miConexion.close()
