apiKey = 'PKXCR7JS2MLM2OX8OZQJ'
secretKey = 'svwF29CXjP3l3TY8VLelx6KbPmTt08HnRFmG1JsB'
endpoint = 'https://paper-api.alpaca.markets'

import alpaca_trade_api as tradeapi
import pandas as pd
import time

api_day = tradeapi.REST(
        apiKey,
        secretKey,
        endpoint
    )
comment = '''
api_weekly = tradeapi.REST(
        'PKXCR7JS2MLM2OX8OZQJ',
        'svwF29CXjP3l3TY8VLelx6KbPmTt08HnRFmG1JsB',
        endpoint
    )
'''
api_weekly = api_day
def placeDayOrder(ticker,inv, _side):
    try:
        final=(1000.00/float(inv))+getPriceThree(ticker)
        loss=(-300.00/float(inv))+getPriceThree(ticker)
        print(final)
        api_day.submit_order(
            symbol=ticker,
            qty=inv,
            side=_side,
            type='market',
            time_in_force='day',
            #order_class='bracket',
            #take_profit={'limit_price':final},
            #stop_loss={'stop_price':loss}
        )
    except:
        print('failed to place order')
        pass

def placeWeeklyOrder(ticker,inv, _side):
    try:
        if _side == 'buy':
            #final=(1000.00/float(inv))+getPriceThree(ticker)
            #loss=(-300.00/float(inv))+getPriceThree(ticker)
            api_weekly.submit_order(
                symbol=ticker,
                qty=inv,
                side=_side,
                type='market',
                time_in_force='day',
                #order_class='bracket',
                #take_profit={'limit_price':final},
                #stop_loss={'stop_price':loss}
            )
        elif _side == 'sell':
            api_weekly.close_position(ticker)
            
    except:
        print('failed to place order')
        #api_weekly.submit_order(
        #        symbol=ticker,
        #        qty=inv,
        #        side=_side,
        #        type='market',
       #         time_in_force='gtc',
        #    )
        pass


def dayInvStatus(obj):
    try:
        position = api_day.get_position(obj.ticker)
        return True
    except:
        #return False
        return False

def dayInv(obj):
    try:
        position = api_day.get_position(obj.ticker)
        return position
    except:
        print('no inventory')
        return 50

def weeklyInvStatus(obj):
    try:
        position = api_weekly.get_position(obj.ticker)
        return True
    except:
        #return False
        return False

def weeklyInv(obj):
    try:
        position = api_weekly.get_position(obj.ticker)
        return position
    except:
        print('no inventory')
        return 50

def marketHoursCheck():
    clock = api_day.get_clock()
    return True if clock.is_open else False

def getPriceThree(ticker):
    barset = api_weekly.get_barset(ticker,'minute',limit=1).df.iloc[0]
    bars = barset[ticker]['close']
    return float(bars)

def getAlpacaData(ticker,interval='minute'):
    try:
        barset = api_weekly.get_barset(ticker,interval,limit=35)
        bars = barset[ticker]
        barList = []
        for index in range(35):
            x=34-index
            barList.append(bars[x].c)

        df_new = pd.DataFrame()
        df_new['close'] = barList
        
        valueList =[] 
        for index, value in enumerate(df_new['close']):
            if index < 11:
                valueList.append(df_new['close'][index:3+index].mean())
            else:
                valueList.append('NaN')
        df_new['sma1'] = valueList

        valueList =[]
        for index, value in enumerate(df_new['close']):
            if index < 11:
                valueList.append(df_new['close'][index:8+index].mean())
            else:
                valueList.append('NaN')
        df_new['sma2'] = valueList

        valueList =[]
        for index, value in enumerate(df_new['close']):
            if index < 11:
                valueList.append(df_new['close'][index:21+index].mean())
            else:
                valueList.append('NaN')
        df_new['sma3'] = valueList 

        upList = []
        downList = []
        rsiPeriod = 14
        for index, value in enumerate(df_new['close']):
            if index <34:
                change = df_new['close'][index]-df_new['close'][index+1]
                if change > 0:
                    upList.append(change)
                    downList.append(0.00)
                elif change < 0:
                    downList.append(abs(change))
                    upList.append(0.00)
                else:
                    upList.append(0.00)
                    downList.append(0.00)
            else:
                upList.append('N/A')
                downList.append('N/A')

        df_new['up']=upList
        df_new['down']=downList

        avgU=[]
        avgD=[]
        for index, value in enumerate(df_new['close']):
            if index <= len(df_new['close'])-15:
                avgU.append(df_new['up'][index:(index+rsiPeriod)].mean())
                avgD.append(df_new['down'][index:(index+rsiPeriod)].mean())
            else:
                avgU.append('NaN')
                avgD.append('NaN')
        
        df_new['avgU']=avgU
        df_new['avgD']=avgD

        rs=[]
        rsi=[]
        for index, value in enumerate(df_new['close']):
            if index <= rsiPeriod:
                rs.append(df_new['avgU'][index]/df_new['avgD'][index])
                rsi.append(100.0-100.0/(1.0+rs[index]))
            else:
                rs.append('NaN')
                rsi.append('NaN')

        df_new['rs']=rs
        df_new['rsi']=rsi
    except:
        print('failed to pull data from alpaca')
        
    return df_new


def getAlpacaDataLong(ticker,interval='minute'):
    try:
        barset = api_weekly.get_barset(ticker,interval,limit=35)
        df_all = pd.DataFrame()
        infoList=[]
        keyList=[]

        for bar in barset:
            bars=barset[bar]

            barList = []
            for index in range(35):
                x=34-index
                barList.append(bars[x].c)

            df_new = pd.DataFrame()
            df_new['close'] = barList
            
            valueList =[] 
            for index, value in enumerate(df_new['close']):
                if index < 11:
                    valueList.append(df_new['close'][index:3+index].mean())
                else:
                    valueList.append('NaN')
            df_new['sma1'] = valueList

            valueList =[]
            for index, value in enumerate(df_new['close']):
                if index < 11:
                    valueList.append(df_new['close'][index:8+index].mean())
                else:
                    valueList.append('NaN')
            df_new['sma2'] = valueList

            valueList =[]
            for index, value in enumerate(df_new['close']):
                if index < 11:
                    valueList.append(df_new['close'][index:21+index].mean())
                else:
                    valueList.append('NaN')
            df_new['sma3'] = valueList 

            upList = []
            downList = []
            rsiPeriod = 14
            for index, value in enumerate(df_new['close']):
                if index <34:
                    change = df_new['close'][index]-df_new['close'][index+1]
                    if change > 0:
                        upList.append(change)
                        downList.append(0.00)
                    elif change < 0:
                        downList.append(abs(change))
                        upList.append(0.00)
                    else:
                        upList.append(0.00)
                        downList.append(0.00)
                else:
                    upList.append('N/A')
                    downList.append('N/A')

            df_new['up']=upList
            df_new['down']=downList

            avgU=[]
            avgD=[]
            for index, value in enumerate(df_new['close']):
                if index <= len(df_new['close'])-15:
                    avgU.append(df_new['up'][index:(index+rsiPeriod)].mean())
                    avgD.append(df_new['down'][index:(index+rsiPeriod)].mean())
                else:
                    avgU.append('NaN')
                    avgD.append('NaN')
            
            df_new['avgU']=avgU
            df_new['avgD']=avgD

            rs=[]
            rsi=[]
            for index, value in enumerate(df_new['close']):
                if index <= rsiPeriod:
                    rs.append(df_new['avgU'][index]/df_new['avgD'][index])
                    rsi.append(100.0-100.0/(1.0+rs[index]))
                else:
                    rs.append('NaN')
                    rsi.append('NaN')

            df_new['rs']=rs
            df_new['rsi']=rsi
            infoList.append(df_new)
            keyList.append(bar)
        df_all = pd.concat(infoList,keys=keyList, axis=0)
        return df_all
    except:
        print('failed to pull data from alpaca')

def closePositions():
    try:
        api_day.close_all_positions()
        api_day.cancel_all_orders()
        api_weekly.close_all_positions()
        api_weekly.cancel_all_orders()
    except:
        print('no positions to close or error')

def check_assets(mylist):
    for item in mylist:
        asset = api_weekly.get_asset(item)
        if not asset.tradable:
            print(f'{item} is not covered!')
            mylist.remove(item)
    return mylist






