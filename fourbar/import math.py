import math

class MecanismoCuatroBarras:
    def __init__(self, r1, r2, r3, r4):
        """
        Inicializa el mecanismo de 4 barras
        r1: longitud del eslabón fijo (bancada)
        r2: longitud del eslabón de entrada (manivela)
        r3: longitud del eslabón acoplador
        r4: longitud del eslabón de salida
        """
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r4 = r4
        self.tipo_grashof = self._verificar_grashof()
        
    def _verificar_grashof(self):
        """Verifica la condición de Grashof y determina el tipo de mecanismo"""
        longitudes = [self.r1, self.r2, self.r3, self.r4]
        longitudes.sort()
        s, p, q, l = longitudes  # s=más corta, l=más larga, p,q=intermedias
        
        suma_extremos = s + l
        suma_intermedias = p + q
        
        if suma_extremos < suma_intermedias:
            # Determinar qué eslabón es el más corto
            eslabones = [(self.r1, "fijo"), (self.r2, "entrada"), 
                        (self.r3, "acoplador"), (self.r4, "salida")]
            min_eslabon = min(eslabones, key=lambda x: x[0])
            
            if min_eslabon[1] == "entrada":
                return "manivela-balancín"
            elif min_eslabon[1] == "fijo":
                return "doble manivela"
            elif min_eslabon[1] == "acoplador":
                return "doble balancín (Grashof)"
            else:
                return "manivela-balancín"
                
        elif suma_extremos == suma_intermedias:
            return "mecanismo plegable"
        else:
            return "triple balancín (no Grashof)"
    
    def ecuaciones_lazo(self, theta2, theta3, theta4):
        """
        Ecuaciones de lazo vectorial para el mecanismo de 4 barras
        Retorna [f1, f2] donde f1 y f2 deben ser cero
        """
        # Ecuación de lazo: r2 + r3 = r1 + r4
        # Componente X: r2*cos(θ2) + r3*cos(θ3) = r1*cos(0) + r4*cos(θ4)
        # Componente Y: r2*sin(θ2) + r3*sin(θ3) = r1*sin(0) + r4*sin(θ4)
        
        f1 = (self.r2 * math.cos(theta2) + self.r3 * math.cos(theta3) - 
              self.r1 - self.r4 * math.cos(theta4))
        f2 = (self.r2 * math.sin(theta2) + self.r3 * math.sin(theta3) - 
              self.r4 * math.sin(theta4))
        
        return [f1, f2]
    
    def jacobiano(self, theta2, theta3, theta4):
        """
        Calcula la matriz Jacobiana del sistema de ecuaciones
        """
        # Derivadas parciales de f1 respecto a theta3 y theta4
        df1_dtheta3 = -self.r3 * math.sin(theta3)
        df1_dtheta4 = self.r4 * math.sin(theta4)
        
        # Derivadas parciales de f2 respecto a theta3 y theta4
        df2_dtheta3 = self.r3 * math.cos(theta3)
        df2_dtheta4 = -self.r4 * math.cos(theta4)
        
        return [[df1_dtheta3, df1_dtheta4],
                [df2_dtheta3, df2_dtheta4]]
    
    def determinante_2x2(self, matriz):
        """Calcula el determinante de una matriz 2x2"""
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
    
    def inversa_2x2(self, matriz):
        """Calcula la inversa de una matriz 2x2"""
        det = self.determinante_2x2(matriz)
        if abs(det) < 1e-10:
            return None  # Matriz singular
        
        return [[matriz[1][1]/det, -matriz[0][1]/det],
                [-matriz[1][0]/det, matriz[0][0]/det]]
    
    def multiplicar_matriz_vector(self, matriz, vector):
        """Multiplica una matriz 2x2 por un vector 2x1"""
        return [matriz[0][0]*vector[0] + matriz[0][1]*vector[1],
                matriz[1][0]*vector[0] + matriz[1][1]*vector[1]]
    
    def newton_raphson(self, theta2, theta3_inicial=None, theta4_inicial=None, 
                      tolerancia=1e-8, max_iter=50):
        """
        Resuelve las ecuaciones de lazo usando Newton-Raphson
        """
        # Estimaciones iniciales si no se proporcionan
        if theta3_inicial is None:
            theta3_inicial = math.pi/4
        if theta4_inicial is None:
            theta4_inicial = math.pi/4
            
        theta3 = theta3_inicial
        theta4 = theta4_inicial
        
        for i in range(max_iter):
            # Evaluar las funciones
            f = self.ecuaciones_lazo(theta2, theta3, theta4)
            
            # Verificar convergencia
            error = math.sqrt(f[0]**2 + f[1]**2)
            if error < tolerancia:
                return theta3, theta4, True, i+1, error
            
            # Calcular Jacobiano
            J = self.jacobiano(theta2, theta3, theta4)
            
            # Verificar singularidad
            det_J = self.determinante_2x2(J)
            if abs(det_J) < 1e-10:
                return theta3, theta4, False, i+1, error
            
            # Calcular corrección
            J_inv = self.inversa_2x2(J)
            delta = self.multiplicar_matriz_vector(J_inv, [-f[0], -f[1]])
            
            # Actualizar variables
            theta3 += delta[0]
            theta4 += delta[1]
        
        return theta3, theta4, False, max_iter, error
    
    def verificar_singularidad(self, theta2, theta3, theta4, umbral=1e-3):
        """
        Verifica si el mecanismo está cerca de una singularidad
        """
        J = self.jacobiano(theta2, theta3, theta4)
        det_J = abs(self.determinante_2x2(J))
        
        if det_J < umbral:
            return True, det_J
        return False, det_J
    
    def calcular_posicion(self, theta2_grados, configuracion="abierta"):
        """
        Calcula la posición de los eslabones para un ángulo de entrada dado
        """
        theta2 = math.radians(theta2_grados)
        
        # Estimaciones iniciales basadas en la configuración
        if configuracion == "abierta":
            theta3_inicial = math.pi/6
            theta4_inicial = math.pi/6
        else:  # configuración cruzada
            theta3_inicial = 2*math.pi/3
            theta4_inicial = 2*math.pi/3
        
        # Resolver usando Newton-Raphson
        theta3, theta4, convergio, iteraciones, error = self.newton_raphson(
            theta2, theta3_inicial, theta4_inicial)
        
        if not convergio:
            return None
        
        # Verificar singularidad
        es_singular, det_jacobiano = self.verificar_singularidad(theta2, theta3, theta4)
        
        # Calcular coordenadas de los puntos
        # Punto A (origen): (0, 0)
        # Punto B: extremo del eslabón 2
        xB = self.r2 * math.cos(theta2)
        yB = self.r2 * math.sin(theta2)
        
        # Punto C: extremo del eslabón 3
        xC = xB + self.r3 * math.cos(theta3)
        yC = yB + self.r3 * math.sin(theta3)
        
        # Punto D: extremo del eslabón 4 (debe coincidir con extremo fijo)
        xD = self.r1  # El eslabón fijo va de (0,0) a (r1,0)
        yD = 0
        
        return {
            'theta2': math.degrees(theta2),
            'theta3': math.degrees(theta3),
            'theta4': math.degrees(theta4),
            'puntos': {
                'A': (0, 0),
                'B': (xB, yB),
                'C': (xC, yC),
                'D': (xD, yD)
            },
            'convergencia': {
                'convergio': convergio,
                'iteraciones': iteraciones,
                'error': error
            },
            'singularidad': {
                'es_singular': es_singular,
                'determinante': det_jacobiano
            }
        }
    
    def analizar_rango_movimiento(self, paso_grados=1):
        """
        Analiza el rango completo de movimiento del mecanismo
        """
        resultados = []
        singularidades = []
        
        for theta2_grados in range(0, 360, paso_grados):
            # Probar ambas configuraciones
            for config in ["abierta", "cruzada"]:
                resultado = self.calcular_posicion(theta2_grados, config)
                
                if resultado is not None:
                    resultados.append({
                        'theta2': theta2_grados,
                        'configuracion': config,
                        'resultado': resultado
                    })
                    
                    # Identificar singularidades
                    if resultado['singularidad']['es_singular']:
                        singularidades.append({
                            'theta2': theta2_grados,
                            'configuracion': config,
                            'determinante': resultado['singularidad']['determinante']
                        })
                else:
                    singularidades.append({
                        'theta2': theta2_grados,
                        'configuracion': config,
                        'determinante': 0,
                        'no_converge': True
                    })
        
        return resultados, singularidades
    
    def imprimir_info(self):
        """Imprime información del mecanismo"""
        print("=== ANÁLISIS DEL MECANISMO DE 4 BARRAS ===")
        print(f"Eslabón fijo (r1): {self.r1}")
        print(f"Eslabón de entrada (r2): {self.r2}")
        print(f"Eslabón acoplador (r3): {self.r3}")
        print(f"Eslabón de salida (r4): {self.r4}")
        print(f"Tipo según Grashof: {self.tipo_grashof}")
        print("=" * 45)

# Ejemplo de uso
def ejemplo_uso():
    # Definir las dimensiones del mecanismo
    r1 = 120  # Eslabón fijo
    r2 = 30   # Eslabón de entrada
    r3 = 90   # Eslabón acoplador
    r4 = 80   # Eslabón de salida
    
    # Crear el mecanismo
    mecanismo = MecanismoCuatroBarras(r1, r2, r3, r4)
    mecanismo.imprimir_info()
    
    # Calcular posición para un ángulo específico
    theta2_entrada = 15  # grados
    resultado = mecanismo.calcular_posicion(theta2_entrada)
    
    if resultado:
        print(f"\nPosición para θ2 = {theta2_entrada}°:")
        print(f"θ3 = {resultado['theta3']:.2f}°")
        print(f"θ4 = {resultado['theta4']:.2f}°")
        print(f"Punto B: ({resultado['puntos']['B'][0]:.3f}, {resultado['puntos']['B'][1]:.3f})")
        print(f"Punto C: ({resultado['puntos']['C'][0]:.3f}, {resultado['puntos']['C'][1]:.3f})")
        
        if resultado['singularidad']['es_singular']:
            print("⚠️  ADVERTENCIA: Posición cerca de singularidad")
        
        print(f"Convergencia en {resultado['convergencia']['iteraciones']} iteraciones")
    else:
        print("❌ No se pudo calcular la posición (singularidad o no convergencia)")

# Ejecutar ejemplo
if __name__ == "__main__":
    ejemplo_uso()
