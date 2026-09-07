"""
RestauranteServicio.

Contiene toda la logica de negocio del sistema: productos, usuarios,
ventas, control de stock y prestamos de articulos del local.

Mejora de la Semana 12 (rendimiento con colecciones)
-----------------------------------------------------
Se conservan las listas principales porque siguen siendo necesarias para:
- Recorrer todos los registros (listar productos, usuarios, ventas, prestamos).
- Guardar y recuperar la informacion en formato JSON.

Ademas de las listas, se agregan estructuras auxiliares en memoria que NO
reemplazan a las listas, sino que aceleran operaciones puntuales que antes
requerian recorrer toda la coleccion:

- self._indice_productos   -> dict[str, Producto]
  Permite buscar un producto por su codigo en tiempo O(1) en promedio,
  en lugar de recorrer toda self.productos comparando codigo por codigo.

- self._indice_usuarios    -> dict[str, Usuario]
  Permite buscar un usuario por su identificacion en tiempo O(1) en
  promedio, en lugar de recorrer toda self.usuarios.

- self._ventas_por_usuario -> dict[str, list[Venta]]
  Permite consultar todas las ventas de un usuario sin recorrer la lista
  completa de ventas cada vez que se hace la consulta. Cada venta nueva
  se agrega tanto a la lista principal como a esta agrupacion.

- self._categorias         -> set[str]
  Guarda las categorias de producto ya registradas (ej. "Plato fuerte",
  "Bebida", "Postre") para validar existencia/pertenencia sin recorrer
  self.productos cada vez que se necesita saber si una categoria ya existe.

- self._prestamos_activos  -> dict[str, Prestamo]
  Guarda, por articulo, el prestamo actualmente activo (estado "prestado").
  Permite saber al instante si un articulo esta prestado en este momento
  sin recorrer todo el historial de self.prestamos.

Todas estas estructuras se reconstruyen al iniciar el programa a partir
de los datos recuperados desde JSON, y se mantienen sincronizadas cada
vez que se registra, modifica o elimina un producto, usuario, venta o
prestamo.
"""

from datetime import datetime

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from modelos.prestamo import Prestamo
from servicios.archivo_servicios import cargar_json, guardar_json

RUTA_PRODUCTOS = "datos/productos.json"
RUTA_USUARIOS = "datos/usuarios.json"
RUTA_VENTAS = "datos/ventas.json"
RUTA_PRESTAMOS = "datos/prestamos.json"


class RestauranteServicio:
    def __init__(self):
        # ---- Colecciones principales (listas) ----
        self.productos = []   # list[Producto]
        self.usuarios = []    # list[Usuario]
        self.ventas = []      # list[Venta]
        self.prestamos = []   # list[Prestamo]

        # ---- Estructuras auxiliares (indices en memoria) ----
        self._indice_productos = {}     # dict[codigo] -> Producto
        self._indice_usuarios = {}      # dict[identificacion] -> Usuario
        self._ventas_por_usuario = {}   # dict[usuario_id] -> list[Venta]
        self._categorias = set()        # set de categorias unicas
        self._prestamos_activos = {}    # dict[articulo] -> Prestamo (estado "prestado")

        self._contador_ventas = 0
        self._contador_prestamos = 0

        self.cargar_datos()

    # ------------------------------------------------------------------
    # Carga y reconstruccion de indices
    # ------------------------------------------------------------------
    def cargar_datos(self):
        """Carga productos, usuarios, ventas y prestamos desde JSON y
        reconstruye los indices auxiliares a partir de las listas recuperadas."""
        datos_productos = cargar_json(RUTA_PRODUCTOS)
        datos_usuarios = cargar_json(RUTA_USUARIOS)
        datos_ventas = cargar_json(RUTA_VENTAS)
        datos_prestamos = cargar_json(RUTA_PRESTAMOS)

        self.productos = [Producto.from_dict(p) for p in datos_productos]
        self.usuarios = [Usuario.from_dict(u) for u in datos_usuarios]
        self.ventas = [Venta.from_dict(v) for v in datos_ventas]
        self.prestamos = [Prestamo.from_dict(p) for p in datos_prestamos]

        self._reconstruir_indices()

    def _reconstruir_indices(self):
        """Reconstruye todas las estructuras auxiliares a partir de las
        listas principales. Se usa al iniciar el programa y puede
        reutilizarse si en algun momento los indices quedaran inconsistentes."""
        self._indice_productos = {p.codigo: p for p in self.productos}
        self._indice_usuarios = {u.identificacion: u for u in self.usuarios}

        self._categorias = {p.categoria for p in self.productos}

        self._ventas_por_usuario = {}
        for venta in self.ventas:
            self._ventas_por_usuario.setdefault(venta.usuario_id, []).append(venta)

        self._prestamos_activos = {
            p.articulo: p for p in self.prestamos if p.estado == "prestado"
        }

        self._contador_ventas = max(
            (v.id_venta for v in self.ventas), default=0
        )
        self._contador_prestamos = max(
            (p.id_prestamo for p in self.prestamos), default=0
        )

    # ------------------------------------------------------------------
    # Persistencia
    # ------------------------------------------------------------------
    def guardar_datos(self):
        guardar_json(RUTA_PRODUCTOS, [p.to_dict() for p in self.productos])
        guardar_json(RUTA_USUARIOS, [u.to_dict() for u in self.usuarios])
        guardar_json(RUTA_VENTAS, [v.to_dict() for v in self.ventas])
        guardar_json(RUTA_PRESTAMOS, [p.to_dict() for p in self.prestamos])

    # ------------------------------------------------------------------
    # Productos
    # ------------------------------------------------------------------
    def registrar_producto(self, codigo, nombre, categoria, precio, stock):
        if self.buscar_producto(codigo) is not None:
            return False, "Ya existe un producto con ese codigo."

        producto = Producto(codigo, nombre, categoria, precio, stock)
        self.productos.append(producto)          # lista principal
        self._indice_productos[codigo] = producto  # indice de busqueda
        self._categorias.add(categoria)             # set de categorias

        self.guardar_datos()
        return True, "Producto registrado correctamente."

    def buscar_producto(self, codigo):
        """Busqueda O(1) en promedio usando el indice, en lugar de recorrer
        toda la lista self.productos como se haria sin la mejora."""
        return self._indice_productos.get(codigo)

    def actualizar_producto(self, codigo, nombre=None, categoria=None,
                             precio=None, stock=None):
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False, "Producto no encontrado."

        if nombre is not None:
            producto.nombre = nombre
        if categoria is not None:
            producto.categoria = categoria
            self._categorias.add(categoria)
        if precio is not None:
            producto.precio = precio
        if stock is not None:
            producto.stock = stock

        self.guardar_datos()
        return True, "Producto actualizado correctamente."

    def eliminar_producto(self, codigo):
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False, "Producto no encontrado."

        self.productos.remove(producto)
        del self._indice_productos[codigo]
        # No se elimina la categoria del set porque otros productos
        # pueden seguir perteneciendo a ella; se reconstruye si hace falta.
        self._categorias = {p.categoria for p in self.productos}

        self.guardar_datos()
        return True, "Producto eliminado correctamente."

    def listar_productos(self):
        return list(self.productos)  # se conserva la lista para recorrer/listar

    def listar_categorias(self):
        """Usa el set de categorias unicas para responder sin recorrer
        toda la lista de productos comparando categorias repetidas."""
        return sorted(self._categorias)

    def categoria_existe(self, categoria):
        """Validacion de pertenencia O(1) gracias al set."""
        return categoria in self._categorias

    # ------------------------------------------------------------------
    # Usuarios
    # ------------------------------------------------------------------
    def registrar_usuario(self, identificacion, nombre, correo, tipo):
        if self.buscar_usuario(identificacion) is not None:
            return False, "Ya existe un usuario con esa identificacion."

        usuario = Usuario(identificacion, nombre, correo, tipo)
        self.usuarios.append(usuario)                     # lista principal
        self._indice_usuarios[identificacion] = usuario     # indice de busqueda
        self._ventas_por_usuario.setdefault(identificacion, [])

        self.guardar_datos()
        return True, "Usuario registrado correctamente."

    def buscar_usuario(self, identificacion):
        """Busqueda O(1) en promedio usando el indice de usuarios."""
        return self._indice_usuarios.get(identificacion)

    def actualizar_usuario(self, identificacion, nombre=None, correo=None, tipo=None):
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False, "Usuario no encontrado."

        if nombre is not None:
            usuario.nombre = nombre
        if correo is not None:
            usuario.correo = correo
        if tipo is not None:
            usuario.tipo = tipo

        self.guardar_datos()
        return True, "Usuario actualizado correctamente."

    def eliminar_usuario(self, identificacion):
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False, "Usuario no encontrado."

        self.usuarios.remove(usuario)
        del self._indice_usuarios[identificacion]
        self._ventas_por_usuario.pop(identificacion, None)

        self.guardar_datos()
        return True, "Usuario eliminado correctamente."

    def listar_usuarios(self):
        return list(self.usuarios)

    # ------------------------------------------------------------------
    # Ventas y control de stock
    # ------------------------------------------------------------------
    def registrar_venta(self, usuario_id, producto_codigo, cantidad):
        usuario = self.buscar_usuario(usuario_id)
        if usuario is None:
            return False, "Usuario no encontrado."

        producto = self.buscar_producto(producto_codigo)
        if producto is None:
            return False, "Producto no encontrado."

        if cantidad <= 0:
            return False, "La cantidad debe ser mayor a cero."

        if producto.stock < cantidad:
            return False, f"Stock insuficiente. Disponible: {producto.stock}"

        producto.stock -= cantidad
        total = round(producto.precio * cantidad, 2)

        self._contador_ventas += 1
        venta = Venta(
            id_venta=self._contador_ventas,
            usuario_id=usuario_id,
            producto_codigo=producto_codigo,
            cantidad=cantidad,
            total=total,
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        self.ventas.append(venta)  # lista principal de ventas
        self._ventas_por_usuario.setdefault(usuario_id, []).append(venta)  # indice

        self.guardar_datos()
        return True, f"Venta registrada. Total: ${total:.2f}"

    def listar_ventas(self):
        return list(self.ventas)

    def ventas_de_usuario(self, usuario_id):
        """Consulta directa sin recorrer toda la lista de ventas: se apoya
        en el dict self._ventas_por_usuario, agrupado por usuario_id."""
        return list(self._ventas_por_usuario.get(usuario_id, []))

    # ------------------------------------------------------------------
    # Prestamos de articulos del local
    # ------------------------------------------------------------------
    def registrar_prestamo(self, usuario_id, articulo):
        """Registra el prestamo de un articulo del local (silla para bebe,
        cargador, juego de mesa, etc.) a un usuario. No se permite prestar
        un articulo que ya esta prestado en este momento."""
        usuario = self.buscar_usuario(usuario_id)
        if usuario is None:
            return False, "Usuario no encontrado."

        if self.articulo_prestado(articulo):
            return False, f"El articulo '{articulo}' ya esta prestado."

        self._contador_prestamos += 1
        prestamo = Prestamo(
            id_prestamo=self._contador_prestamos,
            usuario_id=usuario_id,
            articulo=articulo,
            fecha_prestamo=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            fecha_devolucion=None,
            estado="prestado",
        )

        self.prestamos.append(prestamo)             # lista principal
        self._prestamos_activos[articulo] = prestamo  # indice de activos

        self.guardar_datos()
        return True, "Prestamo registrado correctamente."

    def articulo_prestado(self, articulo):
        """Validacion O(1) usando el indice de prestamos activos, en lugar
        de recorrer todo el historial self.prestamos buscando el estado."""
        return articulo in self._prestamos_activos

    def devolver_prestamo(self, articulo):
        """Marca como devuelto el prestamo activo de un articulo, ubicandolo
        directamente mediante el indice en lugar de recorrer la lista."""
        prestamo = self._prestamos_activos.get(articulo)
        if prestamo is None:
            return False, f"No hay un prestamo activo para '{articulo}'."

        prestamo.estado = "devuelto"
        prestamo.fecha_devolucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        del self._prestamos_activos[articulo]

        self.guardar_datos()
        return True, "Devolucion registrada correctamente."

    def listar_prestamos(self):
        return list(self.prestamos)

    def listar_prestamos_activos(self):
        """Usa directamente el indice de activos, sin recorrer ni filtrar
        todo el historial de prestamos."""
        return list(self._prestamos_activos.values())
