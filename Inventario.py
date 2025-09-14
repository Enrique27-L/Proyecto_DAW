from typing import List, Dict, Set
from collections import defaultdict
from models import db, Producto, Categoria

# Clase para manejar el inventario
class Inventario:
    """
    - Usa un diccionario {id: Producto} para accesos O(1).
    - Mantiene un set con nombres en minúsculas para validar duplicados rápidamente.
    - Permite manejar categorías si el modelo lo soporta.
    """
    def __init__(self, productos_dict=None):
        self.productos = productos_dict or {}  # dict[int, Producto]
        self.nombres = set(p.nombre.lower() for p in self.productos.values())

    @classmethod
    def cargar_desde_bd(cls):
        productos = Producto.query.all()
        productos_dict = {p.id: p for p in productos}
        return cls(productos_dict)

    def recargar(self):
        productos = Producto.query.all()
        self.productos = {p.id: p for p in productos}
        self.nombres = set(p.nombre.lower() for p in self.productos.values())

    # --- CRUD Productos ---
    def agregar(self, nombre: str, cantidad: int, precio: float, categoria_id: int = None) -> Producto:
        if nombre.lower() in self.nombres:
            raise ValueError('Ya existe un producto con ese nombre.')
        p = Producto(nombre=nombre.strip(), cantidad=int(cantidad), precio=float(precio))
        if categoria_id:
            categoria = Categoria.query.get(categoria_id)
            if categoria:
                p.categoria_id = categoria.id
        db.session.add(p)
        db.session.commit()
        self.productos[p.id] = p
        self.nombres.add(p.nombre.lower())
        return p

    def eliminar(self, id: int) -> bool:
        p = self.productos.get(id) or Producto.query.get(id)
        if not p:
            return False
        db.session.delete(p)
        db.session.commit()
        self.productos.pop(id, None)
        self.nombres.discard(p.nombre.lower())
        return True

    def actualizar(self, id: int, nombre=None, cantidad=None, precio=None, categoria_id=None) -> Producto | None:
        p = self.productos.get(id) or Producto.query.get(id)
        if not p:
            return None
        if nombre is not None:
            nuevo = nombre.strip()
            if nuevo.lower() != p.nombre.lower() and nuevo.lower() in self.nombres:
                raise ValueError('Ya existe otro producto con ese nombre.')
            self.nombres.discard(p.nombre.lower())
            p.nombre = nuevo
            self.nombres.add(p.nombre.lower())
        if cantidad is not None:
            p.cantidad = int(cantidad)
        if precio is not None:
            p.precio = float(precio)
        if categoria_id is not None:
            categoria = Categoria.query.get(categoria_id)
            if categoria:
                p.categoria_id = categoria.id
        db.session.commit()
        self.productos[p.id] = p
        return p

    # --- Consultas ---
    def buscar_por_nombre(self, q: str):
        q = q.lower()
        return sorted([p for p in self.productos.values() if q in p.nombre.lower()],
                      key=lambda x: x.nombre)

    def listar_todos(self):
        return sorted(self.productos.values(), key=lambda x: x.nombre)

    # --- Métodos para categorías ---
    def agregar_categoria(self, nombre: str) -> Categoria:
        if Categoria.query.filter_by(nombre=nombre).first():
            raise ValueError('Ya existe una categoría con ese nombre.')
        c = Categoria(nombre=nombre)
        db.session.add(c)
        db.session.commit()
        return c

    def eliminar_categoria(self, id: int) -> bool:
        c = Categoria.query.get(id)
        if not c:
            return False
        db.session.delete(c)
        db.session.commit()
        return True

    def listar_categorias(self):
        return Categoria.query.order_by(Categoria.nombre).all()