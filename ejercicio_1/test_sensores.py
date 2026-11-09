import unittest
from sensores import limpiar_registro_sensor, generar_resumen_sensores

class TestSensores(unittest.TestCase):
    def test_limpieza_sin_mutacion(self):
        original = {"sensor_id": " S1 ", "temperatura": "24.5C"}
        limpio = limpiar_registro_sensor(original)
        self.assertEqual(limpio, {"sensor_id": "S1", "temperatura": 24.5, "ubicacion": "Desconocida"})
        self.assertEqual(original["sensor_id"], " S1 ")

    def test_formatos(self):
        for valor in [" -2 °C ", "-2c", -2]:
            self.assertEqual(limpiar_registro_sensor({"sensor_id": "S", "temperatura": valor})["temperatura"], -2)

    def test_invalido(self):
        with self.assertRaises(ValueError):
            limpiar_registro_sensor({"sensor_id": "S", "temperatura": "error"})

    def test_resumen(self):
        datos = [{"sensor_id": "A", "temperatura": 20}, {"sensor_id": "B", "temperatura": 30}]
        self.assertEqual(generar_resumen_sensores(datos, 20), (["B"], 25))
        self.assertEqual(generar_resumen_sensores([], 20), ([], 0.0))
