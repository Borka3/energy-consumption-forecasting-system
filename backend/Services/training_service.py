import time
from pathlib import Path
import sys
import os
import tensorflow as tf

os.makedirs("Services/Models", exist_ok=True)  


sys.path.append(str(Path(__file__).parent.parent))

from Services import preprocessing_service
from Services.HelperClasses.custom_preparer import CustomPreparer
from Services.HelperClasses.ann_regression import AnnRegression
from Services.HelperClasses.scorer import Scorer

NUMBER_OF_COLUMNS = 15
SHARE_FOR_TRAINING = 0.85


def train_model(start_date, end_date, hyperparams=None):

    print("=" * 60)
    region = "N.Y.C."

    print("=" * 60)
    
    try:
       
        print("Preprocessing for period and region...")
       
        dataframe = preprocessing_service.preprocess_for_training(start_date, end_date, region)
        
        if dataframe.empty:
            print(f"There is no data for the region '{region}' in the period  {start_date} to  {end_date}")
            return {
                'success': False,
                'message': f'No data for the region {region} in a given period'
            }
        
        print(f"Preprocessed {len(dataframe)} rows for region {region}")
        
        
        print("\n Preparing data for training...")
        num_columns = dataframe.shape[1]  
        preparer = CustomPreparer(dataframe, num_columns, SHARE_FOR_TRAINING)
        trainX, trainY, testX, testY = preparer.prepare_for_training()
        
        print(f" Training samples: {trainX.shape}")
        print(f" Test samples:{testX.shape}")
        
        if len(trainX) == 0 or len(testX) == 0:
            print(" Insufficient data for training!")
            return {
                'success': False,
                'message': 'Insufficient data for training'
            }
        
        
        print("\n ANN model configuration...")
        ann_regression = AnnRegression()
        
        if hyperparams:
            print(f"Hyperparameters: {hyperparams}")
            ann_regression.set_hyperparameters(hyperparams)
        
    
        print("\n Training a neural network...")
        time_begin = time.time()
        ann_regression.compile_and_fit(trainX, trainY)
        time_end = time.time()
        
        training_time = float(time_end - time_begin)
        print(f"Training time:{training_time:.1f} seconds")
        
        
        print("\n Evaluation of the model...")
        trainPredict, testPredict = ann_regression.get_predict(testX)
        
        trainPredict, trainY_scaled, testPredict, testY_scaled = preparer.inverse_transform(
            trainPredict, testPredict
        )
        
        scorer = Scorer()
        train_rmse, test_rmse = scorer.get_score(trainY_scaled, trainPredict, testY_scaled, testPredict)
        train_mape, test_mape = scorer.get_mape(trainY_scaled, trainPredict, testY_scaled, testPredict)
        
        print(f" RMSE - Train: {train_rmse:.2f}, Test: {test_rmse:.2f}")
        print(f" MAPE - Train: {train_mape:.2f}%, Test: {test_mape:.2f}%")
        
        
        print("\n Saving a model...")
        model_name = f"model_{region}_{start_date}_{end_date}".replace("-", "_")
        model_path = ann_regression.save_model(model_name)
        
        if model_path:
            model_path = str(model_path)
            print(f" Model saved: {model_path}")
        else:
            model_path = f"Services/Models/{model_name}.keras"
            print(f" AnnRegression.save_model() did not return a path")
            print(f" I will save as: {model_path}")
        
        print(f"\n TRAINING COMPLETED FOR THE REGION'{region}'!")
        
        return {
            'success': True,
            'message': f'Training successfully completed for the region {region}',
            'region': region,
            'training_time': training_time,
            'metrics': {
                'train_rmse': train_rmse,
                'test_rmse': test_rmse,
                'train_mape': train_mape,
                'test_mape': test_mape
            },
            'model_path': str(model_path),
            'data_info': {
                'training_samples': int(len(trainX)),
                'test_samples': int(len(testX)),
                'total_samples': int(len(dataframe))
            }
        }
        
    except Exception as e:
        print(f" Region training error {region}: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'success': False,
            'message': f'Region training error {region}: {str(e)}',
            'region': region
        }
    
    
def get_default_hyperparams():

    return {
        'layers': 2,
        'neurons': 64,
        'epochs': 50,
        'batch_size': 32,
        'learning_rate': 0.001,
        'activation': 'relu',
        'optimizer': 'adam'
    }


