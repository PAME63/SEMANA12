"""
Punto de entrada de la aplicacion restaurante_app.

Toda la logica de negocio vive en servicios.restaurante.RestauranteServicio.
Este archivo solo se encarga del menu de consola y de leer datos del usuario.
"""

from servicios.restaurante_servicios import RestauranteServicio


def menu_principal():
    print("\n===== RESTAURANTE APP =====")
    print("1. Gestionar productos")
    print("2. Gestionar usuarios")
    print("3. Registrar venta")
    print("4. Consultar ventas por usuario")
    print("5. Listar categorias registradas")
    print("6. Gestionar prestamos de articulos")
    print("0. Salir")
    return input("Seleccione una opcion: ").strip()


def menu_productos():
    print("\n--- Productos ---")
    print("1. Registrar producto")
    print("2. Buscar producto por codigo")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Listar productos")
    print("0. Volver")
    return input("Seleccione una opcion: ").strip()


def menu_usuarios():
    print("\n--- Usuarios ---")
    print("1. Registrar usuario")
    print("2. Buscar usuario por identificacion")
    print("3. Actualizar usuario")
    print("4. Eliminar usuario")
    print("5. Listar usuarios")
    print("0. Volver")
    return input("Seleccione una opcion: ").strip()


def menu_prestamos():
    print("\n--- Prestamos de articulos del local ---")
    print("1. Registrar prestamo")
    print("2. Registrar devolucion")
    print("3. Listar prestamos activos")
    print("4. Listar historial de prestamos")
    print("0. Volver")
    return input("Seleccione una opcion: ").strip()


def gestionar_productos(servicio):
    while True:
        opcion = menu_productos()

        if opcion == "1":
            codigo = input("Codigo: ").strip()
            nombre = input("Nombre: ").strip()
            categoria = input("Categoria: ").strip()
            try:
                precio = float(input("Precio: ").strip())
                stock = int(input("Stock: ").strip())
            except ValueError:
                print("Precio o stock invalido.")
                continue
            ok, mensaje = servicio.registrar_producto(codigo, nombre, categoria, precio, stock)
            print(mensaje)

        elif opcion == "2":
            codigo = input("Codigo a buscar: ").strip()
            producto = servicio.buscar_producto(codigo)
            print(producto if producto else "Producto no encontrado.")

        elif opcion == "3":
            codigo = input("Codigo del producto a actualizar: ").strip()
            nombre = input("Nuevo nombre (Enter para omitir): ").strip() or None
            categoria = input("Nueva categoria (Enter para omitir): ").strip() or None
            precio_str = input("Nuevo precio (Enter para omitir): ").strip()
            stock_str = input("Nuevo stock (Enter para omitir): ").strip()
            precio = float(precio_str) if precio_str else None
            stock = int(stock_str) if stock_str else None
            ok, mensaje = servicio.actualizar_producto(
                codigo, nombre=nombre, categoria=categoria, precio=precio, stock=stock
            )
            print(mensaje)

        elif opcion == "4":
            codigo = input("Codigo del producto a eliminar: ").strip()
            ok, mensaje = servicio.eliminar_producto(codigo)
            print(mensaje)

        elif opcion == "5":
            productos = servicio.listar_productos()
            if not productos:
                print("No hay productos registrados.")
            for producto in productos:
                print(producto)

        elif opcion == "0":
            break

        else:
            print("Opcion invalida.")


def gestionar_usuarios(servicio):
    while True:
        opcion = menu_usuarios()

        if opcion == "1":
            identificacion = input("Identificacion: ").strip()
            nombre = input("Nombre: ").strip()
            correo = input("Correo: ").strip()
            tipo = input("Tipo (cliente/empleado): ").strip()
            ok, mensaje = servicio.registrar_usuario(identificacion, nombre, correo, tipo)
            print(mensaje)

        elif opcion == "2":
            identificacion = input("Identificacion a buscar: ").strip()
            usuario = servicio.buscar_usuario(identificacion)
            print(usuario if usuario else "Usuario no encontrado.")

        elif opcion == "3":
            identificacion = input("Identificacion del usuario a actualizar: ").strip()
            nombre = input("Nuevo nombre (Enter para omitir): ").strip() or None
            correo = input("Nuevo correo (Enter para omitir): ").strip() or None
            tipo = input("Nuevo tipo (Enter para omitir): ").strip() or None
            ok, mensaje = servicio.actualizar_usuario(
                identificacion, nombre=nombre, correo=correo, tipo=tipo
            )
            print(mensaje)

        elif opcion == "4":
            identificacion = input("Identificacion del usuario a eliminar: ").strip()
            ok, mensaje = servicio.eliminar_usuario(identificacion)
            print(mensaje)

        elif opcion == "5":
            usuarios = servicio.listar_usuarios()
            if not usuarios:
                print("No hay usuarios registrados.")
            for usuario in usuarios:
                print(usuario)

        elif opcion == "0":
            break

        else:
            print("Opcion invalida.")


def registrar_venta(servicio):
    print("\n--- Registrar venta ---")
    usuario_id = input("Identificacion del usuario: ").strip()
    producto_codigo = input("Codigo del producto: ").strip()
    try:
        cantidad = int(input("Cantidad: ").strip())
    except ValueError:
        print("Cantidad invalida.")
        return
    ok, mensaje = servicio.registrar_venta(usuario_id, producto_codigo, cantidad)
    print(mensaje)


def consultar_ventas_usuario(servicio):
    print("\n--- Ventas por usuario ---")
    usuario_id = input("Identificacion del usuario: ").strip()
    ventas = servicio.ventas_de_usuario(usuario_id)
    if not ventas:
        print("Este usuario no tiene ventas registradas.")
    for venta in ventas:
        print(venta)


def listar_categorias(servicio):
    print("\n--- Categorias registradas ---")
    categorias = servicio.listar_categorias()
    if not categorias:
        print("No hay categorias registradas.")
    for categoria in categorias:
        print(f"- {categoria}")


def gestionar_prestamos(servicio):
    while True:
        opcion = menu_prestamos()

        if opcion == "1":
            usuario_id = input("Identificacion del usuario: ").strip()
            articulo = input("Articulo a prestar (ej. Silla para bebe): ").strip()
            ok, mensaje = servicio.registrar_prestamo(usuario_id, articulo)
            print(mensaje)

        elif opcion == "2":
            articulo = input("Articulo a devolver: ").strip()
            ok, mensaje = servicio.devolver_prestamo(articulo)
            print(mensaje)

        elif opcion == "3":
            activos = servicio.listar_prestamos_activos()
            if not activos:
                print("No hay prestamos activos en este momento.")
            for prestamo in activos:
                print(prestamo)

        elif opcion == "4":
            historial = servicio.listar_prestamos()
            if not historial:
                print("No hay prestamos registrados.")
            for prestamo in historial:
                print(prestamo)

        elif opcion == "0":
            break

        else:
            print("Opcion invalida.")


def main():
    servicio = RestauranteServicio()

    while True:
        opcion = menu_principal()

        if opcion == "1":
            gestionar_productos(servicio)
        elif opcion == "2":
            gestionar_usuarios(servicio)
        elif opcion == "3":
            registrar_venta(servicio)
        elif opcion == "4":
            consultar_ventas_usuario(servicio)
        elif opcion == "5":
            listar_categorias(servicio)
        elif opcion == "6":
            gestionar_prestamos(servicio)
        elif opcion == "0":
            print("Hasta pronto.")
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()
