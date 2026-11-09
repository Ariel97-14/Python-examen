"""Lógica de cálculo independiente de Django."""
import math


def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    """Calcula kg CO2 a partir de kWh y kg CO2/kWh."""
    if not math.isfinite(consumo_kwh) or consumo_kwh < 0:
        raise ValueError("El consumo debe ser finito y no negativo.")
    if not math.isfinite(factor_emision) or factor_emision < 0:
        raise ValueError("El factor debe ser finito y no negativo.")
    return consumo_kwh * factor_emision


def obtener_metricas_consumo(registros):
    """Acumula consumos por planta. En empate conserva la primera."""
    consumos = {}
    total_emisiones = 0.0
    for registro in registros:
        consumo = registro["consumo_kwh"]
        total_emisiones += calcular_emisiones_carbono(consumo)
        planta = registro["planta"]
        consumos[planta] = consumos.get(planta, 0.0) + consumo
    return {
        "total_emisiones": total_emisiones,
        "planta_top": max(consumos, key=consumos.get) if consumos else None,
        "total_consumo": sum(consumos.values()),
        "consumos_por_planta": consumos,
    }
