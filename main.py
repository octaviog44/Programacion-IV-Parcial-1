from catalogo import (
    Categoria,
    Producto,
    ProductoSimple,
    ProductoPorPeso,
    ProductoCombo,
    ErrorDeDominio,
    KILOGRAMO,
    UNIDAD,
    Exportable,
    exportar_catalogo,
)

from libreria_externa import PlanoCAD

def main() -> None:
    # ==========================================
    # CATEGORÍAS
    # ==========================================

    bebidas = Categoria(
        "Bebidas",
        "Bebidas y refrescos",
    )

    alimentos = Categoria(
        "Alimentos",
        "Productos alimenticios",
    )

    snacks = Categoria(
        "Snacks",
        "Productos para picar",
    )

    # ==========================================
    # PRODUCTOS
    # ==========================================

    gaseosa = ProductoSimple(
        nombre="Gaseosa",
        precio_base=1500.0,
        stock_cantidad=10,
        unidad_venta=UNIDAD,
        categoria_principal=bebidas,
    )

    queso = ProductoPorPeso(
        nombre="Queso",
        precio_base=8000.0,
        stock_cantidad=5,
        unidad_venta=KILOGRAMO,
        categoria_principal=alimentos,
    )

    print("========================================")
    print("R2 - COMPOSICIÓN, AGREGACIÓN Y ASOCIACIÓN")
    print("========================================")

    # ==========================================
    # ASOCIACIÓN
    # ProductoCategoria -> Categoria
    # ==========================================

    print()
    print("=== ASOCIACIÓN: PRODUCTO - CATEGORIA ===")

    print(
        "Categoría principal de",
        gaseosa.nombre,
        ":",
        gaseosa.categoria_principal().nombre,
    )

    print(
        "Categoría principal de",
        queso.nombre,
        ":",
        queso.categoria_principal().nombre,
    )

    # ==========================================
    # COMPOSICIÓN
    # Producto crea internamente ProductoCategoria
    # ==========================================

    print()
    print("=== COMPOSICIÓN: PRODUCTO - PRODUCTOCATEGORIA ===")

    print("Categorías de", gaseosa.nombre, ":")

    for clasificacion in gaseosa.categorias():
        print(
            "-",
            clasificacion.categoria.nombre,
            "| principal:",
            clasificacion.es_principal,
        )

    # Agregamos una segunda categoría.
    gaseosa.clasificar_en(snacks)

    print()
    print("Después de agregar la categoría Snacks:")

    for clasificacion in gaseosa.categorias():
        print(
            "-",
            clasificacion.categoria.nombre,
            "| principal:",
            clasificacion.es_principal,
        )

    # ==========================================
    # CAMBIO DE CATEGORÍA PRINCIPAL
    # ==========================================

    print()
    print("=== CAMBIO DE CATEGORÍA PRINCIPAL ===")

    gaseosa.clasificar_en(
        Categoria(
            "Golosinas",
            "Productos dulces",
        ),
        es_principal=True,
    )

    print("Categoría principal actual:")
    print("-", gaseosa.categoria_principal().nombre)

    print()
    print("Todas las categorías de", gaseosa.nombre, ":")

    for clasificacion in gaseosa.categorias():
        print(
            "-",
            clasificacion.categoria.nombre,
            "| principal:",
            clasificacion.es_principal,
        )

    # ==========================================
    # REGLA: NO DUPLICAR CATEGORÍAS
    # ==========================================

    print()
    print("=== VALIDACIÓN DE CATEGORÍAS DUPLICADAS ===")

    try:
        gaseosa.clasificar_en(snacks)
    except ErrorDeDominio as error:
        print("Error controlado:", error)

    # ==========================================
    # PROTECCIÓN DE LA COLECCIÓN
    # ==========================================

    print()
    print("=== PROTECCIÓN DE LA COLECCIÓN ===")

    categorias = gaseosa.categorias()

    print("Tipo devuelto por categorias():", type(categorias).__name__)

    try:
        categorias.append(snacks)
    except AttributeError:
        print(
            "Correcto: la colección devuelta no permite modificar "
            "la colección interna."
        )

    # ==========================================
    # AGREGACIÓN
    # ProductoCombo -> Producto
    # ==========================================

    print()
    print("=== AGREGACIÓN: PRODUCTOCOMBO - PRODUCTO ===")

    combo = ProductoCombo(
        nombre="Combo Gaseosa + Queso",
        precio_base=9000.0,
        stock_cantidad=5,
        unidad_venta=UNIDAD,
        categoria_principal=alimentos,
        componentes=[gaseosa, queso],
        descuento=0.10,
    )

    print("Combo:", combo.nombre)

    print("Componentes:")

    for componente in combo.componentes():
        print("-", componente.nombre)

    print(
        "Precio final del combo:",
        combo.precio_final(1),
    )

    # ==========================================
    # DEMOSTRAR QUE LOS PRODUCTOS SIGUEN EXISTIENDO
    # ==========================================

    print()
    print("=== INDEPENDENCIA DE LOS COMPONENTES ===")

    print(
        "Gaseosa sigue existiendo:",
        gaseosa.nombre,
    )

    print(
        "Queso sigue existiendo:",
        queso.nombre,
    )

    print(
        "Precio de la gaseosa por 2 unidades:",
        gaseosa.precio_final(2),
    )

    print(
        "Precio del queso por 0.5 kg:",
        queso.precio_final(0.5),
    )

    # ==========================================
    # R3 - HERENCIA Y POLIMORFISMO
    # ==========================================

    print()
    print("========================================")
    print("R3 - HERENCIA Y POLIMORFISMO")
    print("========================================")

    print()
    print("=== HERENCIA ===")

    print(
        "Gaseosa es Producto:",
        isinstance(gaseosa, ProductoSimple),
    )

    print(
        "Queso es Producto:",
        isinstance(queso, ProductoPorPeso),
    )

    print(
        "Combo es Producto:",
        isinstance(combo, ProductoCombo),
    )

    print()
    print("=== POLIMORFISMO ===")

    productos: list[Producto] = [
        gaseosa,
        queso,
        combo,
    ]

    cantidades = [2, 0.5, 1]

    for producto, cantidad in zip(productos, cantidades):
        print(
            producto.nombre,
            "-> cantidad:",
            cantidad,
            "-> precio final:",
            producto.precio_final(cantidad),
        )

    # ==========================================
    # R4 - PROTOCOL Y EXPORTACIÓN
    # ==========================================

    print()
    print("========================================")
    print("R4 - PROTOCOL Y EXPORTACIÓN")
    print("========================================")

    print()
    print("=== EXPORTACIÓN DE PRODUCTOS ===")

    exportaciones_productos = exportar_catalogo(
        [gaseosa, queso, combo]
    )

    for exportacion in exportaciones_productos:
        print(exportacion)

    print()
    print("=== EXPORTACIÓN DE PLANO CAD ===")

    plano = PlanoCAD(
        identificador="PLANO-001",
        escala="1:100",
    )

    exportacion_plano = exportar_catalogo([plano])

    for exportacion in exportacion_plano:
        print(exportacion)

    print()
    print("=== EXPORTACIÓN CONJUNTA ===")

    elementos_exportables = [
        gaseosa,
        queso,
        combo,
        plano,
    ]

    exportaciones = exportar_catalogo(
        elementos_exportables
    )

    for exportacion in exportaciones:
        print(exportacion)

        print()
    print("=== COMPATIBILIDAD CON EXPORTABLE ===")

    exportables: list[Exportable] = [
        gaseosa,
        queso,
        combo,
        plano,
    ]

    print(
        "Cantidad de objetos compatibles con Exportable:",
        len(exportables),
    )

if __name__ == "__main__":
    main()