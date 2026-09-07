"""
Modelo Producto.

Representa un producto del menu del restaurante (plato, bebida, etc.)
Cada producto tiene un codigo unico que se utiliza como clave de busqueda
rapida en los indices creados por RestauranteServicio.
"""


class Producto:
    def __init__(self, codigo, nombre, categoria, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
        }

    @staticmethod
    def from_dict(data):
        return Producto(
            codigo=data["codigo"],
            nombre=data["nombre"],
            categoria=data["categoria"],
            precio=data["precio"],
            stock=data["stock"],
        )

    def __str__(self):
        return (
            f"[{self.codigo}] {self.nombre} - {self.categoria} "
            f"- ${self.precio:.2f} - Stock: {self.stock}"
        )
