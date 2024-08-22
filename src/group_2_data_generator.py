import numpy as np


class DataGenerator:

    def __init__(self, num_value):
        self.num_value = num_value
        self.value = {"base": 10, "delta": 0.15}

    def __generateDataPoints(self):
        return np.random.random(self.num_value)

    def getTemperatureSensorDataset(self, min, max):
        x = self.__generateDataPoints()
        m = max - min
        c = min
        y = m * x + c
        return y

    def getTemperatureSensorData(self, min, max):
        x = np.random.random(1)[0]
        m = max - min
        c = min
        y = m * x + c
        return y
