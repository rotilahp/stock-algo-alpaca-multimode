apiKey = 'PKUEUNNM9IGYK7KPVC57'
secretKey = '6sfPaWM8SiBc9JPLEcKvlvqXEcDmYTjP/YLl05k9'
endpoint = 'https://paper-api.alpaca.markets'

import alpaca_trade_api as tradeapi
import pandas as pd
import time

api_for_daniel = tradeapi.REST(
        apiKey,
        secretKey,
        endpoint
    )

api_for_mom = tradeapi.REST(
        'PK2B9YFVI6LVO5YP12G3',
        'h8aB36QHred2OgLiYp4Wn0EVz4BTCGwCxesmmWXe',
        endpoint
    )

def get_last_trade(ticker):
    info = api_for_daniel.get_last_trade(ticker)
    return float(info.price)

def placeDayOrder(ticker,inv, _side):
    try:
        if _side == 'buy':
            current_price = get_last_trade(ticker)
            loss=current_price*.9995
            api_for_mom.submit_order(
                symbol=ticker,
                qty=inv,
                side=_side,
                type='limit',
                time_in_force='day',
                limit_price=current_price*1.0005,
                order_class='oto',
                stop_loss={'stop_price':loss}
            )
            
        elif _side == 'sell':
            #check for positions
            #check for orders
            order = [o for o in api_for_mom.list_orders() if o.symbol == ticker]
            position = [p for p in api_for_mom.list_positions()
                        if p.symbol == ticker]

            if position is not None:
                if order is None:
                    current_price = get_last_trade(ticker)
                    order = api_for_mom.submit_order(
                        symbol=ticker,
                        qty=inv,
                        side=_side,
                        type='limit',
                        time_in_force='day',
                        limit_price=current_price*0.9995,
                    )
                else:
                    #cancel sell order first
                    api_for_mom.cancel_order(order[0].id)
                    current_price = get_last_trade(ticker)
                    api_for_mom.submit_order(
                        symbol=ticker,
                        qty=inv,
                        side=_side,
                        type='limit',
                        time_in_force='day',
                        limit_price=current_price*0.9995,
                    )
            
    except Exception as e:
        print(e)
        print('failed to place order')
        return



def placeWeeklyOrder(ticker,inv, _side):
    try:
        if _side == 'buy':
            current_price = get_last_trade(ticker)
            loss=current_price*.9995
            api_for_daniel.submit_order(
                symbol=ticker,
                qty=inv,
                side=_side,
                type='limit',
                time_in_force='day',
                limit_price=current_price*1.0005,
                order_class='oto',
                stop_loss={'stop_price':loss}
            )
            
        elif _side == 'sell':
            #check for positions
            #check for orders
            order = [o for o in api_for_daniel.list_orders() if o.symbol == ticker]
            position = [p for p in api_for_daniel.list_positions()
                        if p.symbol == ticker]

            if position is not None:
                if order is None:
                    current_price = get_last_trade(ticker)
                    order = api_for_daniel.submit_order(
                        symbol=ticker,
                        qty=inv,
                        side=_side,
                        type='limit',
                        time_in_force='day',
                        limit_price=current_price*0.9995,
                    )
                else:
                    #cancel sell order first
                    api_for_daniel.cancel_order(order[0].id)
                    current_price = get_last_trade(ticker)
                    api_for_daniel.submit_order(
                        symbol=ticker,
                        qty=inv,
                        side=_side,
                        type='limit',
                        time_in_force='day',
                        limit_price=current_price*0.9995,
                    )
            
    except Exception as e:
        print(e)
        print('failed to place order')
        return

#placeWeeklyOrder('AMD',55,'buy')

def orderUpdate():
    return None

def dayInvStatus(obj):
    try:
        position = api_for_mom.get_position(obj.ticker)
        return True
    except:
        #return False
        return False

def dayInv(obj):
    try:
        position = api_for_mom.get_position(obj.ticker)
        return position
    except:
        print('no inventory')
        return 50

def weeklyInvStatus(obj):
    try:
        position = api_for_daniel.get_position(obj.ticker)
        return True
    except:
        #return False
        return False

def get_position(obj):
    try:
        position = api_for_daniel.get_position(obj.ticker)
        return position
    except:
        print('no inventory')
        return 0

def marketHoursCheck():
    clock = api_for_daniel.get_clock()
    return True if clock.is_open else False

def getPriceThree(ticker):
    barset = api_for_daniel.get_barset(ticker,'minute',limit=1).df.iloc[0]
    bars = barset[ticker]['close']
    return float(bars)



#print(get_last_trade('AMD'))

def get_ask_price(ticker):
    barset = api_for_daniel.get_barset(ticker,'minute',limit=1).df.iloc[0]
    bars = barset[ticker]['close']
    return float(bars)

def get_bid_price(ticker):
    barset = api_for_daniel.get_barset(ticker,'minute',limit=1).df.iloc[0]
    bars = barset[ticker]['close']
    return float(bars)

def getAlpacaData(ticker,interval='minute'):
    try:
        barset = api_for_mom.get_barset(ticker,interval,limit=35)
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
        barset = api_for_daniel.get_barset(ticker,interval,limit=35)
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
            df_new['sma3'] = valueList

            valueList =[]
            for index, value in enumerate(df_new['close']):
                if index < 11:
                    valueList.append(df_new['close'][index:8+index].mean())
                else:
                    valueList.append('NaN')
            df_new['sma8'] = valueList

            valueList =[]
            for index, value in enumerate(df_new['close']):
                if index < 11:
                    valueList.append(df_new['close'][index:21+index].mean())
                else:
                    valueList.append('NaN')
            df_new['sma21'] = valueList 

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

def calc_macD(ticker,interval='minute'):
    barset = api_for_daniel.get_barset(ticker,interval,limit=55)
    df_all = pd.DataFrame()
    infoList=[]
    keyList=[]

    for bar in barset:
        bars=barset[bar]

        #closing in ascending order
        closing_list=[]
        for i in range(55):
            closing_list.append(bars[i].c)
        closing=pd.Series(closing_list)

        #ema3 in ascending order
        span=3
        sma=closing.rolling(window=span,min_periods=span).mean()[:span]
        rest=closing[span:]
        ema3 = pd.concat([sma,rest]).ewm(span=span,adjust=False).mean()

        #ema12 in ascending order
        span=12
        sma=closing.rolling(window=span,min_periods=span).mean()[:span]
        rest=closing[span:]
        ema12 = pd.concat([sma,rest]).ewm(span=span,adjust=False).mean()

        #ema21 in ascending order
        span=21
        sma=closing.rolling(window=span,min_periods=span).mean()[:span]
        rest=closing[span:]
        ema21 = pd.concat([sma,rest]).ewm(span=span,adjust=False).mean()

        #ema26 in ascending order
        span=26
        sma=closing.rolling(window=span,min_periods=span).mean()[:span]
        rest=closing[span:]
        ema26 = pd.concat([sma,rest]).ewm(span=span,adjust=False).mean()

        #macD in ascending order
        macD_list=[]
        for i in range(55):
            macD_list.append(ema12[i]-ema26[i])
        macD=pd.Series(macD_list)

        #signal in ascending order
        span=9
        sma=macD.rolling(window=span,min_periods=span).mean()[:span]
        rest=macD[span:]
        signal = pd.concat([sma,rest]).ewm(span=span,adjust=False).mean()

        #closing in descending order
        close_list=[]
        for i in range(55):
            x=54-i
            close_list.append(closing[x])
        df_closing=pd.Series(close_list)

        #macD in descending order
        macD_list=[]
        for i in range(55):
            x=54-i
            macD_list.append(macD[x])
        df_macD=pd.Series(macD_list)

        #signal in descending order
        signal_list=[]
        for i in range(55):
            x=54-i
            signal_list.append(signal[x])
        df_signal=pd.Series(signal_list)

        #ema in descending order
        revEma=[]
        for i in range(55):
            x=54-i
            revEma.append(ema3[x])
        df_ema3=pd.Series(revEma)

        #ema in descending order
        revEma=[]
        for i in range(55):
            x=54-i
            revEma.append(ema12[x])
        df_ema12=pd.Series(revEma)

        #ema in descending order
        revEma=[]
        for i in range(55):
            x=54-i
            revEma.append(ema21[x])
        df_ema21=pd.Series(revEma)

        comment='''
        #ema in descending order
        revEma=[]
        for i in range(55):
            x=54-i
            revEma.append(ema26[x])
        df_ema26=pd.Series(revEma)
        '''
        
        df_stock=pd.DataFrame({'close':df_closing,'ema3':df_ema3,'ema12':df_ema12,
                                'ema21':df_ema21,'macD':df_macD,'signal':df_signal})
        infoList.append(df_stock)
        keyList.append(bar)
    df_all=pd.concat(infoList,keys=keyList, axis=0)
    return df_all

def closePositions():
    try:
        api_for_mom.cancel_all_orders()
        api_for_daniel.cancel_all_orders()
        api_for_mom.close_all_positions()
        api_for_daniel.close_all_positions()
    except Exception as e:
        print(e)
        print('no positions to close or error')
        return

def check_assets(mylist):
    for item in mylist:
        asset = api_for_daniel.get_asset(item)
        if not asset.tradable:
            print(f'{item} is not covered!')
            mylist.remove(item)
    return mylist

def _cancel_order(_order):
    if _order is not None:
            api_for_daniel.cancel_order(_order.id)

