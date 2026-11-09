"""Productos ecológicos, validación de stock y persistencia JSON."""
import json
from pathlib import Path


class StockInvalidoError(Exception):
    """El stock debe ser un entero no negativo."""


class DispositivoEcológico:
    def __init__(self, modelo, precio, stock):
        self.modelo = modelo
        self.precio = precio
        self.set_stock(stock)

    def get_stock(self):
        return self.__stock

    def set_stock(self, nuevo_stock):
        if type(nuevo_stock) is not int or nuevo_stock < 0:
            raise StockInvalidoError("El stock debe ser un entero no negativo.")
        self.__stock = nuevo_stock

    stock = property(get_stock, set_stock)

    def obtener_ficha_tecnica(self):
        return f"Modelo: {self.modelo} | Precio: ${self.precio:.2f} | Stock: {self.get_stock()}"

    def a_diccionario(self):
        return {"tipo": type(self).__name__, "modelo": self.modelo,
                "precio": self.precio, "stock": self.get_stock()}


class PanelSolar(DispositivoEcológico):
    def __init__(self, modelo, precio, stock, eficiencia_watts):
        super().__init__(modelo, precio, stock)
        self.eficiencia_watts = eficiencia_watts

    def obtener_ficha_tecnica(self):
        return f"{super().obtener_ficha_tecnica()} | Potencia: {self.eficiencia_watts} W"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["eficiencia_watts"] = self.eficiencia_watts
        return datos


class GestorInventario:
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo):
        datos = [d.a_diccionario() for d in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    productos = [DispositivoEcológico("Termostato Smart", 350.0, 8),
                 PanelSolar("SolarMax-500", 1200.0, 10, 500)]
    try:
        productos[1].set_stock(-5)
    except StockInvalidoError as error:
        print(f"Error controlado: {error}")
    for producto in productos:
        print(producto.obtener_ficha_tecnica())
    ruta = Path(__file__).with_name("catalogo_ecotech.json")
    GestorInventario.guardar_catalogo_json(productos, ruta)
    print(f"Catálogo exportado: {ruta.name}")
