import unittest
from django.test import SimpleTestCase
from django.urls import reverse
from .servicios import calcular_emisiones_carbono, obtener_metricas_consumo


class TestCalculoEmisiones(unittest.TestCase):
    def test_nominal(self):
        self.assertEqual(calcular_emisiones_carbono(100), 40)

    def test_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(12.5, 0.3), 3.75)

    def test_cero(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0)
        self.assertEqual(calcular_emisiones_carbono(100, 0), 0)

    def test_negativo(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-50)

    def test_no_finitos(self):
        for valor in [float("nan"), float("inf"), -1]:
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                calcular_emisiones_carbono(100, valor)


class TestMetricas(unittest.TestCase):
    def test_acumulacion(self):
        datos = [{"planta": "Norte", "consumo_kwh": 60},
                 {"planta": "Sur", "consumo_kwh": 100},
                 {"planta": "Norte", "consumo_kwh": 60}]
        resultado = obtener_metricas_consumo(datos)
        self.assertEqual(resultado["planta_top"], "Norte")
        self.assertAlmostEqual(resultado["total_emisiones"], 88)

    def test_vacio(self):
        resultado = obtener_metricas_consumo([])
        self.assertIsNone(resultado["planta_top"])
        self.assertEqual(resultado["total_emisiones"], 0)

    def test_negativo(self):
        with self.assertRaises(ValueError):
            obtener_metricas_consumo([{"planta": "Norte", "consumo_kwh": -1}])


class TestPanel(SimpleTestCase):
    def test_renderizado(self):
        respuesta = self.client.get(reverse("panel_sustentabilidad"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "sustentabilidad/panel.html")
        self.assertEqual(respuesta.context["planta_top"], "Norte")
        self.assertEqual(respuesta.context["total_emisiones"], 1380)
        self.assertContains(respuesta, "Panel de sustentabilidad")
