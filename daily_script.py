from mystock import myStock
from alpaca_test import (placeDayOrder,placeWeeklyOrder,dayInvStatus,
                        closePositions,marketHoursCheck,
                        getPriceThree, getAlpacaDataLong,calc_macD)
import time
from schedule import is_time_between_int
import pandas as pd
          
stocksList = ['AAL','GNUS','NIO','UAL','DAL','GE','F','SAVE','NCLH','CCL','M',
                'BA','WFC','JBLU','MGM','SIRI','WORK','LUV','OXY','ITUB','VALE',
                'MU','RCL','C','PLUG','EWZ','EBAY','PLAY','TNA','SCHW','ZNGA',
                'PENN','GPS','JETS','FCX','ZM','CLDR','SPG','AMTD','BBBY','NKLA','CRWD',
                'KEY','PE','PK','MAC','RF','SPR','SABR','SQ','FTI','X','JWN',
                'TSLA','BLDP','PLUG','UBER','TRMB','YNDX','AAXN','MRCY','TDY','LMT',
                'AJRD','LHX','MAXR','BWXT','LUV','SKYW','F','ALK','CIDM','AMTD',
                'KZR','ATSG','WMG'
                ]                  
weekList = stocksList
objectList=[]
weekObjList=[]
cashAmount = 300000
df_all_data = pd.DataFrame()

def get_data():
    myString=''
    for stock in stocksList:
        myString+=f'{stock},'
    df_all_data = getAlpacaDataLong(myString)
    #df_all_data=calc_macD(myString)
    return df_all_data

def setup():
    #CREATE STOCK OBJECTS
    for stock in stocksList:
        objectList.append(myStock(stock))

    for stock in weekList:
        weekObjList.append(myStock(stock))

    closePositions()   
    weeklyLoop()

def dayLoop():
    for obj in objectList:
        obj.stockInterval = '5min'
        obj.getData()
        print('now loading: {}'.format(obj.ticker))

        if obj.dayInvState == True:
            print('Sell Check!')
            obj.smaDayTradeSell()
        elif obj.dayInvState == False:
            print('Buy Check!')
            obj.smaDayTradeBuy()

        if obj.buyState == True:
            print('Buying!') 
            currentPrice = getPriceThree(obj.ticker)       
            obj.dayInv = int(cashAmount/(len(weekList))/int(currentPrice))
            placeDayOrder(obj.ticker,obj.dayInv,'buy')
            obj.buyState = False
            obj.dayInvState = True

        if obj.sellState == True:
            print('Selling!') 
            placeDayOrder(obj.ticker,obj.dayInv,'sell')
            obj.sellState = False
            obj.dayInvState = False
        time.sleep(1)

def weeklyLoop():
    df_all_data = get_data()
    for obj in weekObjList:
        obj.stockInterval = 'minute'
        obj.df_stock = df_all_data.loc[obj.ticker]
        print('now loading: {}'.format(obj.ticker))

        if obj.weeklyInvState == True:
            print('Sell Check!')
            obj.smaDayTradeSell()
            #obj.simple_ema_sell()
        elif obj.weeklyInvState == False:
            print('Buy Check!')
            obj.smaDayTradeBuy()
            #obj.simple_ema_buy()

        if obj.buyState == True:
            print('Buying!')      
            currentPrice = getPriceThree(obj.ticker)       
            obj.weeklyInv = int(cashAmount/(len(weekList))/int(currentPrice))
            placeWeeklyOrder(obj.ticker,obj.weeklyInv,'buy')
            placeDayOrder(obj.ticker,obj.weeklyInv,'buy')
            obj.buyState = False
            obj.weeklyInvState = True

        if obj.sellState == True:
            print('Selling!') 
            placeWeeklyOrder(obj.ticker,obj.weeklyInv,'sell')
            placeDayOrder(obj.ticker,obj.weeklyInv,'sell')
            obj.sellState = False
            obj.weeklyInvState = False
        time.sleep(.33)


marketLoop = True
while marketLoop:
    if marketHoursCheck():
        marketLoop=False
    else:
        print('market not open yet')
        time.sleep(30)

setup()
flag = True
previous_sec = time.time()
while flag:
    current_sec = time.time()
    if current_sec-previous_sec > 60:
        previous_sec=time.time()
        weeklyLoop()
    if is_time_between_int(12,58,13,00):
        closePositions()
        time.sleep(1)
        flag = False


