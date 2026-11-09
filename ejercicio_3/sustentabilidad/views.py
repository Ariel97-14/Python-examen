from django.shortcuts import render
from .servicios import obtener_metricas_consumo

REGISTROS_CONSUMO = [
    {"planta": "Norte", "consumo_kwh": 1200},
    {"planta": "Sur", "consumo_kwh": 850},
    {"planta": "Norte", "consumo_kwh": 1400},
]


def vista_panel_sustentabilidad(request):
    contexto = obtener_metricas_consumo(REGISTROS_CONSUMO)
    return render(request, "sustentabilidad/panel.html", contexto)
