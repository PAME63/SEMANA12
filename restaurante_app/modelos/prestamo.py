"""
Modelo Prestamo.

Adaptado al contexto de restaurante: representa el prestamo temporal de un
articulo del local (por ejemplo silla para bebe, cargador, juego de mesa,
paraguas) a un usuario, mientras permanece en el establecimiento. No se
presta comida ni bebida: eso se gestiona mediante Venta.

Un prestamo tiene un estado ("prestado" o "devuelto") que permite saber
si el articulo esta actualmente en uso sin tener que revisar manualmente
el historial completo.
"""


class Prestamo:
    def __init__(self, id_prestamo, usuario_id, articulo, fecha_prestamo,
                 fecha_devolucion=None, estado="prestado"):
        self.id_prestamo = id_prestamo
        self.usuario_id = usuario_id
        self.articulo = articulo
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.estado = estado  # "prestado" o "devuelto"

    def to_dict(self):
        return {
            "id_prestamo": self.id_prestamo,
            "usuario_id": self.usuario_id,
            "articulo": self.articulo,
            "fecha_prestamo": self.fecha_prestamo,
            "fecha_devolucion": self.fecha_devolucion,
            "estado": self.estado,
        }

    @staticmethod
    def from_dict(data):
        return Prestamo(
            id_prestamo=data["id_prestamo"],
            usuario_id=data["usuario_id"],
            articulo=data["articulo"],
            fecha_prestamo=data["fecha_prestamo"],
            fecha_devolucion=data.get("fecha_devolucion"),
            estado=data.get("estado", "prestado"),
        )

    def __str__(self):
        return (
            f"Prestamo #{self.id_prestamo} | Usuario: {self.usuario_id} | "
            f"Articulo: {self.articulo} | Estado: {self.estado} | "
            f"Prestado: {self.fecha_prestamo} | Devuelto: {self.fecha_devolucion or '-'}"
        )
