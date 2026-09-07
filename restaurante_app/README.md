

Estudiante: Yajaira Pamela Jitala Cepeda  
 # Restaurante App

Aplicacion academica de consola para practicar Programacion Orientada a Objetos,
colecciones, relaciones entre objetos, persistencia con archivos JSON y
optimizacion de busquedas mediante estructuras auxiliares.

## Estructura

```
restaurante_app/
|
|-- datos/
|   |-- productos.json
|   |-- usuarios.json
|   |-- ventas.json
|   `-- prestamos.json
|
|-- modelos/
|   |-- __init__.py
|   |-- producto.py
|   |-- usuario.py
|   |-- venta.py
|   `-- prestamo.py
|
|-- servicios/
|   |-- __init__.py
|   |-- archivo_servicios.py
|   `-- restaurante_servicios.py
|
`-- main.py
```

- `modelos/`: clases principales del sistema (`Producto`, `Usuario`, `Venta`,
  `Prestamo`) y su conversion hacia/desde diccionario para la persistencia en JSON.
- `servicios/archivo_servicios.py`: funciones utilitarias de lectura y
  escritura de archivos JSON, sin logica de negocio.
- `servicios/restaurante_servicios.py`: toda la logica de negocio (productos,
  usuarios, ventas, stock, prestamos) y los indices en memoria para mejorar rendimiento.
- `datos/`: archivos JSON donde se conservan productos, usuarios, ventas y prestamos.
- `main.py`: menu de consola que solo lee datos del usuario y llama al servicio.

## Mejora Semana 12: rendimiento con colecciones

Con pocos registros, recorrer una lista completa parece suficiente, pero en
un restaurante con muchos productos, usuarios y ventas, repetir recorridos
lineales en cada busqueda afecta el rendimiento del sistema.

En esta version se mantiene el menu y las operaciones de la Semana 11, pero
se cambio la forma **interna** en que `RestauranteServicio` consulta los
datos. El sistema sigue cargando la informacion desde JSON hacia listas, y
adicionalmente construye indices en memoria para responder mas rapido a las
consultas frecuentes.

`RestauranteServicio` mantiene dos ideas al mismo tiempo:

- **Listas (`list`)**: `self.productos`, `self.usuarios`, `self.ventas`,
  `self.prestamos`. Se conservan porque siguen siendo necesarias para
  recorrer todos los registros (listar productos/usuarios/ventas/prestamos)
  y para guardar/recuperar la informacion en JSON.
- **Indices (`dict` y `set`)**: estructuras auxiliares que **no reemplazan**
  las listas, sino que evitan recorrer toda la coleccion en operaciones que
  se repiten con frecuencia.

### Colecciones auxiliares utilizadas

| Estructura | Tipo | Uso | Reemplaza a |
|---|---|---|---|
| `_indice_productos` | `dict[str, Producto]` | Buscar un producto por su **codigo** sin recorrer `self.productos`. | Recorrido lineal de la lista de productos. |
| `_indice_usuarios` | `dict[str, Usuario]` | Buscar un usuario por su **identificacion** sin recorrer `self.usuarios`. | Recorrido lineal de la lista de usuarios. |
| `_ventas_por_usuario` | `dict[str, list[Venta]]` | Consultar todas las ventas de un usuario sin revisar toda `self.ventas`. Cada venta nueva se agrega tanto a la lista principal como a esta agrupacion. | Recorrer todas las ventas filtrando por usuario en cada consulta. |
| `_categorias` | `set[str]` | Validar si una categoria ya existe y listar categorias unicas sin comparar contra cada producto. | Recorrido de productos comparando categorias repetidas. |
| `_prestamos_activos` | `dict[str, Prestamo]` | Saber al instante si un articulo del local (silla para bebe, cargador, juego de mesa, etc.) esta prestado en este momento, y ubicar ese prestamo para registrar su devolucion. | Recorrer todo el historial de prestamos filtrando por estado "prestado". |

### Por que mejora el rendimiento

Una busqueda en una lista debe comparar elemento por elemento hasta encontrar
el dato, por lo que el tiempo crece segun la cantidad de registros
(complejidad O(n)). Un diccionario usa una clave (codigo de producto,
identificacion de usuario) para llegar directamente al dato en tiempo
practicamente constante (O(1) en promedio). El `set` aplica la misma idea
para validar existencia de una categoria sin recorrer manualmente la lista
de productos.

### Sincronizacion y reconstruccion

- Al **registrar** un producto, usuario, venta o prestamo, se actualiza
  tanto la lista principal como el/los indice(s) correspondiente(s).
- Al **actualizar** un producto (por ejemplo su categoria), se ajusta el
  `set` de categorias.
- Al **eliminar** un producto o usuario, se elimina tambien de su indice
  correspondiente (y de `_ventas_por_usuario` en el caso de usuarios).
- Al **devolver** un prestamo, se marca el estado como "devuelto" y se
  elimina del indice `_prestamos_activos` (queda solo en el historial de
  `self.prestamos`).
- Al **iniciar el programa**, `cargar_datos()` lee los cuatro archivos JSON
  hacia las listas principales y luego `_reconstruir_indices()` construye
  todos los diccionarios y el set desde cero a partir de esas listas, por lo
  que los indices siempre quedan coherentes con la informacion persistida.

## Operaciones principales

- Registrar, buscar (por codigo), actualizar, eliminar y listar productos.
- Registrar, buscar (por identificacion), actualizar, eliminar y listar usuarios.
- Registrar una venta relacionando un usuario con un producto y descontando
  stock automaticamente.
- Consultar todas las ventas de un usuario especifico (usando el indice
  agrupado, sin recorrer todas las ventas).
- Listar las categorias unicas de productos registradas (usando el `set`).
- Registrar el prestamo de un articulo del local (silla para bebe, cargador,
  juego de mesa) a un usuario, validando que no este ya prestado.
- Registrar la devolucion de un articulo prestado.
- Listar los prestamos activos y el historial completo de prestamos.
- Persistir toda la informacion (productos, usuarios, ventas, prestamos) en JSON.

## Ejecucion

Desde la carpeta `restaurante_app`, ejecutar:

```
python main.py
```

La aplicacion carga automaticamente los archivos de `datos/` al iniciar
(reconstruyendo los indices en memoria) y guarda los cambios en JSON despues
de cada operacion que registra, actualiza o elimina informacion.

## Pruebas realizadas

- Ejecucion de `main.py` confirmando que las funcionalidades de productos,
  usuarios y ventas de la Semana 11 siguen operativas.
- Carga de productos, usuarios, ventas y prestamos existentes desde los
  archivos JSON.
- Busqueda de un producto por su codigo usando `_indice_productos`.
- Busqueda de un usuario por su identificacion usando `_indice_usuarios`.
- Consulta de las ventas de un usuario usando `_ventas_por_usuario`.
- Registro de una venta, confirmando el descuento correcto de stock del
  producto vendido.
- Registro de un prestamo, validando mediante `_prestamos_activos` que un
  articulo ya prestado no pueda volver a prestarse hasta ser devuelto.
- Registro de una devolucion, confirmando que el articulo se retira del
  indice de prestamos activos y queda en el historial como "devuelto".
- Verificacion de que los indices auxiliares permanecen coherentes despues
  de registrar productos, usuarios, ventas y prestamos nuevos.
- Cierre y nueva ejecucion del programa, confirmando que los datos se
  recuperan desde JSON y que los indices se reconstruyen correctamente
  (`_reconstruir_indices`), incluyendo el indice de prestamos activos.
   GRACIAS 
   


