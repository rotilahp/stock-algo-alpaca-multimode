import pandas as pd
import time

twelveApi = '4138a26532c14163a10c81b40f323194'

class myStock:
    outputSize = 10
    smaTimePeriod=[3,8,21]
    
    def __init__(self,ticker,stockInt='1min'):
        self._ticker=ticker
        self._stockInterval = stockInt
        self._dayInv=50
        self._main_inv=50
        self.technical='sma'
        self._df_stock=pd.DataFrame()
        self._buyState = False
        self._sellState = False
        self._dayInvState = False
        self._main_inv_state = False
        self._stopLoss = 0.00
        self._takeProfit = 0.00
        self._currentDate = ''
        self._currentPrice = 0
        self._limit_check=False
        self._limit_side='sell'
        self._limit_check_for_mom=False

    def __dict__(self,item):
        self.item=item
  
    def smaDayTradeBuy(self):
        try:
            df_sma3_price = self._df_stock['sma3']
            df_sma8_price = self._df_stock['sma8']
            df_sma21_price = self._df_stock['sma21']

            #This is a check for recent crosses btwn sma3, sma8, sma21
            cross1 = False
            cross2 = False
            for i, value in enumerate(df_sma3_price[0:6]):
                if df_sma3_price[i] - df_sma8_price[i] < 0.0:
                    cross1 = True
                if df_sma3_price[i] - df_sma21_price[i] < 0.0:
                    cross2 = True

            if df_sma3_price[0] > df_sma21_price[0] and df_sma3_price[0] > df_sma8_price[0]:
                if cross1 and cross2:
                    print('sma says to buy')
                    self._buyState = True

        except Exception as e:
            print(e)
            return

    def smaDayTradeSell(self):
        try:
            df_sma3_price = self._df_stock['sma3']  
            df_sma8_price = self._df_stock['sma8']
            df_sma21_price=self._df_stock['sma21']  
            df_rsi_price=self._df_stock['rsi']

            if df_sma3_price[0] < df_sma21_price[0] or df_sma3_price[0] < df_sma8_price[0]:
                if df_rsi_price[0] < float(50):
                    self._sellState = True
                    print('sma and rsi says to sell')
 
        except Exception as e:
            print(e)
            return

    def simple_ema_buy(self):
        try:
            df_ema3=self._df_stock['ema3']
            df_ema12=self._df_stock['ema12']
            df_ema21=self._df_stock['ema21']
            
            cross1 = False
            cross2 = False
            for i, value in enumerate(df_ema3[0:6]):
                if df_ema3[i] - df_ema12[i] < 0.0:
                    cross1 = True
                if df_ema3[i] - df_ema21[i] < 0.0:
                    cross2 = True

            if df_ema3[0] > df_ema12[0] and df_ema3[0] > df_ema21[0]:
                if cross1 and cross2:
                    print('ema says to buy')
                    self._buyState = True

        except Exception as e:
            print(e)
            return

    def simple_ema_sell(self):
        try:
            df_ema3=self._df_stock['ema3']
            df_ema12=self._df_stock['ema12']
            df_ema21=self._df_stock['ema21']
            df_macD=self._df_stock['macD']
            df_signal = self._df_stock['signal']

            if df_ema3[0] < df_ema12[0] or df_ema3[0] < df_ema21[0]:
                if df_signal[0] > df_macD[0]:
                    print('ema and macd say to sell')
                    self._sellState=True

        except Exception as e:
            print(e)
            return

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
    def main_inv_state(self):
        return self._main_inv_state

    @main_inv_state.setter
    def main_inv_state(self,value):
        if type(value) == bool:
            self._main_inv_state=value
        else:
            print('need a bool fool')

    @property
    def limit_check(self):
        return self._limit_check

    @limit_check.setter
    def limit_check(self,value):
        if type(value) == bool:
            self._limit_check=value
        else:
            print('need a bool fool')

    @property
    def limit_check_for_mom(self):
        return self._limit_check_for_mom

    @limit_check_for_mom.setter
    def limit_check_for_mom(self,value):
        if type(value) == bool:
            self._limit_check_for_mom=value
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
    def main_inv(self):
        return self._main_inv

    @main_inv.setter
    def main_inv(self,value):
        if type(value) == int:
            self._main_inv=value
        else:
            print('need an int fool')   

    @property
    def currentPrice(self):
        return self._currentPrice

    @currentPrice.setter
    def currentPrice(self,value):
        self._currentPrice = value

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
    def limit_side(self):
        return self._limit_side

    @limit_side.setter
    def limit_side(self,value):
        self._limit_side = value

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
