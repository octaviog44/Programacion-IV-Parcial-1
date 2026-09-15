from catalogo import (
    Categoria,
    ErrorDeDominio,
    ProductoSimple,
    ProductoPorPeso,
    ProductoCombo,
    KILOGRAMO,
    UNIDAD,
)

from catalogo import (
    Categoria,
    ProductoSimple,
    ProductoPorPeso,
    ProductoCombo,
    KILOGRAMO,
    UNIDAD,
    ErrorDeDominio,
)

def main() -> None:
    # Categorías
    bebidas = Categoria("Bebidas", "Bebidas y refrescos")
    alimentos = Categoria("Alimentos", "Productos alimenticios")

    # Producto simple
    gaseosa = ProductoSimple(
        nombre="Gaseosa",
        precio_base=1500.0,
        stock_cantidad=10,
        unidad_venta=UNIDAD,
        categoria_principal=bebidas,
    )

    # Producto por peso
    queso = ProductoPorPeso(
        nombre="Queso",
        precio_base=8000.0,
        stock_cantidad=5,
        unidad_venta=KILOGRAMO,
        categoria_principal=alimentos,
    )

    # Mostrar información
    print("=== PRODUCTO SIMPLE ===")
    print("Nombre:", gaseosa.nombre)
    print("Precio publicado:", gaseosa.precio_publicado)
    print("Disponible:", gaseosa.disponible)
    print("Precio por 2 unidades:", gaseosa.precio_final(2))
    print("Categoría principal:", gaseosa.categoria_principal().nombre)

    print()

    print("=== PRODUCTO POR PESO ===")
    print("Nombre:", queso.nombre)
    print("Precio publicado:", queso.precio_publicado)
    print("Disponible:", queso.disponible)
    print("Precio por 0.5 kg:", queso.precio_final(0.5))
    print("Categoría principal:", queso.categoria_principal().nombre)

    print()

    # Clasificar gaseosa también en alimentos
    gaseosa.clasificar_en(alimentos)

    print("=== CLASIFICACIONES ===")
    for clasificacion in gaseosa.categorias():
        print(
            clasificacion.categoria.nombre,
            "- principal:",
            clasificacion.es_principal,
        )

    print()

    # Deshabilitar producto
    gaseosa.deshabilitar()

    print("=== HABILITACIÓN ===")
    print("Gaseosa disponible después de deshabilitar:",
          gaseosa.disponible)

    gaseosa.habilitar()

    print("Gaseosa disponible después de habilitar:",
          gaseosa.disponible)


if __name__ == "__main__":
    main()


    print()
    print("=== PRUEBAS DE VALIDACIÓN ===")

    try:
        Categoria("")
    except ErrorDeDominio as error:
        print("Categoría vacía:", error)

    try:
        ProductoSimple(
            nombre="",
            precio_base=1000,
            stock_cantidad=5,
            unidad_venta=UNIDAD,
            categoria_principal=bebidas,
        )
    except ErrorDeDominio as error:
        print("Producto sin nombre:", error)

    try:
        gaseosa.precio_final(2.5)
    except ErrorDeDominio as error:
        print("Cantidad inválida para producto simple:", error)