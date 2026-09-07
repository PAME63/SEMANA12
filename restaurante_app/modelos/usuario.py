"""
Modelo Usuario.

Representa a un cliente o empleado que puede estar relacionado con ventas.
La identificacion es la clave unica utilizada por el indice de usuarios.
"""


class Usuario:
    def __init__(self, identificacion, nombre, correo, tipo):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.tipo = tipo  # Ej: "cliente" o "empleado"

    def to_dict(self):
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "tipo": self.tipo,
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            identificacion=data["identificacion"],
            nombre=data["nombre"],
            correo=data["correo"],
            tipo=data["tipo"],
        )

    def __str__(self):
        return f"[{self.identificacion}] {self.nombre} ({self.tipo}) - {self.correo}"
