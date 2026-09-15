from dataclasses import FrozenInstanceError

from catalogo import (
    Categoria,
    Producto,
    ProductoSimple,
    ProductoPorPeso,
    ProductoCombo,
    ProductoDestacado,
    ErrorDeDominio,
    KILOGRAMO,
    GRAMO,
    UNIDAD,
    Exportable,
    exportar_catalogo,
)

from libreria_externa import PlanoCAD


class ProductoIncompleto(Producto):
    """
    Subclase incompleta utilizada únicamente para demostrar
    la falla temprana de una clase abstracta.
    """

    pass


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

    fiambres = Categoria(
        "Fiambres",
        "Productos de fiambre",
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

    jamon = ProductoPorPeso(
        nombre="Jamon",
        precio_base=9000.0,
        stock_cantidad=3000,
        unidad_venta=GRAMO,
        categoria_principal=fiambres,
    )

    # ==========================================
    # R1 - MODELO Y ENCAPSULAMIENTO
    # ==========================================

    print("========================================")
    print("R1 - MODELO Y ENCAPSULAMIENTO")
    print("========================================")

    print()
    print("=== PRECIO PUBLICADO ===")

    print(gaseosa.nombre, "->", gaseosa.precio_publicado)
    print(queso.nombre, "->", queso.precio_publicado)
    print(jamon.nombre, "->", jamon.precio_publicado)

    print()
    print("=== DISPONIBILIDAD ===")

    print(
        gaseosa.nombre,
        "-> disponible:",
        gaseosa.disponible,
    )

    gaseosa.deshabilitar()

    print(
        gaseosa.nombre,
        "deshabilitada -> disponible:",
        gaseosa.disponible,
    )

    gaseosa.habilitar()

    print(
        gaseosa.nombre,
        "habilitada nuevamente -> disponible:",
        gaseosa.disponible,
    )

    print()
    print("=== UNIDAD DE MEDIDA INMUTABLE ===")

    print(
        "Unidad:",
        KILOGRAMO.nombre,
        "| símbolo:",
        KILOGRAMO.simbolo,
    )

    try:
        KILOGRAMO.simbolo = "kg2"
    except FrozenInstanceError as error:
        print(
            "Error controlado: no se puede modificar "
            "una UnidadMedida congelada."
        )
        print("Tipo de error:", type(error).__name__)

    # ==========================================
    # R2 - COMPOSICIÓN, AGREGACIÓN Y ASOCIACIÓN
    # ==========================================

    print()
    print("========================================")
    print("R2 - COMPOSICIÓN, AGREGACIÓN Y ASOCIACIÓN")
    print("========================================")

    # ==========================================
    # ASOCIACIÓN
    # Producto -> UnidadMedida
    # ProductoCategoria -> Categoria
    # ==========================================

    print()
    print("=== ASOCIACIÓN ===")

    print(
        "Categoría principal de",
        gaseosa.nombre,
        ":",
        gaseosa.categoria_principal().nombre,
    )

    print(
        "Unidad de venta de",
        gaseosa.nombre,
        ":",
        gaseosa.unidad_venta.simbolo
        if gaseosa.unidad_venta is not None
        else "sin unidad",
    )

    print(
        "Unidad de venta de",
        queso.nombre,
        ":",
        queso.unidad_venta.simbolo
        if queso.unidad_venta is not None
        else "sin unidad",
    )

    # ==========================================
    # COMPOSICIÓN
    # Producto crea internamente ProductoCategoria
    # ==========================================

    print()
    print("=== COMPOSICIÓN ===")

    print("Categorías de", gaseosa.nombre, ":")

    for clasificacion in gaseosa.categorias():
        print(
            "-",
            clasificacion.categoria.nombre,
            "| principal:",
            clasificacion.es_principal,
        )

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

    golosinas = Categoria(
        "Golosinas",
        "Productos dulces",
    )

    gaseosa.clasificar_en(
        golosinas,
        es_principal=True,
    )

    print(
        "Categoría principal actual:",
        gaseosa.categoria_principal().nombre,
    )

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

    print(
        "Tipo devuelto por categorias():",
        type(categorias).__name__,
    )

    try:
        categorias.append(snacks)
    except AttributeError:
        print(
            "Correcto: la colección devuelta no permite "
            "modificar la colección interna."
        )

    # ==========================================
    # AGREGACIÓN
    # ProductoCombo -> Producto
    # ==========================================

    print()
    print("=== AGREGACIÓN ===")

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
        "Precio final del combo por 1 unidad:",
        combo.precio_final(1),
    )

    print(
        "Precio final del combo por 2 unidades:",
        combo.precio_final(2),
    )

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

    # Se demuestra que los mismos productos pueden formar
    # parte de otro combo.
    segundo_combo = ProductoCombo(
        nombre="Combo Queso + Jamon",
        precio_base=16000.0,
        stock_cantidad=3,
        unidad_venta=UNIDAD,
        categoria_principal=fiambres,
        componentes=[queso, jamon],
        descuento=0.05,
    )

    print(
        "Segundo combo creado:",
        segundo_combo.nombre,
    )

    print("Componentes del segundo combo:")

    for componente in segundo_combo.componentes():
        print("-", componente.nombre)

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
        "Gaseosa hereda de Producto:",
        isinstance(gaseosa, Producto),
    )

    print(
        "Queso hereda de Producto:",
        isinstance(queso, Producto),
    )

    print(
        "Combo hereda de Producto:",
        isinstance(combo, Producto),
    )

    print()
    print("=== POLIMORFISMO ===")

    productos: list[Producto] = [
        gaseosa,
        queso,
        jamon,
        combo,
    ]

    cantidades = [
        2,
        0.5,
        250,
        1,
    ]

    for producto, cantidad in zip(productos, cantidades):
        print(
            producto.nombre,
            "-> cantidad:",
            cantidad,
            "-> precio final:",
            producto.precio_final(cantidad),
        )

    # ==========================================
    # FALLA TEMPRANA DE CLASE ABSTRACTA
    # ==========================================

    print()
    print("=== FALLA TEMPRANA DE CLASE ABSTRACTA ===")

    try:
        Producto(
            nombre="Producto abstracto",
            precio_base=1000.0,
            stock_cantidad=1,
            unidad_venta=UNIDAD,
            categoria_principal=alimentos,
        )
    except TypeError as error:
        print(
            "Error controlado al instanciar Producto:",
            error,
        )

    try:
        ProductoIncompleto(
            nombre="Producto incompleto",
            precio_base=1000.0,
            stock_cantidad=1,
            unidad_venta=UNIDAD,
            categoria_principal=alimentos,
        )
    except TypeError as error:
        print(
            "Error controlado al instanciar "
            "una subclase incompleta:",
            error,
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
        [
            gaseosa,
            queso,
            jamon,
            combo,
        ]
    )

    for exportacion in exportaciones_productos:
        print(exportacion)

    print()
    print("=== EXPORTACIÓN DE PLANO CAD ===")

    plano = PlanoCAD(
        identificador="PLANO-001",
        escala="1:100",
    )

    exportacion_plano = exportar_catalogo(
        [plano]
    )

    for exportacion in exportacion_plano:
        print(exportacion)

    print()
    print("=== EXPORTACIÓN CONJUNTA ===")

    elementos_exportables: list[Exportable] = [
        gaseosa,
        queso,
        jamon,
        combo,
        plano,
    ]

    exportaciones = exportar_catalogo(
        elementos_exportables
    )

    for exportacion in exportaciones:
        print(exportacion)

    print()
    print("Cantidad de objetos compatibles con Exportable:")

    exportables: list[Exportable] = [
        gaseosa,
        queso,
        jamon,
        combo,
        plano,
    ]

    print(len(exportables))

    # ==========================================
    # R5 - PRODUCTO DESTACADO
    # ==========================================

    print()
    print("========================================")
    print("R5 - PRODUCTO DESTACADO")
    print("========================================")

    print()
    print("=== DECISIÓN DE DISEÑO ===")

    print(
        "ProductoDestacado no hereda de Producto porque "
        "ser destacado no representa un tipo de producto."
    )

    print(
        "ProductoDestacado mantiene una referencia al Producto "
        "que se desea mostrar en la vidriera."
    )

    print(
        "De esta forma se pueden destacar productos simples, "
        "productos por peso y combos."
    )

    print()
    print("=== DESTACAR PRODUCTOS ===")

    destacado_gaseosa = ProductoDestacado(
        producto=gaseosa,
        orden_vidriera=1,
    )

    destacado_queso = ProductoDestacado(
        producto=queso,
        orden_vidriera=2,
    )

    destacado_combo = ProductoDestacado(
        producto=combo,
        orden_vidriera=3,
    )

    destacados = [
        destacado_gaseosa,
        destacado_queso,
        destacado_combo,
    ]

    for destacado in destacados:
        print(
            "Orden:",
            destacado.orden_vidriera,
            "| Producto:",
            destacado.producto.nombre,
            "| Tipo:",
            type(destacado.producto).__name__,
        )

    print()
    print("=== VALIDACIONES ===")

    try:
        ProductoDestacado(
            producto=gaseosa,
            orden_vidriera=0,
        )
    except ErrorDeDominio as error:
        print("Error controlado:", error)

    try:
        ProductoDestacado(
            producto="Gaseosa",
            orden_vidriera=1,
        )
    except ErrorDeDominio as error:
        print("Error controlado:", error)


if __name__ == "__main__":
    main()