from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np
import pandas as pd
from datetime import date, datetime
import pickle
import sys
import os
import tensorflow as tf

np.random.seed(42)
tf.random.set_seed(42)

sys.path.append('../export_to_dataframes')
from export_dataframes import MongoClientDataframes

def get__hr_data():
    '''returns train/ dev/ test datasets for X and y'''

    #get heart rate data from MongoDB
    client = MongoClientDataframes(
        connection_string = "mongodb://localhost:27017/",
        database="local",
        collection="fitbit")
    startTime = date(year = 2023, month =3, day = 28)
    endTime =  date(year = 2023, month = 4, day = 29)
    df = client.dataframe_heart_rate(start_date=startTime)
    
    # Convert the 'date' and 'time' columns to a datetime object and set it as the index
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    df = df.set_index('datetime').drop(columns=['date', 'time'])

    '''Resample the DataFrame to include every minute and 
    fill the missing heart rate values with the previous 
    non-missing value'''
    df = df.resample('1min').ffill()
    data = df.heart_rate.values

    temp, X, y = [], [], []
    # get mean values for each 5 minutes interval
    for i in range(0,len(data),5):
        temp.append(np.mean(data[i:i+5]))
    #each instance contains 12 values (each hour is divided to 12 intervals)
    for i in range(0,len(temp)-12-len(temp)%12,12):
        X.append(temp[i:i+12])
    #the ground truth is the mean value of the next hour
    for i in range(12,len(temp)-len(temp)%12,12):
        y.append(np.mean(temp[i:i+12]))
    X, y= np.array(X), np.array(y)
    X,y = X.reshape(X.shape[0],X.shape[1] , 1),\
        y.reshape(y.shape[0], 1, 1)

    #divine into train/ dev/ test set
    train_set_size = int(0.7*len(X))
    X_train, y_train = X[:train_set_size,:], y[:train_set_size,:]
    X_val, y_val = X[train_set_size:int(0.8*len(X)),:], y[train_set_size:int(0.8*len(X)),:]
    X_test, y_test = X[int(0.8*len(X)):,:], y[int(0.8*len(X)):,:]
    X_list = [X_train, X_val, X_test]
    y_list = [y_train, y_val, y_test]

    return X_list, y_list


def train_model():
    '''trains and saves an LSTM model for predicting next hour heart rate'''

    #get the data
    X, y = get__hr_data()
    X_train, y_train = X[0], y[0]
    X_val, y_val= X[1], y[1]
    X_test, y_test = X[2], y[2]

    #train the model
    model = Sequential()
    model.add(LSTM(64,activation='relu', 
                input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(1))
    model.compile(optimizer='rmsprop', loss='mse')
    model.fit(X_train, y_train, epochs=30, batch_size=32,
            validation_data=(X_val, y_val))
    
    # Save the model to a pickle file
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
    folder_path = os.path.join(parent_dir, 'machine_learning')    
    with open(folder_path+'/lstm_model.p', 'wb') as f:
        pickle.dump(model, f)

    #make predictions
    preds = model.predict(X_test)
    y_test = y_test.reshape(y_test.shape[0],y_test.shape[1])
    r2 = r2_score(y_test, preds)
    mae = mean_absolute_error(y_test, preds)
    print('Mean absolute error and  r2 score are:', mae,r2)



train_model()

