import numpy
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


class CustomPreparer:
   
    def __init__(self, dataframe, number_of_columns, share_for_training):
        self.feature_scaler = MinMaxScaler(feature_range=(0, 1))
        self.target_scaler = MinMaxScaler(feature_range=(0, 1))

        self.datasetOrig = dataframe.values.astype('float32')
        self.number_of_columns = number_of_columns
        self.predictor_column_no = list(dataframe.columns).index("power_load") 
        self.share_for_training = share_for_training


        
    def prepare_for_training(self):
    
        target = self.datasetOrig[:, self.predictor_column_no].reshape(-1, 1)
        features = numpy.delete(self.datasetOrig, self.predictor_column_no, axis=1)

    
        train_size = int(len(features) * self.share_for_training)
        train_features, test_features = features[:train_size], features[train_size:]
        train_target, test_target = target[:train_size], target[train_size:]

    
    
        train_features = pd.DataFrame(train_features).interpolate(method='linear', limit_direction='both').fillna(method='bfill').fillna(method='ffill').values
        test_features = pd.DataFrame(test_features).interpolate(method='linear', limit_direction='both').fillna(method='bfill').fillna(method='ffill').values

        train_target = pd.DataFrame(train_target).interpolate(method='linear', limit_direction='both').fillna(method='bfill').fillna(method='ffill').values
        test_target = pd.DataFrame(test_target).interpolate(method='linear', limit_direction='both').fillna(method='bfill').fillna(method='ffill').values

    
        self.feature_scaler.fit(train_features)
        self.target_scaler.fit(train_target)

        print(" Target scaler fitted to min/max:",
          self.target_scaler.data_min_,
          self.target_scaler.data_max_)

    
        train_features_scaled = self.feature_scaler.transform(train_features)
        test_features_scaled = self.feature_scaler.transform(test_features)

        train_target_scaled = self.target_scaler.transform(train_target)
        test_target_scaled = self.target_scaler.transform(test_target)

    
        train_dataset = numpy.concatenate((train_features_scaled, train_target_scaled), axis=1)
        test_dataset = numpy.concatenate((test_features_scaled, test_target_scaled), axis=1)

        look_back = train_dataset.shape[1]
        trainX, trainY = self.create_dataset(train_dataset, look_back)
        testX, testY = self.create_dataset(test_dataset, look_back)

        self.trainX, self.trainY = trainX, trainY
        self.testX, self.testY = testX, testY
        return trainX.copy(), trainY.copy(), testX.copy(), testY.copy()

   


    def prepare_for_predict(self):
    
        features = numpy.delete(self.datasetOrig, self.predictor_column_no, axis=1)
        target = self.datasetOrig[:, self.predictor_column_no].reshape(-1, 1)  
    
        print(" DEBUG forecast features shape:", features.shape)
        print(" DEBUG forecast columns count:", features.shape[1])
    
    
        if not hasattr(self.feature_scaler, "min_"):
            print(" The scaler was not fitted, I fit it on the prediction input...")
            self.feature_scaler.fit(features)

    
        features_scaled = self.feature_scaler.transform(features)
    

        dataset = numpy.concatenate((features_scaled, target), axis=1)
    
    
        look_back = dataset.shape[1]
        testX, testY = self.create_dataset(dataset, look_back)
    
    
        testX = numpy.reshape(testX, (testX.shape[0], testX.shape[1]))
        self.testX, self.testY = testX, testY
    
        return testX.copy(), testY.copy()

    
    

    def inverse_transform(self, trainPredict, testPredict):
    
        trainPredict = numpy.reshape(trainPredict, (trainPredict.shape[0], 1))
        testPredict = numpy.reshape(testPredict, (testPredict.shape[0], 1))

    
        trainY = numpy.reshape(self.trainY, (self.trainY.shape[0], 1))
        testY = numpy.reshape(self.testY, (self.testY.shape[0], 1))

    
        trainPredict = self.target_scaler.inverse_transform(trainPredict)
        trainY = self.target_scaler.inverse_transform(trainY)
        testPredict = self.target_scaler.inverse_transform(testPredict)
        testY = self.target_scaler.inverse_transform(testY)

    
        trainPredict = trainPredict.flatten()
        trainY = trainY.flatten()
        testPredict = testPredict.flatten()
        testY = testY.flatten()

        return trainPredict, trainY, testPredict, testY


   

    def inverse_transform_test_predict(self, testPredict):
    
        if testPredict.ndim == 1:
            testPredict = testPredict.reshape(-1, 1)
        elif testPredict.ndim == 3:
            testPredict = testPredict.reshape(-1, 1)

    
        if not hasattr(self.target_scaler, "min_"):
            print("The target scaler was not fitted, I am fitting it on a dummy target...")
            dummy_target = self.datasetOrig[:, self.predictor_column_no].reshape(-1, 1)
            self.target_scaler.fit(dummy_target)

    
        return self.target_scaler.inverse_transform(testPredict).flatten()




    def create_dataset(self, dataset, look_back):
        dataX, dataY = [], []
        n_features = dataset.shape[1]

    
        if look_back > n_features - 1:
            look_back = n_features - 1

        for i in range(len(dataset)-1):
        
            a = dataset[i, :-1]
            dataX.append(a)
       
            dataY.append(dataset[i, -1])

        dataX = numpy.array(dataX)
        dataY = numpy.array(dataY)

    
        print("DEBUG dataset shape in create_dataset:", dataset.shape)
        print("DEBUG dataX shape:", dataX.shape)
        print("DEBUG dataY shape:", dataY.shape)

        return dataX, dataY


    def invert_function_load(self, x, a, b, min, max):
        return (((b - a) * (x - min) )/ (max - min)) + a


    def fit_scalers_for_forecast(self, df):
    
        data = df.values.astype('float32')

    
        features = numpy.delete(data, self.predictor_column_no, axis=1)
        target = data[:, self.predictor_column_no].reshape(-1, 1)

    
        self.feature_scaler.fit(features)

   
        self.target_scaler.fit(target)

        print(" Scalers fitted for forecast (features + target)")