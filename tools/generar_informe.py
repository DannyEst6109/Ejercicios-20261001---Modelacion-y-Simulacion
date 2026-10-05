"""Constructor del informe a partir de los resultados calculados."""
import json
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak

BASE = Path(__file__).resolve().parents[1]
R = json.loads((BASE/'output/resultados/resultados.json').read_text())
OUT = BASE/'output/pdf/Ejercicios 20261001.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
for name, file in [('TimesCustom','times.ttf'), ('TimesBold','timesbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name, 'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('TimesCustom', normal='TimesCustom', bold='TimesBold', italic='TimesCustom', boldItalic='TimesBold')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Texto', fontName='TimesCustom', fontSize=11, leading=14, spaceAfter=8))
styles.add(ParagraphStyle(name='Titulo', fontName='TimesBold', fontSize=18, leading=22, spaceAfter=14))
styles.add(ParagraphStyle(name='Subtitulo', fontName='TimesBold', fontSize=12, leading=16, spaceBefore=8, spaceAfter=8))
styles.add(ParagraphStyle(name='Centro', fontName='TimesCustom', fontSize=13, leading=19, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='CentroGrande', fontName='TimesBold', fontSize=18, leading=23, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Nota', fontName='TimesCustom', fontSize=9, leading=12, spaceAfter=8))
story=[]
def p(text, style='Texto'):
    story.append(Paragraph(text,styles[style]))
def title(text): p(text,'Titulo')
def sub(text): p(text,'Subtitulo')
def table(rows,widths=None,size=10):
    t=Table(rows,colWidths=widths,repeatRows=1,hAlign='CENTER')
    t.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),'TimesCustom'),('FONTNAME',(0,0),(-1,0),'TimesBold'),
        ('FONTSIZE',(0,0),(-1,-1),size),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8efeb')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f6f7f6')]),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEADING',(0,0),(-1,-1),size+1),
        ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
        ('LINEBELOW',(0,0),(-1,0),0.6,colors.HexColor('#21664f')),
    ]))
    story.append(t)
    story.append(Spacer(1,10))
def new(): story.append(PageBreak())
def chart(name): story.append(Image(str(BASE/f'output/resultados/{name}.png'),width=468,height=227.5))

# Portada: composición centrada basada en la referencia suministrada.
story.append(Spacer(1,25))
p('<b>Universidad del Valle de Guatemala</b>','Centro')
p('Facultad de Ingeniería','Centro')
p('MODELACIÓN Y SIMULACIÓN - SECCIÓN 20','Centro')
story.append(Spacer(1,48))
story.append(Image(str(BASE/'assets/logo_uvg.png'),width=230,height=230))
story.append(Spacer(1,54))
p('Ejercicios 20261001','CentroGrande')
p('Euler explícito y Runge-Kutta de cuarto orden','Centro')
story.append(Spacer(1,45))
p('Carlos Daniel Estrada Vega - 20853','Centro')
story.append(Spacer(1,48))
p('Guatemala, 5 de octubre de 2026','Centro')
new()
title('1. Objetivo y metodología')
p('Se aplican Euler y Runge-Kutta de cuarto orden (RK4) al enfriamiento de una bebida, la caída de un objeto y el crecimiento de una población. Luego se repite el ejercicio del café con distintos tamaños de paso para comparar precisión y costo.')
sub('Implementación directa')
p('Para una ecuación y\'(t) = f(t, y), Euler actualiza la solución usando la pendiente al inicio de cada paso:')
p('<b>y<sub>n+1</sub> = y<sub>n</sub> + h f(t<sub>n</sub>, y<sub>n</sub>)</b>')
p('RK4 utiliza cuatro pendientes por paso:')
for line in [
    'k<sub>1</sub> = f(t<sub>n</sub>, y<sub>n</sub>)',
    'k<sub>2</sub> = f(t<sub>n</sub> + h/2, y<sub>n</sub> + hk<sub>1</sub>/2)',
    'k<sub>3</sub> = f(t<sub>n</sub> + h/2, y<sub>n</sub> + hk<sub>2</sub>/2)',
    'k<sub>4</sub> = f(t<sub>n</sub> + h, y<sub>n</sub> + hk<sub>3</sub>)',
    '<b>y<sub>n+1</sub> = y<sub>n</sub> + (h/6)(k<sub>1</sub> + 2k<sub>2</sub> + 2k<sub>3</sub> + k<sub>4</sub>)</b>']: p(line)
p('El código separa los modelos de las funciones euler() y rk4(). Ambos métodos se programaron directamente, sin solucionadores automáticos. Matplotlib se utiliza para dibujar las gráficas.')
sub('Malla, presentación y verificación')
p('Cada simulación incluye t = 0 y t = 20. Se realizan N = 20/h pasos y se registran N + 1 valores, contando la condición inicial. Los resultados se redondean solo al mostrarlos; la población se calcula como una variable continua.')
p('Para comprobar la precisión, se comparan los resultados con las soluciones analíticas de los modelos. También se revisa que los valores respeten sus límites físicos. El error global de Euler es de orden h y el de RK4 de orden h⁴ para estas ecuaciones.')
new()
title('2. Enfriamiento de una bebida')
p('<b>Modelo:</b> dT/dt = -0.1(T - 20).<br/><b>Condición inicial:</b> T(0) = 90 °C.<br/><b>Configuración:</b> temperatura ambiente de 20 °C; h = 1 minuto; intervalo de 0 a 20 minutos; 20 pasos.')
chart('cafe')
p('Figura 1. Temperatura del café obtenida con Euler y RK4.','Nota')
sub('¿La rapidez de enfriamiento permanece constante?')
p('No. El café se enfría más rápido al inicio, cuando la diferencia con el ambiente es mayor: dT/dt = -7 °C/min. Conforme la temperatura se acerca a 20 °C, esa diferencia disminuye y el enfriamiento se vuelve más lento.')
r=R['cafe']
p(f"En el primer minuto, Euler reduce la temperatura en {90-r['euler'][1]:.4f} °C y RK4 en {90-r['rk4'][1]:.4f} °C. En el último minuto las reducciones son {r['euler'][-2]-r['euler'][-1]:.4f} °C y {r['rk4'][-2]-r['rk4'][-1]:.4f} °C, respectivamente. Esto confirma que el enfriamiento se hace más lento.")
sub('Comparación con la solución analítica')
p('La solución exacta es T(t) = 20 + 70 exp(-0.1t). A los 20 minutos da 29.473470 °C. Euler obtiene 28.510366 °C y RK4, 29.473487 °C. Sus errores absolutos son 0.963104 °C y 0.000017163 °C, respectivamente. Euler enfría el café más rápido de lo que indica el modelo.')
new()
title('Tabla 1. Temperatura por minuto')
p('h = 1 min. Se incluye la condición inicial y los 20 pasos.','Nota')
table([['t (min)','Euler (°C)','RK4 (°C)']]+[[f'{t:.0f}',f'{a:.6f}',f'{b:.6f}'] for t,a,b in zip(r['t'],r['euler'],r['rk4'])],[100,184,184])
p('Los valores se muestran con seis decimales; el cálculo no redondea las iteraciones.','Nota')
new()
title('3. Caída con resistencia del aire')
p('<b>Modelo:</b> dv/dt = 9.81 - 0.15v.<br/><b>Condición inicial:</b> v(0) = 0 m/s.<br/><b>Configuración:</b> m = 80 kg; c = 12 kg/s; h = 0.5 segundos; intervalo de 0 a 20 segundos; 40 pasos. Se toma positiva la dirección de caída.')
chart('caida')
p('Figura 2. Velocidad de caída obtenida con Euler y RK4.','Nota')
sub('¿La velocidad aumenta de la misma manera o se estabiliza?')
p('La velocidad aumenta cada vez más lentamente. La resistencia del aire crece con v y reduce la aceleración. Al igualar dv/dt a cero se obtiene la velocidad terminal: mg/c = 65.4 m/s. Ambas curvas se acercan a ese valor.')
p('La aceleración baja de 9.81 m/s² al inicio a unos 0.4884 m/s² a los 20 segundos, usando RK4. Por eso la curva se aplana, aunque la velocidad todavía aumenta al final de la simulación.')
sub('Comparación con la solución analítica')
p('La solución exacta es v(t) = 65.4[1 - exp(-0.15t)]. A los 20 segundos da 62.143926 m/s. Euler obtiene 62.507675 m/s y RK4, 62.143923 m/s. Los errores absolutos son 0.363749 m/s y 0.000002742 m/s. Con este paso, Euler sobreestima la velocidad.')
new()
title('Tabla 2. Velocidad cada 0.5 segundos')
p('h = 0.5 s. Se incluyen 41 valores, correspondientes a 40 pasos.','Nota')
r=R['caida']
table([['t (s)','Euler (m/s)','RK4 (m/s)']]+[[f'{t:.1f}',f'{a:.6f}',f'{b:.6f}'] for t,a,b in zip(r['t'],r['euler'],r['rk4'])],[100,184,184],9)
new()
title('4. Crecimiento con límite ambiental')
p('<b>Modelo:</b> dP/dt = 0.4P(1 - P/1000).<br/><b>Condición inicial:</b> P(0) = 100.<br/><b>Configuración:</b> r = 0.4 por día; K = 1000; h = 0.5 días; intervalo de 0 a 20 días; 40 pasos.')
chart('poblacion')
p('Figura 3. Población obtenida con Euler y RK4.','Nota')
sub('¿Qué ocurre cuando P se acerca a K = 1000?')
p('El crecimiento disminuye porque el factor 1 - P/K se acerca a cero. La población se estabiliza cerca de 1000, el límite de recursos del ambiente. La curva tiene forma de S: la tasa de crecimiento aumenta hasta P = 500 y luego disminuye.')
p('La tasa inicial es 36 por día y su máximo es 100 por día. Al día 20, RK4 da una población de 996.989729 y una tasa de apenas 1.2005 por día. Esto explica por qué la curva es casi horizontal al final.')
sub('Comparación con la solución analítica')
p('La solución exacta es P(t) = 1000/[1 + 9 exp(-0.4t)]. Al día 20 da 996.989924. Euler obtiene 997.960117 y RK4, 996.989729. Los errores absolutos son 0.970193 y 0.000195069. Ambos resultados están por debajo de K; RK4 es más cercano al valor exacto.')
new()
title('Tabla 3. Población cada 0.5 días')
p('h = 0.5 días. Se incluyen 41 valores, correspondientes a 40 pasos.','Nota')
r=R['poblacion']
table([['t (días)','Euler','RK4']]+[[f'{t:.1f}',f'{a:.6f}',f'{b:.6f}'] for t,a,b in zip(r['t'],r['euler'],r['rk4'])],[100,184,184],9)
new()
title('5. Sensibilidad al tamaño de paso')
p('Se repite el ejercicio del café con h = 1, 0.5 y 0.1 minutos, manteniendo los demás datos. El valor exacto al minuto 20 es 29.473469827 °C.')
table([['h (min)','Pasos','Euler (°C)','RK4 (°C)','|Euler - RK4|']]+[[str(s['h']),str(s['pasos']),f"{s['euler']:.9f}",f"{s['rk4']:.9f}",f"{s['diferencia']:.9f}"] for s in R['sensibilidad']],[55,45,124,124,120],9)
p('Tabla 4. Resultados finales y diferencia absoluta entre métodos.','Nota')
table([['h (min)','Error Euler (°C)','Error RK4 (°C)','Eval. Euler','Eval. RK4']]+[[str(s['h']),f"{s['error_euler']:.9f}",f"{s['error_rk4']:.3e}",str(s['evaluaciones_euler']),str(s['evaluaciones_rk4'])] for s in R['sensibilidad']],[55,120,120,85,88],9)
p('Tabla 5. Errores finales y evaluaciones de f. El costo se compara por evaluaciones, no por tiempo de ejecución.','Nota')
sub('¿Qué ocurre cuando disminuye h?')
p('Ambos métodos mejoran su precisión. Al reducir h de 1 a 0.1, el error de Euler baja de 0.963104 a 0.094893 °C y el de RK4, de 1.716 × 10⁻⁵ a 1.592 × 10⁻⁹ °C.')
sub('¿Qué ocurre con las iteraciones?')
p('Las iteraciones aumentan de 20 a 40 y luego a 200. Un paso diez veces menor requiere diez veces más iteraciones para cubrir el mismo intervalo.')
sub('¿Los resultados se vuelven más cercanos?')
p('Sí. La diferencia final baja de 0.963121 a 0.477620 y luego a 0.094893 °C. La comparación con la solución exacta confirma que ambos métodos mejoran.')
sub('¿Cuál es más sensible al tamaño de paso?')
p('Euler muestra un cambio mayor en el resultado final: 0.868211 °C entre h = 1 y h = 0.1, frente a 0.000017161 °C en RK4. En este ejercicio, Euler necesita pasos menores para mejorar su precisión. El error de RK4 disminuye más rápidamente gracias a su cuarto orden.')
sub('¿Qué relación existe entre precisión y costo?')
p('Reducir h mejora la precisión, pero aumenta el trabajo. Euler evalúa f una vez por paso y RK4, cuatro veces. Aun así, RK4 con h = 1 tiene menos error que Euler con h = 0.1 y requiere 80 evaluaciones frente a 200. En este caso, RK4 consigue mayor precisión con menos evaluaciones.')
new()
title('6. Conclusiones')
p('Los resultados siguen el comportamiento esperado: el café se acerca a 20 °C, la velocidad de caída a 65.4 m/s y la población a 1000. En los tres casos, la curva se aplana al acercarse a su límite.')
p('RK4 es más preciso que Euler con los pasos utilizados. Euler calcula una temperatura final menor que la exacta, y valores finales mayores en la velocidad y la población.')
p('Al disminuir el paso, aumentan las iteraciones y mejora la precisión. RK4 realiza más cálculos por paso, pero puede alcanzar un error menor con pasos más grandes. Por eso conviene considerar tanto el error como la cantidad de evaluaciones al elegir un método.')
sub('Cómo ejecutar el programa')
p('Código disponible en <a href="https://github.com/DannyEst6109/Ejercicios-20261001---Modelacion-y-Simulacion" color="#21664f"><u>GitHub: Ejercicios 20261001</u></a>.')
p('Se requiere Python 3 y Matplotlib. Desde la carpeta del código, ejecutar <b>python -m pip install -r requirements.txt</b> y luego <b>python ejercicios_20261001.py</b>.')
p('Las tablas CSV, las gráficas PNG y los resultados sin redondear se guardan en output/resultados. El programa también comprueba los límites físicos y la reducción de los errores.')
sub('Material utilizado')
p('Enunciado de la actividad: “Ejercicios de Programación - Euler y Runge-Kutta 4” (20261001-1.pdf). Las soluciones exactas se obtienen por separación de variables. Las tablas y gráficas se generaron con el código adjunto.')

def footer(c,doc):
    c.saveState()
    c.setFont('TimesCustom',9)
    c.setFillColor(colors.HexColor('#555555'))
    c.drawCentredString(306,27,str(doc.page))
    if doc.page>1:
        c.drawString(54,765,'Ejercicios 20261001')
        c.drawRightString(558,765,'Carlos Daniel Estrada Vega | 20853')
    c.restoreState()

doc=SimpleDocTemplate(str(OUT),pagesize=letter,rightMargin=72,leftMargin=72,topMargin=54,bottomMargin=48,
                      title='Ejercicios 20261001',author='Carlos Daniel Estrada Vega - 20853')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
