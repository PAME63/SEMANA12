"""
Modelo Venta.

Representa la relacion Usuario-Producto: una venta asocia a un usuario
(cliente) con un producto vendido, la cantidad y el total pagado.
"""


class Venta:
    def __init__(self, id_venta, usuario_id, producto_codigo, cantidad, total, fecha):
        self.id_venta = id_venta
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad
        self.total = total
        self.fecha = fecha

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
            "total": self.total,
            "fecha": self.fecha,
        }

    @staticmethod
    def from_dict(data):
        return Venta(
            id_venta=data["id_venta"],
            usuario_id=data["usuario_id"],
            producto_codigo=data["producto_codigo"],
            cantidad=data["cantidad"],
            total=data["total"],
            fecha=data["fecha"],
        )

    def __str__(self):
        return (
            f"Venta #{self.id_venta} | Usuario: {self.usuario_id} | "
            f"Producto: {self.producto_codigo} | Cant: {self.cantidad} | "
            f"Total: ${self.total:.2f} | Fecha: {self.fecha}"
        )
