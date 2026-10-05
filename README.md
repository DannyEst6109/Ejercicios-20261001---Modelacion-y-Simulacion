# Ejercicios 20261001

**MODELACIÓN Y SIMULACIÓN - SECCIÓN 20**  
Universidad del Valle de Guatemala, Facultad de Ingeniería  
Carlos Daniel Estrada Vega - 20853

Implementación de Euler explícito y Runge-Kutta de cuarto orden (RK4) para tres ecuaciones diferenciales. Los métodos están programados directamente, sin solucionadores automáticos.

## Ejercicios

| Modelo | Condición inicial | Parámetros | Paso | Intervalo |
| --- | --- | --- | --- | --- |
| Enfriamiento del café | T(0) = 90 °C | k = 0.1 min⁻¹; Ta = 20 °C | 1 min | 0 a 20 min |
| Caída con resistencia del aire | v(0) = 0 m/s | g = 9.81 m/s²; m = 80 kg; c = 12 kg/s | 0.5 s | 0 a 20 s |
| Crecimiento logístico | P(0) = 100 | r = 0.4 día⁻¹; K = 1000 | 0.5 días | 0 a 20 días |

El ejercicio del café también se ejecuta con pasos de 1, 0.5 y 0.1 minutos para comparar precisión, iteraciones y costo. Las soluciones analíticas permiten comprobar los errores.

## Archivos

- [Informe PDF](output/pdf/Ejercicios%2020261001.pdf): tablas completas, gráficas, respuestas de análisis y conclusiones.
- [Entrega en ZIP](output/Ejercicios%2020261001.zip): informe, código, resultados e instrucciones.
- `ejercicios_20261001.py`: modelos, métodos numéricos y generación de resultados.
- `requirements.txt`: dependencia para ejecutar las simulaciones y generar las gráficas.
- `output/resultados/`: tablas CSV, gráficas PNG y resultados JSON sin redondear.
- `tools/generar_informe.py` y `assets/logo_uvg.png`: fuente y logotipo para regenerar el informe.

## Ejecutar

Con Python 3, abrir una terminal en la carpeta del repositorio y ejecutar:

```bash
python -m pip install -r requirements.txt
python ejercicios_20261001.py
```

Los archivos de resultados se guardan en `output/resultados/`. El programa comprueba la cantidad de pasos, los límites físicos y la reducción del error al disminuir el paso.

## Regenerar el informe

El PDF ya está incluido. Para regenerarlo en Windows, después de ejecutar las simulaciones:

```bash
python -m pip install reportlab
python tools/generar_informe.py
```

El generador usa las fuentes Times New Roman de `C:/Windows/Fonts` y guarda el informe en `output/pdf/`. El ZIP es una copia preparada para la entrega; no se actualiza automáticamente al ejecutar estos comandos.

## Repositorio

[Ejercicios 20261001 - Modelación y Simulación](https://github.com/DannyEst6109/Ejercicios-20261001---Modelacion-y-Simulacion)
