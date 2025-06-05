# micropython
##Este Repositorio contiene una aplicación para ejecutarse en micropython para microcontroladores
## Análisis de Posición en mecanismo de cuatro barras
  ### 1. Generador de datos aleatorios para construir un dataset
      Genera datos aleatorios para las longitudes de los eslabones y el ángulo del eslabón de entrada
  ### 2. Cálculo de salidas
      Realiza el análsis de posición para un mecanismo de 4 barras calculando mediante Newton-Raphson los ángulos de los eslabones acoplador y de salida del mecanismo
      Define condición de Grashof y determina si hay configuración abierta o cerrada.
  ### 3. Genera el dataset
      Construye el dataset para un número de muestras capaz de guardarse en la memoria del microcontrolador para transferirse mediante una memoria flash/usb
  ### 4. Formulación de la red neuronal (se realiza en python para poder usar librerías especificas para NN)
      Se programa una red neuronal usando tensorflow y pytorch, 
      el Dataset generado se utiliza para entrenamiento
      se normalizan los datos de las entradas y se definen las condiciones del entrenamiento y prueba
      se exportan los escaladores, los pesos y los errores o sesgos en formato .txt para ser usado por el microcontrolador
  ### 5. Uso de la red neuronal en el microcontrolador
      Se implementa una red neuronal simplificada,creando una clase que agrupa las funciones de carga de escaladores y pesos y se incluyen las funciones de activación reLU y la función sigmoide para identificar la configuración (cruzada /abierta) del mecanismo.
      Finalmente se usa la red neuronal para predecir la posición de los eslabones acoplador y de salida y la configuración del mecanismo para un conjunto de datos manual.
      
