import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from keras.models import Sequential
from keras.layers import Dense, LSTM

class StockMarketPrediction:
  def __init__(self,dates,stock_price,verbose=False):
    self.time_steps = 3
    self.len_array = len(stock_price)
    self.stock_price = stock_price
    self.scaler_y = MinMaxScaler()
    self.scaler_x = MinMaxScaler()
    self.verbose = verbose
    self.end_date = dates[-1]

    train, test = self.split_data(self.stock_price)
    dates_train, dates_test = self.split_data(dates)
    dates_train, dates_test = dates_train[self.time_steps+1:-1], dates_test[self.time_steps+1:-1]

    x_train, y_train = self.process_data(train), self.scaler_y.fit_transform(train[self.time_steps+2:].reshape(-1,1))
    self.x_test, self.y_test = self.process_data(test), self.scaler_y.fit_transform(test[self.time_steps+2:].reshape(-1,1))

    self.model = Sequential([LSTM(32, return_sequences=True, input_shape=(4,2)),LSTM(32),Dense(1)])
    self.model.compile(loss='mean_squared_error',optimizer='adam')
    if verbose:
      print(self.model.summary())
    history = self.model.fit(x_train,y_train,epochs=10,batch_size=128)
    self.test_model(self.model)
    
  def test_model(self,model):
    y_pred = model.predict(self.x_test)
    unscaled_y_pred = self.scaler_y.inverse_transform(y_pred)
    unscaled_y_test = self.scaler_y.inverse_transform(self.y_test)
    print('RMSE on test data',mean_squared_error(unscaled_y_test,unscaled_y_pred))

  def split_data(self,array,test_size=0.05):
    n = int(np.round(len(array)*test_size))
    train_data = array[:-n]
    test_data = array[-n:]
    if self.verbose:
      print('train length is',len(train_data),', test length is',len(test_data))
    return train_data, test_data

  def process_data(self,array):
    x_data = np.column_stack((array[:-1], np.diff(array)/array[:-1]))
    x_data = self.scaler_x.fit_transform(x_data)
    bigtable = np.empty((len(array)-self.time_steps-2,self.time_steps+1,2))
    for j in range(self.time_steps+1):
      bigtable[:,j,0] = x_data[:,0][j:len(array)+j-2-self.time_steps]
      bigtable[:,j,1] = x_data[:,1][j:len(array)+j-2-self.time_steps]
    return bigtable

  def predict_future(self,n_steps):
    pred_dates = pd.bdate_range(start=self.end_date,periods=n_steps)
    array = self.stock_price[-(self.time_steps+3):]
    pred_stocks = np.empty(n_steps)
    for i in range(n_steps):
      y_pred = self.model.predict(self.process_data(array))
      y_pred = self.scaler_y.inverse_transform(y_pred)
      pred_stocks[i] = y_pred
      array = np.append(array,y_pred)
      array = array[1:]
    return pred_stocks, pred_dates