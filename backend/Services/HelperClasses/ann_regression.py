from keras.layers import Dense
from keras.models import Sequential
from tensorflow import keras
from Services.HelperClasses.ann_base import AnnBase
import os


MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'Models')
MODEL_NAME = os.path.join(MODELS_DIR, 'current_model.keras')

class AnnRegression(AnnBase):
    

    def get_model(self, input_dim):

        model = Sequential()
    
        if self.number_of_hidden_layers > 0:
            model.add(Dense(
                self.number_of_neurons_in_first_hidden_layer,
                input_dim=input_dim,  
                kernel_initializer=self.kernel_initializer,
                activation=self.activation_function
            ))
        
        if self.number_of_hidden_layers > 1:
            for i in range(self.number_of_hidden_layers - 1):
                model.add(Dense(
                    self.number_of_neurons_in_other_hidden_layers,
                    kernel_initializer=self.kernel_initializer,
                    activation=self.activation_function
                ))
    
        model.add(Dense(1, kernel_initializer=self.kernel_initializer, activation='linear'))
        return model



    def get_model_from_path(self, path):
        model = keras.models.load_model(path)
        return model

    

    def compile_and_fit(self, trainX, trainY):
    
        self.model = self.get_model(input_dim=trainX.shape[1])
        self.model.compile(loss=self.cost_function, optimizer=self.optimizer)
        self.trainX = trainX
    
        os.makedirs(MODELS_DIR, exist_ok=True)
    
        self.model.fit(trainX, trainY, epochs=self.epoch_number, 
                  batch_size=self.batch_size_number, verbose=self.verbose)
        self.model.save(MODEL_NAME)
        print(f" Model saved: {MODEL_NAME}")
    
        return MODEL_NAME

    def use_current_model(self, path, trainX):
        self.trainX = trainX
        self.model = self.get_model_from_path(path)

    def get_predict(self, testX):
        trainPredict = self.model.predict(self.trainX)
        testPredict = self.model.predict(testX)
        return trainPredict, testPredict

    def compile_fit_predict(self, trainX, trainY, testX):
        self.compile_and_fit(trainX, trainY)
        return self.get_predict(testX)

    def predict_with_model_from_path(self, testX, path):
        self.model = self.get_model_from_path(path)
        return self.get_predict_test(testX)

    def get_predict_test(self, testX):
        testPredict = self.model.predict(testX)
        return testPredict
    

    def set_hyperparameters(self, hyperparams: dict):
       
        if 'epochs' in hyperparams:
            self.epoch_number = int(hyperparams['epochs'])
        if 'batch_size' in hyperparams:
            self.batch_size_number = int(hyperparams['batch_size'])
        if 'layers' in hyperparams:
            self.number_of_hidden_layers = int(hyperparams['layers'])
        if 'neurons' in hyperparams:
            self.number_of_neurons_in_first_hidden_layer = int(hyperparams['neurons'])
            self.number_of_neurons_in_other_hidden_layers = int(hyperparams['neurons'])
        if 'activation' in hyperparams:
            self.activation_function = str(hyperparams['activation'])
        if 'optimizer' in hyperparams:
            self.optimizer = str(hyperparams['optimizer'])
        if 'learning_rate' in hyperparams:
        
            import tensorflow as tf
            if self.optimizer == 'adam':
                self.optimizer = tf.keras.optimizers.Adam(learning_rate=float(hyperparams['learning_rate']))
            elif self.optimizer == 'sgd':
                self.optimizer = tf.keras.optimizers.SGD(learning_rate=float(hyperparams['learning_rate']))
           


    def save_model(self, model_name='current_model'):
        
        if not model_name.endswith('.keras') and not model_name.endswith('.h5'):
            model_name = model_name + '.keras'
        
       
        model_path = os.path.join(MODELS_DIR, model_name)
        
       
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
     
        if self.model:
            self.model.save(model_path)
            print(f"Model additionally saved:{model_path}")
            return model_path
        else:
            print("The model is not trained, it has nothing to save")
            return None