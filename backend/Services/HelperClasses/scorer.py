import math
from sklearn.metrics import mean_squared_error
import numpy as np

class Scorer:
    def get_score(self, trainY, trainPredict, testY, testPredict):
        trainScore = math.sqrt(mean_squared_error(trainY, trainPredict))
        testScore = math.sqrt(mean_squared_error(testY, testPredict))
        
       
        if hasattr(trainScore, 'item'):
            trainScore = trainScore.item()
        if hasattr(testScore, 'item'):
            testScore = testScore.item()
            
        return float(trainScore), float(testScore)

    def get_mape(self, trainY, trainPredict, testY, testPredict):
        trainY = np.array(trainY).astype(float)
        trainPredict = np.array(trainPredict).astype(float)
        testY = np.array(testY).astype(float)
        testPredict = np.array(testPredict).astype(float)
        
       
        trainY_nonzero = np.where(trainY == 0, np.finfo(float).eps, trainY)
        testY_nonzero = np.where(testY == 0, np.finfo(float).eps, testY)
        
        trainResult = np.mean(np.abs((trainY_nonzero - trainPredict) / trainY_nonzero)) * 100
        testResult = np.mean(np.abs((testY_nonzero - testPredict) / testY_nonzero)) * 100
        
        
        trainResult = float(trainResult)
        testResult = float(testResult)
        
        return trainResult, testResult