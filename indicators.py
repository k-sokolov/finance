'''Technical Indicator functions'''

import numpy as np
import scipy as sp
import pandas as pd

def RSI(data, ndays=14):
    '''input: a pandas.Series of Close prices and a period in days(default=14),
    output: a pandas.Series with RSI value per day of data
    '''
    #check_data(data)
    U,D = np.zeros(len(data)), np.zeros(len(data))
    for i in range(1, len(data)):
        a = data.ix[i] - data.ix[i-1]
        if a > 0:
            U[i] = a
        elif a < 0:
            D[i] = ((-1) * a)
        
    U = pd.Series(U, index=data.index)
    D = pd.Series(D, index=data.index)
    RSI = 100 - 100/(1 + (D.rolling(ndays, min_periods=1).sum()/U.rolling(ndays, min_periods=1).sum()))        
    
    return RSI.apply(lambda x: '%.3f' % x)

def SO(Close, Low, High, ndays=14):
    '''input: pandas.Series of Close, Low and High prices, and a period for calculation in days(default=14),
    output: a pandas.Series with Stochastic Oscillator value per day of data, starting from day 14
    '''
    SO  = 100*((Close - Low.rolling(ndays, min_periods=1).min()) /
              (High.rolling(ndays, min_periods=1).max() - Low.rolling(ndays, min_periods=1).min()))
    
    return SO.reindex(Close.index).apply(lambda x: '%.3f' % x)

def Will(Close, Low, High, ndays=14):
    '''input: pandas.Series of Close, Low and High prices, and a period of calculation in days(default=14)
    output: a pandas.Series with Williams %R value per day of data
    '''
    Will  = (-100)*((High.rolling(ndays, min_periods=1).max()- Close) /
              (High.rolling(ndays, min_periods=1).max() - Low.rolling(ndays, min_periods=1).min()))
    
    return Will.apply(lambda x: '%.3f' % x)

def MACD(Close, period1=12, period2=26, periodsignal=9):
    '''input: a pandas.Series of Close prices, a period of 1st EMA(default=12), a period of 2nd EMA(default=26) 
    and a period of Signal Line EMA (default=9)
    output: a pandas.Series with MACD value per day of data
    Values of MACD: -1 = 'sell', 1 = 'buy', else = 'no signal' 
    '''
    #a function to get signals of MACD from the MACD value series.
    def todo(nda):
        if (nda[0]<0) and (nda[2]>0):
            return 1
        elif (nda[0]>0) and (nda[2]<0):
            return -1
        else: return 0
    
    
    MACD = Close.ewm(12).mean() - Close.ewm(26).mean()
    SignalLine = MACD.ewm(9).mean()
    Result = (MACD-SignalLine).rolling(3).apply(todo)
    
    return Result

def PROC(Close, ndays=2):
    '''input: pandas.Series of Close prices, a period of calculation in days(default=2)
    output: pandas.Series with PROC values for each day of input
    '''
    PROC = np.zeros(len(Close))
    for i in range(len(PROC)):
        if i < ndays:
            PROC[i] = (Close[i] - Close[0]) / Close[0]
        else:
            PROC[i] = (Close[i] - Close[i-ndays]) / Close[i-ndays]
            
    PROC = pd.Series(PROC, index = Close.index)
    
    return PROC

def OBV(Close, Vol, ndays=1):
    '''input: pandas.Series of Close prices, pandas.Series of trading volume and a period of calculation
    in days(default=1)
    output: pandas.Series with OBV values for each day of input
    '''
    OBV = np.zeros(len(Vol))
    OBV[0] = Vol[0]
    for i in range(len(OBV)):
        if i < ndays:
            if Close[i] > Close[0]:
                OBV[i] = OBV[0] + Vol[i]
            elif Close[i] < Close[0]:
                OBV[i] = OBV[0] - Vol[i]
            else: 
                OBV[i] = OBV[0]
        else:
            if Close[i] > Close[i-ndays]:
                OBV[i] = OBV[i-ndays] + Vol[i]
            elif Close[i] < Close[i-ndays]:
                OBV[i] = OBV[i-ndays] - Vol[i]
            else: 
                OBV[i] = OBV[i-ndays]
    OBV = pd.Series(OBV, index = Vol.index)  
    
    return OBV