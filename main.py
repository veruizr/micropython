from nn_grua import NNGruapred
import math

# Instanciar la clase con los archivos exportados
nn = NNGruapred('grua_weights.json', 'scaler_params.json')

# Trayectoria de cinco puntos de ejemplo
trayectoria = [
    (4.0, 5.0),
    (5.2, 6.3),
    (6.0, 7.5),
    (7.2, 7.9),
    (8.1, 8.6)
]

# Obtener ángulos para todos los puntos de la trayectoria
resultados = nn.predecir_angs(trayectoria)

# Imprimir resultados
for i, (punto, ang) in enumerate(zip(trayectoria, resultados)):
    ang_grados = [round(math.degrees(a), 3) for a in ang]
    ang_radianes = [round(a, 6) for a in ang]
    print(f"Punto {i+1} ({punto[0]}, {punto[1]}):")
    print(f"  Ángulos (radianes): {ang_radianes}")
    print(f"  Ángulos (grados):   {ang_grados}")
