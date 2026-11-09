# TP final Python — EcoTech Solutions

Tres ejercicios organizados en carpetas independientes. Requiere Python 3.11 o superior.

## Ejecución
Desde la raíz:
```bash
python ejercicio_1/sensores.py
python ejercicio_2/inventario.py
python -m unittest discover -s ejercicio_1 -v
python -m unittest discover -s ejercicio_2 -v
```

## Proyecto Django
```bash
cd ejercicio_3
python -m venv .venv
```
Windows: `.venv\Scripts\activate`. Linux/macOS: `source .venv/bin/activate`.
```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```
Abrir http://127.0.0.1:8000/. Incluye configuración, rutas, aplicación, plantilla, WSGI y ASGI. Los datos son ejemplos en memoria; no requiere servicios externos. Configuración destinada al desarrollo local.

## Criterios
- Ejercicio 1: admite números y texto Celsius (C/°C), ubicación ausente, nula o vacía se convierte en "Desconocida". Lecturas inválidas generan ValueError. Lista vacía: ([], 0.0). El umbral se supera estrictamente.
- Ejercicio 2: stock privado con getter/setter y propiedad; se valida también al construir. JSON conserva tipo y atributos del panel. La demostración exporta catalogo_ecotech.json junto al script.
- Ejercicio 3: emisiones en kg CO2 = kWh × factor. Se acumulan todos los registros de cada planta antes de buscar el máximo. En empate gana la primera planta encontrada. Sin registros: emisiones 0 y planta_top None.

## Correspondencia con la consigna
1. sensores.py: limpiar_registro_sensor y generar_resumen_sensores.
2. inventario.py: StockInvalidoError, DispositivoEcológico, PanelSolar y GestorInventario.
3. sustentabilidad/servicios.py: cálculo y métricas; tests.py: TestCalculoEmisiones y pruebas de integración; views.py: vista_panel_sustentabilidad.
