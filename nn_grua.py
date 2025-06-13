import ujson
import math

class NNGruapred:
    def __init__(self, weights_path, scaler_path):
        with open(weights_path, 'r') as f:
            self.weights = ujson.load(f)
        with open(scaler_path, 'r') as f:
            self.scalers = ujson.load(f)

    def escalar_entrada(self, x, y):
        mean = self.scalers['X_mean']
        scale = self.scalers['X_scale']
        return [(x - mean[0]) / scale[0], (y - mean[1]) / scale[1]]

    def desescalar_salida(self, thetas):
        mean = self.scalers['y_mean']
        scale = self.scalers['y_scale']
        return [thetas[i] * scale[i] + mean[i] for i in range(3)]

    def relu(self, vec):
        return [max(0, v) for v in vec]

    def matvec(self, mat, vec):
        return [
            sum(mat[i][j] * vec[j] for j in range(len(vec)))
            for i in range(len(mat))
        ]

    def predecir_grua(self, x, y):
        inp = self.escalar_entrada(x, y)
        out1 = self.matvec(self.weights['layer1_weight'], inp)
        out1 = [out1[i] + self.weights['layer1_bias'][i] for i in range(64)]
        out1 = self.relu(out1)
        out2 = self.matvec(self.weights['layer2_weight'], out1)
        out2 = [out2[i] + self.weights['layer2_bias'][i] for i in range(64)]
        out2 = self.relu(out2)
        out3 = self.matvec(self.weights['layer3_weight'], out2)
        out3 = [out3[i] + self.weights['layer3_bias'][i] for i in range(3)]
        thetas = self.desescalar_salida(out3)
        return thetas

    def predecir_angs(self, trayectoria):
        return [self.predecir_grua(x, y) for (x, y) in trayectoria]
