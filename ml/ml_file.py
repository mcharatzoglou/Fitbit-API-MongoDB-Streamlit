from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np
import pandas as pd
from datetime import date, datetime
import sys
sys.path.append('../export_to_dataframes')
from export_dataframes import MongoClientDataframes

#get data from MongoDB
client = MongoClientDataframes(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit")
startTime = date(year = 2023, month =3, day = 27)
endTime =  date(year = 2023, month = 4, day = 27)
df = client.dataframe_heart_rate(start_date=startTime)
df = df.dropna()
df = df[(df ["heart_rate"]!= 0)]

data = df.heart_rate.values
X, y = [], []
for i in range(len(data)-13):
    X.append(data[i:i+6])
    y.append(data[i+6:i+12])
X,y = np.array(X), np.array(y)
X,y = X.reshape(X.shape[0],X.shape[1] , 1),\
    y.reshape(y.shape[0],y.shape[1] , 1)

train_set_size = int(0.7*len(X))
X_train, y_train = X[:train_set_size,:], y[:train_set_size,:]
X_val, y_val = X[train_set_size:int(0.8*len(X)),:], y[train_set_size:int(0.8*len(X)),:]
X_test, y_test = X[int(0.8*len(X)):,:], y[int(0.8*len(X)):,:]
print(X_test.shape, y_test.shape)

#train LSTM model
model = Sequential()
model.add(LSTM(32,activation='relu', input_shape=(X.shape[1], X.shape[2])))
model.add(Dense(6))

model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=50, batch_size=32,
           validation_data=(X_val, y_val))

preds = model.predict(X_test)
print(preds.shape)
y_test = y_test.reshape(y_test.shape[0],y_test.shape[1])
print(y_test.shape)
r2 = mean_absolute_error(y_test, preds)
print(r2)