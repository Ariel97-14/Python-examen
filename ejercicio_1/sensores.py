"""Normalización y reporte de sensores térmicos."""
import math
import re


def limpiar_registro_sensor(registro_raw):
    """Devuelve un nuevo registro; exige ID y temperatura válidos."""
    sensor_id = str(registro_raw.get("sensor_id") or "").strip()
    texto = str(registro_raw.get("temperatura", "")).strip()
    if not sensor_id or not re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)\s*(?:°?\s*[Cc])?", texto):
        raise ValueError("Se requiere ID y temperatura numérica en Celsius.")
    temperatura = float(re.sub(r"\s*°?\s*[Cc]$", "", texto))
    if not math.isfinite(temperatura):
        raise ValueError("La temperatura debe ser finita.")
    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": str(registro_raw.get("ubicacion") or "").strip() or "Desconocida",
    }


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """Retorna (IDs que superan el umbral, promedio); vacío devuelve 0.0."""
    if not lista_sensores_limpios:
        return ([], 0.0)
    alertas = [s["sensor_id"] for s in lista_sensores_limpios
               if s["temperatura"] > umbral_temperatura]
    promedio = sum(s["temperatura"] for s in lista_sensores_limpios) / len(lista_sensores_limpios)
    return (alertas, promedio)


if __name__ == "__main__":
    crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": " SENSOR-002 ", "temperatura": " 32 °C "},
        {"sensor_id": " SENSOR-003 ", "temperatura": 28},
    ]
    limpios = [limpiar_registro_sensor(r) for r in crudos]
    alertas, promedio = generar_resumen_sensores(limpios, 30)
    for sensor in limpios:
        print(sensor)
    print(f"Sensores en alerta: {', '.join(alertas) or 'Ninguno'}")
    print(f"Temperatura promedio: {promedio:.2f} °C")
