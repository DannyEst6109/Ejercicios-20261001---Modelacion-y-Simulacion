"""Euler y RK4 implementados directamente para Ejercicios 20261001.

Autor: Carlos Daniel Estrada Vega, 20853.
Ejecutar: python ejercicios_20261001.py
Dependencia para gráficas: matplotlib (pip install matplotlib).
Los cálculos usan la biblioteca estándar; no se usan solucionadores de EDO.
"""
import csv
import json
import math
from pathlib import Path


def integrar(f, y0, t0, tf, h, metodo):
    """Integra en una malla uniforme; incluye los extremos t0 y tf."""
    if h <= 0 or tf <= t0:
        raise ValueError('El paso debe ser positivo y tf mayor que t0.')
    n = round((tf - t0) / h)
    if not math.isclose(n * h, tf - t0, rel_tol=1e-12, abs_tol=1e-12):
        raise ValueError('El intervalo debe ser divisible entre h.')
    tiempos = [t0 + i * h for i in range(n + 1)]
    valores = [float(y0)]
    for t in tiempos[:-1]:
        y = valores[-1]
        if metodo == 'euler':
            siguiente = y + h * f(t, y)
        elif metodo == 'rk4':
            k1 = f(t, y)
            k2 = f(t + h / 2, y + h * k1 / 2)
            k3 = f(t + h / 2, y + h * k2 / 2)
            k4 = f(t + h, y + h * k3)
            siguiente = y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        else:
            raise ValueError('Método desconocido.')
        valores.append(siguiente)
    return tiempos, valores


def euler(f, y0, t0, tf, h):
    return integrar(f, y0, t0, tf, h, 'euler')


def rk4(f, y0, t0, tf, h):
    return integrar(f, y0, t0, tf, h, 'rk4')


def enfriamiento(t, temperatura):
    return -0.1 * (temperatura - 20)


def caida(t, velocidad):
    return 9.81 - (12 / 80) * velocidad


def poblacion(t, cantidad):
    return 0.4 * cantidad * (1 - cantidad / 1000)


MODELOS = [
    ('cafe', enfriamiento, 90, 1, 'Enfriamiento de una bebida',
     'Tiempo (min)', 'Temperatura (°C)', lambda t: 20 + 70 * math.exp(-0.1 * t)),
    ('caida', caida, 0, 0.5, 'Caída con resistencia del aire',
     'Tiempo (s)', 'Velocidad (m/s)', lambda t: 65.4 * (1 - math.exp(-0.15 * t))),
    ('poblacion', poblacion, 100, 0.5, 'Crecimiento logístico',
     'Tiempo (días)', 'Población', lambda t: 1000 / (1 + 9 * math.exp(-0.4 * t))),
]


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    salida = Path(__file__).resolve().parent / 'output' / 'resultados'
    salida.mkdir(parents=True, exist_ok=True)
    resultados = {}
    for nombre, f, y0, h, titulo, eje_x, eje_y, exacta in MODELOS:
        t, ye = euler(f, y0, 0, 20, h)
        _, yr = rk4(f, y0, 0, 20, h)
        ya = [exacta(x) for x in t]
        errores_e = [abs(a - b) for a, b in zip(ye, ya)]
        errores_r = [abs(a - b) for a, b in zip(yr, ya)]
        assert len(t) == round(20 / h) + 1 and t[-1] == 20
        assert all(math.isfinite(x) for x in ye + yr)
        assert max(errores_r) < max(errores_e)
        if nombre == 'cafe':
            assert all(20 < x <= 90 for x in ye + yr)
            assert all(a > b for a, b in zip(ye, ye[1:]))
        elif nombre == 'caida':
            assert all(0 <= x < 65.4 for x in ye + yr)
        else:
            assert all(100 <= x < 1000 for x in ye + yr)
        with (salida / f'{nombre}.csv').open('w', newline='', encoding='utf-8-sig') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(['t', 'Euler', 'RK4', 'Analítica', 'Error Euler', 'Error RK4'])
            escritor.writerows(zip(t, ye, yr, ya, errores_e, errores_r))
        fig, ax = plt.subplots(figsize=(7.2, 3.5), layout='constrained')
        ax.plot(t, ye, '--', color='#b15c26', label='Euler', linewidth=2)
        ax.plot(t, yr, color='#21664f', label='RK4', linewidth=2)
        ax.set(xlabel=eje_x, ylabel=eje_y, title=titulo)
        ax.grid(alpha=0.2)
        ax.legend()
        fig.savefig(salida / f'{nombre}.png', dpi=200)
        plt.close(fig)
        resultados[nombre] = dict(t=t, euler=ye, rk4=yr, exacta=ya,
                                  error_euler=errores_e, error_rk4=errores_r)
    sensibilidad = []
    for h in (1, 0.5, 0.1):
        t, ye = euler(enfriamiento, 90, 0, 20, h)
        _, yr = rk4(enfriamiento, 90, 0, 20, h)
        exacta = 20 + 70 * math.exp(-2)
        n = len(t) - 1
        sensibilidad.append(dict(h=h, pasos=n, euler=ye[-1], rk4=yr[-1],
                                  diferencia=abs(ye[-1] - yr[-1]),
                                  error_euler=abs(ye[-1] - exacta),
                                  error_rk4=abs(yr[-1] - exacta),
                                  evaluaciones_euler=n, evaluaciones_rk4=4*n))
    assert all(a['error_euler'] > b['error_euler'] and a['error_rk4'] > b['error_rk4']
               for a, b in zip(sensibilidad, sensibilidad[1:]))
    with (salida / 'sensibilidad.csv').open('w', newline='', encoding='utf-8-sig') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(sensibilidad[0]))
        escritor.writeheader()
        escritor.writerows(sensibilidad)
    resultados['sensibilidad'] = sensibilidad
    (salida / 'resultados.json').write_text(json.dumps(resultados, indent=2), encoding='utf-8')
    for nombre in ('cafe', 'caida', 'poblacion'):
        r = resultados[nombre]
        print(f"{nombre}: Euler={r['euler'][-1]:.9f}, RK4={r['rk4'][-1]:.9f}, "
              f"analítica={r['exacta'][-1]:.9f}")
    print('Verificación completada: mallas, valores físicos, errores y convergencia.')
    print(f'Resultados guardados en: {salida}')


if __name__ == '__main__':
    main()
