from twelvedata import TDClient
import pandas as pd

td = TDClient(apikey="4138a26532c14163a10c81b40f323194")

def getTwelveData(_symbol,_interval='1min'):
    ts = td.time_series(
        symbol=_symbol,
        interval=_interval,
        outputsize=30,
        timezone="America/Los_Angeles",
    )
    df = ts.without_ohlc().with_sma(time_period=3).with_sma(time_period=8).with_sma(time_period=21).with_rsi().as_pandas()
    return df

def testData(_symbol,_interval='1min'):
    ts = td.time_series(
        symbol=_symbol,
        interval=_interval,
        outputsize=35,
        timezone="America/Los_Angeles",
    )
    df_new = ts.as_pandas()

    valueList =[] 
    for index, value in enumerate(df_new['close']):
        if index < 11:
            valueList.append(df_new['close'][index:3+index].mean())
        else:
            valueList.append('N/A')
    df_new['sma1'] = valueList

    valueList =[]
    for index, value in enumerate(df_new['close']):
        if index < 11:
            valueList.append(df_new['close'][index:8+index].mean())
        else:
            valueList.append('N/A')
    df_new['sma2'] = valueList

    valueList =[]
    for index, value in enumerate(df_new['close']):
        if index < 11:
            valueList.append(df_new['close'][index:21+index].mean())
        else:
            valueList.append('N/A')
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

    return df_new

comment='''
start = time.time()
print(testData('M','1min'))
end=time.time()
print(f'time it took:{end-start}')

'''
