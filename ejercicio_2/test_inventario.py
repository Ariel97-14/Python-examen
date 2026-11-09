import json
import tempfile
import unittest
from pathlib import Path
from inventario import DispositivoEcológico, PanelSolar, StockInvalidoError, GestorInventario

class TestInventario(unittest.TestCase):
    def test_stock_protegido(self):
        producto = DispositivoEcológico("Sensor", 100, 5)
        with self.assertRaises(StockInvalidoError):
            producto.stock = -1
        self.assertEqual(producto.get_stock(), 5)
        with self.assertRaises(StockInvalidoError):
            DispositivoEcológico("Sensor", 100, -1)

    def test_exportacion_y_polimorfismo(self):
        panel = PanelSolar("Solar", 500, 2, 300)
        self.assertIn("300 W", panel.obtener_ficha_tecnica())
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "catalogo_ecotech.json"
            GestorInventario.guardar_catalogo_json([panel], ruta)
            with ruta.open(encoding="utf-8") as archivo:
                datos = json.load(archivo)
            self.assertEqual(datos[0]["stock"], 2)
            self.assertEqual(datos[0]["eficiencia_watts"], 300)
