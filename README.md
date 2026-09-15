# Parcial 1 - Programación IV

## Catálogo de productos

Este proyecto implementa un modelo orientado a objetos para representar un catálogo de productos, aplicando los conceptos de encapsulamiento, composición, agregación, asociación, herencia, polimorfismo y Protocols de Python.

## Estructura del proyecto


Guardamagna-Octavio-Parcial-1/
├── README.md
├── catalogo.py
├── libreria_externa.py
├── main.py
├── link_video.txt
└── uml/
    └── modelo_final.md

## Archivos principales

**catalogo.py:** contiene las clases y reglas principales del dominio.
**libreria_externa.py:** contiene la clase PlanoCAD, perteneciente a una biblioteca externa. Este archivo no se modifica.
**main.py:** contiene la demostración y las pruebas de funcionamiento del modelo.
**modelo_final.md:** contiene el modelo UML realizado con Mermaid.
**link_video.txt:** contiene el enlace al video de demostración.

## Modelo de dominio
El modelo está compuesto por las siguientes clases principales:

**UnidadMedida:** representa la unidad utilizada para la venta de un producto.
**Categoria:** representa una categoría del catálogo.
**ProductoCategoria:** representa la clasificación de un producto dentro de una categoría.
**Producto:** clase abstracta base para los distintos tipos de productos.
**ProductoSimple:** representa productos vendidos por unidades.
**ProductoPorPeso:** representa productos vendidos por peso u otra cantidad decimal.
**ProductoCombo:** representa un conjunto de productos agrupados con un descuento.
**ProductoDestacado:** permite destacar un producto en una posición determinada de la vidriera.
**Exportable:** Protocol utilizado para representar objetos que pueden exportarse mediante el método exportar().

## Relaciones entre las clases

## Composición

**Producto** tiene una relación de composición con **ProductoCategoria**.

Cada producto crea y mantiene internamente sus objetos **ProductoCategoria**.

Producto ◆── ProductoCategoria

## Agregación

**ProductoCombo** tiene una relación de agregación con **Producto**.

Los productos que forman parte del combo existen independientemente del combo y pueden seguir existiendo aunque el combo deje de existir.

ProductoCombo ◇── Producto

## Asociación

**`ProductoCategoria`** tiene una relación de asociación con **`Categoria`**.

Además, **`ProductoDestacado`** mantiene una referencia al **`Producto`** que se desea destacar.

```text
ProductoCategoria ── Categoria
ProductoDestacado ── Producto
```

## Herencia y polimorfismo

`Producto` es una clase abstracta que define el método `precio_final()`.

Las clases `ProductoSimple`, `ProductoPorPeso` y `ProductoCombo` heredan de `Producto` e implementan su propia forma de calcular el precio final.

Esto permite aplicar polimorfismo, ya que el mismo método `precio_final()` puede producir un resultado diferente dependiendo del tipo concreto de producto.

## ProductoCombo

Un `ProductoCombo` está formado por al menos dos productos y posee un descuento entre `0` y `1`, sin incluir `1`.

El precio final del combo se calcula sumando el precio final de una unidad de cada uno de sus componentes, aplicando posteriormente el descuento y multiplicando por la cantidad solicitada.

```text
precio final =
    suma de precios de los componentes
    × (1 - descuento)
    × cantidad
```

El `precio_base` del combo se almacena como parte de los datos generales del producto, mientras que el cálculo de `precio_final()` utiliza los precios de los componentes y el descuento.

El `stock_cantidad` representa la cantidad de combos disponibles.

## ProductoDestacado

`ProductoDestacado` no hereda de `Producto`.

La característica de estar destacado representa una decisión de presentación en la vidriera y no un nuevo tipo de producto ni una modificación de su forma de calcular el precio.

Por este motivo, `ProductoDestacado` mantiene una referencia a un `Producto` y almacena su posición mediante `orden_vidriera`.

Esto permite destacar productos de distintos tipos, por ejemplo:

- `ProductoSimple`
- `ProductoPorPeso`
- `ProductoCombo`

## Encapsulamiento y validaciones

Los atributos internos del modelo se almacenan utilizando atributos protegidos, por ejemplo:

```python
_nombre
_precio_base
_stock_cantidad
```

El acceso a los datos se realiza mediante propiedades de solo lectura cuando corresponde.

Las colecciones internas tampoco se exponen directamente. Por ejemplo, `categorias()` devuelve una tupla para evitar que el código externo pueda modificar directamente la colección interna.

El modelo también incluye validaciones para mantener las reglas del dominio, entre ellas:

- El nombre de una categoría no puede estar vacío.
- El nombre de un producto no puede estar vacío.
- El precio base no puede ser negativo.
- El stock no puede ser negativo.
- Un producto debe tener una única categoría principal.
- No se puede clasificar dos veces un producto en la misma categoría.
- Un producto simple requiere una cantidad entera mayor o igual a `1`.
- Un producto por peso requiere una cantidad mayor que `0`.
- Un combo debe tener al menos dos componentes.
- El descuento de un combo debe estar entre `0` y `1`, sin incluir `1`.
- El orden de un producto destacado debe ser un entero mayor o igual a `1`.

## Exportable y Protocol

Se define el Protocol `Exportable` con el método:

```python
def exportar(self) -> str:
    ...
```

Las clases no necesitan heredar explícitamente de `Exportable`. Se utiliza tipado estructural, por lo que cualquier objeto que implemente el método `exportar()` puede ser utilizado como `Exportable`.

La función:

```python
exportar_catalogo(items: list[Exportable]) -> list[str]
```

permite exportar distintos objetos que sean compatibles con este contrato.

Esto permite utilizar tanto los productos del catálogo como la clase `PlanoCAD` de la biblioteca externa sin modificar dicha clase.

## UML

El modelo UML se encuentra en:

```text
uml/modelo_final.md
```

El diagrama representa las clases principales y las relaciones de composición, agregación, asociación y herencia utilizadas en el proyecto.

## Ejecución

Para ejecutar la demostración del proyecto, abrir una terminal en la carpeta principal y ejecutar:

```bash
python main.py
```

El programa realiza demostraciones de:

- Categorías y clasificaciones.
- Composición.
- Agregación.
- Asociación.
- Herencia.
- Polimorfismo.
- Exportación mediante `Exportable`.
- Compatibilidad con `PlanoCAD`.
- Productos destacados.
- Validaciones y errores controlados.