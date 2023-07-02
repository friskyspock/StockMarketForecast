import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense, LSTM
from statsmodels.tsa.holtwinters import ExponentialSmoothing

import logging, os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

class EnsembleModel:
  def __init__(self, array, dates, time_steps=80):
    self.scaler = MinMaxScaler()
    self.time_steps = time_steps
    self.model = None
    self.fitted_model = None
    self.len_array = len(array)
    self.end_date = dates[-1]
    self.scaled_array = self.scaler.fit_transform(array.reshape(-1,1))
    x, y = self.process_data(self.scaled_array)
    self.build_model(x,y)

  def process_data(self,data_array):
    y_data = data_array[self.time_steps+1:]
    x_data = np.concatenate([data_array[j:len(data_array)+j-1-self.time_steps] for j in range(self.time_steps+1)],axis=1)
    x_data = x_data.reshape((len(data_array)-self.time_steps-1,self.time_steps+1,1))
    return x_data, y_data

  def build_model(self,x_data,y_data):
    self.model = Sequential([
                      LSTM(64, return_sequences=True, input_shape=(self.time_steps+1,1)),
                      LSTM(32),
                      Dense(1)
                  ])
    self.model.compile(loss='mean_squared_error',optimizer='adam')
    history = self.model.fit(x_data,y_data,epochs=30,batch_size=12,verbose=0)
    hwes_model = ExponentialSmoothing(self.scaled_array, seasonal_periods=52, trend='add', seasonal='add')
    self.fitted_model = hwes_model.fit()

  def predict_future(self,n_steps):
    pred_dates = pd.bdate_range(start=self.end_date,periods=n_steps)
    array = self.scaled_array[-(self.time_steps+2):]
    hwes_array = self.fitted_model.forecast(steps=n_steps)
    pred_stocks = np.empty(n_steps)
    for i in range(n_steps):
      x,y = self.process_data(array)
      y_pred = self.model.predict(x,verbose=0)
      adj = np.sqrt(y_pred*hwes_array[i]) # ensemble
      y_pred_unscaled = self.scaler.inverse_transform(adj.reshape(1,-1))
      pred_stocks[i] = y_pred_unscaled.flatten()
      array = np.append(array,y_pred,axis=0)
      array = array[1:]
    return pred_stocks, pred_dates