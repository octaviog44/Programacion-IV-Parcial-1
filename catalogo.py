from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


class ErrorDeDominio(ValueError):
    """Error producido por una regla del dominio."""


@dataclass(frozen=True)
class UnidadMedida:
    nombre: str
    simbolo: str
    tipo: str


KILOGRAMO = UnidadMedida("kilogramo", "kg", "masa")
GRAMO = UnidadMedida("gramo", "g", "masa")
LITRO = UnidadMedida("litro", "L", "volumen")
UNIDAD = UnidadMedida("unidad", "u", "unidad")


class Categoria:
    def __init__(
        self,
        nombre: str,
        descripcion: str = "",
    ) -> None:
        if not nombre.strip():
            raise ErrorDeDominio(
                "El nombre de la categoría no puede estar vacío."
            )

        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion


class ProductoCategoria:
    def __init__(
        self,
        categoria: Categoria,
        es_principal: bool,
    ) -> None:
        self._categoria = categoria
        self._es_principal = es_principal

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @property
    def es_principal(self) -> bool:
        return self._es_principal

    def _marcar_principal(self, valor: bool) -> None:
        self._es_principal = valor


class Producto(ABC):
    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock_cantidad: float,
        unidad_venta: UnidadMedida | None,
        categoria_principal: Categoria,
    ) -> None:
        if not nombre.strip():
            raise ErrorDeDominio(
                "El nombre del producto no puede estar vacío."
            )

        if precio_base < 0:
            raise ErrorDeDominio(
                "El precio base no puede ser negativo."
            )

        if stock_cantidad < 0:
            raise ErrorDeDominio(
                "El stock no puede ser negativo."
            )

        if not isinstance(categoria_principal, Categoria):
            raise ErrorDeDominio(
                "La categoría principal debe ser una Categoria."
            )

        self._nombre = nombre
        self._precio_base = precio_base
        self._stock_cantidad = stock_cantidad
        self._habilitado = True
        self._unidad_venta = unidad_venta

        # Composición:
        # Producto crea internamente su ProductoCategoria.
        self._clasificaciones = [
            ProductoCategoria(categoria_principal, True)
        ]

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @property
    def unidad_venta(self) -> UnidadMedida | None:
        return self._unidad_venta

    @property
    def disponible(self) -> bool:
        return self._habilitado and self._stock_cantidad > 0

    @property
    def precio_publicado(self) -> str:
        precio = f"$ {self._precio_base:.2f}"

        if self._unidad_venta is not None:
            precio += f" / {self._unidad_venta.simbolo}"

        return precio

    def habilitar(self) -> None:
        self._habilitado = True

    def deshabilitar(self) -> None:
        self._habilitado = False

    def clasificar_en(
        self,
        categoria: Categoria,
        es_principal: bool = False,
    ) -> None:
        if not isinstance(categoria, Categoria):
            raise ErrorDeDominio(
                "La categoría debe ser una Categoria."
            )

        # No se puede clasificar dos veces en la misma categoría.
        for clasificacion in self._clasificaciones:
            if clasificacion.categoria is categoria:
                raise ErrorDeDominio(
                    "El producto ya está clasificado en esa categoría."
                )

        # Si la nueva clasificación será principal,
        # desmarcamos la principal anterior.
        if es_principal:
            for clasificacion in self._clasificaciones:
                clasificacion._marcar_principal(False)

        # Composición:
        # Producto crea internamente el vínculo.
        nueva_clasificacion = ProductoCategoria(
            categoria,
            es_principal,
        )

        self._clasificaciones.append(nueva_clasificacion)

    def categorias(self) -> tuple[ProductoCategoria, ...]:
        # Se devuelve una tupla, no la lista interna.
        return tuple(self._clasificaciones)

    def categoria_principal(self) -> Categoria:
        for clasificacion in self._clasificaciones:
            if clasificacion.es_principal:
                return clasificacion.categoria

        raise ErrorDeDominio(
            "El producto debe tener exactamente una categoría principal."
        )

    @abstractmethod
    def precio_final(self, cantidad: float) -> float:
        pass

    def exportar(self) -> str:
        return (
            f"PRODUCTO|{self._nombre}|"
            f"{self.precio_publicado}|"
            f"{self._stock_cantidad}"
        )


class ProductoSimple(Producto):
    def precio_final(self, cantidad: float) -> float:
        if isinstance(cantidad, bool) or not isinstance(
            cantidad, (int, float)
        ):
            raise ErrorDeDominio(
                "La cantidad debe ser numérica."
            )

        if cantidad < 1 or not float(cantidad).is_integer():
            raise ErrorDeDominio(
                "La cantidad debe ser un valor entero mayor o igual a 1."
            )

        return self._precio_base * cantidad


class ProductoPorPeso(Producto):
    def precio_final(self, cantidad: float) -> float:
        if isinstance(cantidad, bool) or not isinstance(
            cantidad, (int, float)
        ):
            raise ErrorDeDominio(
                "La cantidad debe ser numérica."
            )

        if cantidad <= 0:
            raise ErrorDeDominio(
                "La cantidad debe ser mayor que cero."
            )

        return round(self._precio_base * cantidad, 2)


class ProductoCombo(Producto):
    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock_cantidad: float,
        unidad_venta: UnidadMedida | None,
        categoria_principal: Categoria,
        componentes: list[Producto],
        descuento: float,
    ) -> None:
        super().__init__(
            nombre,
            precio_base,
            stock_cantidad,
            unidad_venta,
            categoria_principal,
        )

        if len(componentes) < 2:
            raise ErrorDeDominio(
                "Un combo debe tener al menos 2 componentes."
            )

        for componente in componentes:
            if not isinstance(componente, Producto):
                raise ErrorDeDominio(
                    "Todos los componentes deben ser productos."
                )

        if not 0 <= descuento < 1:
            raise ErrorDeDominio(
                "El descuento debe estar entre 0 y 1, sin incluir el 1."
            )

        # Agregación:
        # los productos ya existen antes del combo
        # y pueden seguir existiendo después.
        self._componentes = list(componentes)
        self._descuento = descuento

    def componentes(self) -> tuple[Producto, ...]:
        # Se devuelve una copia inmutable de la colección.
        return tuple(self._componentes)

    def precio_final(self, cantidad: float) -> float:
        if isinstance(cantidad, bool) or not isinstance(
            cantidad, (int, float)
        ):
            raise ErrorDeDominio(
                "La cantidad debe ser numérica."
            )

        if cantidad < 1 or not float(cantidad).is_integer():
            raise ErrorDeDominio(
                "La cantidad debe ser un valor entero mayor o igual a 1."
            )

        # Polimorfismo:
        # cada componente calcula su precio según su propia clase.
        precio_componentes = sum(
            componente.precio_final(1)
            for componente in self._componentes
        )

        precio_con_descuento = (
            precio_componentes * (1 - self._descuento)
        )

        return precio_con_descuento * cantidad


class ProductoDestacado:
    """
    Representa un producto destacado en la vidriera.

    No hereda de Producto porque "destacado" no representa
    un tipo de producto, sino una característica de presentación.

    Puede destacar cualquier Producto existente, incluyendo
    productos simples, productos por peso y combos.
    """

    def __init__(
        self,
        producto: Producto,
        orden_vidriera: int,
    ) -> None:
        if not isinstance(producto, Producto):
            raise ErrorDeDominio(
                "El producto destacado debe ser un Producto."
            )

        if isinstance(orden_vidriera, bool) or not isinstance(
            orden_vidriera, int
        ):
            raise ErrorDeDominio(
                "El orden de vidriera debe ser un entero."
            )

        if orden_vidriera < 1:
            raise ErrorDeDominio(
                "El orden de vidriera debe ser mayor o igual a 1."
            )

        self._producto = producto
        self._orden_vidriera = orden_vidriera

    @property
    def producto(self) -> Producto:
        return self._producto

    @property
    def orden_vidriera(self) -> int:
        return self._orden_vidriera


class Exportable(Protocol):
    def exportar(self) -> str:
        ...


def exportar_catalogo(items: list[Exportable]) -> list[str]:
    return [item.exportar() for item in items]