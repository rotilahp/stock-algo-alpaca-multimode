import requests
import json
import pandas as pd
from alpaca_test import getAlpacaData
import time
import numpy as np

twelveApi = '4138a26532c14163a10c81b40f323194'

class myStock:
    outputSize = 10
    smaTimePeriod=[3,8,21]
    
    def __init__(self,ticker,stockInt='1min'):
        self._ticker=ticker
        self._stockInterval = stockInt
        self._dayInv=50
        self._weeklyInv=50
        self.technical='sma'
        self._df_stock=pd.DataFrame()
        self._buyState = False
        self._sellState = False
        self._dayInvState = False
        self._weeklyInvState = False
        self._stopLoss = 0.00
        self._takeProfit = 0.00
        self._currentDate = ''
        self._currentPrice = 0

    def __dict__(self,item):
        self.item=item

    def getData(self):
        try:            
            #self._df_stock = testData(self._ticker,self._stockInterval)
            self._df_stock = getAlpacaData(self._ticker)
        except:
            print('data didnt load')
            pass

    def smaDayTradeBuy(self):
        try:
            df_sma3_price = self._df_stock['sma1']
            df_sma8_price = self._df_stock['sma2']
            df_sma21_price = self._df_stock['sma3']

            #This is a check for recent crosses btwn sma3, sma8, sma21
            cross1 = False
            cross2 = False
            for i, value in enumerate(df_sma3_price[0:8]):
                if df_sma3_price[i] - df_sma8_price[i] < 0.0:
                    cross1 = True
                if df_sma3_price[i] - df_sma21_price[i] < 0.0:
                    cross2 = True

            print('cross1:{} cross2:{}'.format(cross1,cross2))
            print('if {} > {} and {} > {}'.format(df_sma3_price[0],df_sma21_price[0],df_sma3_price[0],df_sma8_price[0]))
            if df_sma3_price[0] > df_sma21_price[0] and df_sma3_price[0] > df_sma8_price[0]:
                if cross1 and cross2:
                    self._buyState = True
        except:
            print('missing a list')
            self.getData()
            pass
    def smaDayTradeSell(self):
        try:
            df_sma3_price = self._df_stock['sma1']  
            df_sma8_price = self._df_stock['sma2']
            df_sma21_price=self._df_stock['sma3']  
            df_rsi_price=self._df_stock['rsi']

            if df_sma3_price[0] < df_sma21_price[0] or df_sma3_price[0] < df_sma8_price[0]:
                print('sma says to sell')

                if df_rsi_price[0] < float(50):
                    self._sellState = True
                    print('rsi says to sell')
 
        except:
            print('missing a list')
            self.getData()
            pass

    @property
    def buyState(self):
        return self._buyState

    @buyState.setter
    def buyState(self,value):
        if type(value) == bool:
            self._buyState=value
        else:
            print('need a bool fool')

    @property
    def sellState(self):
        return self._sellState

    @sellState.setter
    def sellState(self,value):
        if type(value) == bool:
            self._sellState=value
        else:
            print('need a bool fool')

    @property
    def dayInvState(self):
        return self._dayInvState

    @dayInvState.setter
    def dayInvState(self,value):
        if type(value) == bool:
            self._dayInvState=value
        else:
            print('need a bool fool')

    @property
    def weeklyInvState(self):
        return self._weeklyInvState

    @weeklyInvState.setter
    def weeklyInvState(self,value):
        if type(value) == bool:
            self._weeklyInvState=value
        else:
            print('need a bool fool')

    @property
    def dayInv(self):
        return self._dayInv

    @dayInv.setter
    def dayInv(self,value):
        if type(value) == int:
            self._dayInv=value
        else:
            print('need an int fool')

    @property
    def weeklyInv(self):
        return self._weeklyInv

    @weeklyInv.setter
    def weeklyInv(self,value):
        if type(value) == int:
            self._weeklyInv=value
        else:
            print('need an int fool')

    @property
    def stopLoss(self):
        return self._stopLoss

    @stopLoss.setter
    def stopLoss(self,value):
        if type(value) == float:
            self._stopLoss=value
        else:
            print('need an float fool')

    @property
    def takeProfit(self):
        return self._takeProfit

    @takeProfit.setter
    def takeProfit(self,value):
        if type(value) == float:
            self._takeProfit=value
        else:
            print('need an float fool')        

    @property
    def currentPrice(self):
        return self._currentPrice

    @currentPrice.setter
    def currentPrice(self,value):
        self._currentPrice = getPrice(self)

    @property
    def currentDate(self):
        return self._currentDate 

    @property
    def weeklyCounter(self):
        return self._weeklyCounter

    @weeklyCounter.setter
    def weeklyCounter(self,value):
        self._weeklyCounter = value

    @property
    def stockInterval(self):
        return self._stockInterval

    @stockInterval.setter
    def stockInterval(self,value):   
        self._stockInterval=value
        
    @property
    def df_stock(self):
        return self._df_stock

    @df_stock.setter
    def df_stock(self,value):   
        self._df_stock=value

    @property
    def ticker(self):
        return self._ticker

comment = '''
stock1 = myStock('AMD')
stock1.getData()
stock1.smaDayTradeSell()
time.sleep(1)
'''
