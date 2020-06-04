from mystock import myStock
from alpaca_test import (placeDayOrder,placeWeeklyOrder,dayInvStatus,
                        dayInv,weeklyInvStatus,closePositions,weeklyInv,
                        marketHoursCheck,getPriceThree, getAlpacaDataLong,
                        calc_macD)
import time
from schedule import is_time_between_int
import pandas as pd
          
stocksList = [  'FSLY','ZS','ZM','WIX','TWLO','DOCU','DDOG','OKTA',               #cloud computing----------------------------
                'CRWD','FIVN','NET','VEEV','QLYS',
                'WDAY','PAYC','PCTY','PLAN','AKAM','CRM',                        #global x cloud etf
                'TSLA','SQ','ROKU','TWOU','Z','SPLK','TREE','PINS',               #Ark Web ETF 
                'EVBG','COUP','SHOP',                                             
                'USAC','NS','CEQP','DKL','DCP','CAPL','WLKP','HESM',              #high income -------------------------------
                'MMP','PAA','HEP','BPMP','EPD','WES','KNOP',
                'FNGO',                                                           #FANG 2x leverage
                'CRSP','ILMN','NVTA','CGEN','ARCT','NTLA',                        #biotech stocks--------------------------
                'IOVA','EDIT','CLLS','CDNA','TWST','PRLB',                                
                'REGN','EXEL','SRPT','SGEN','GMAB',                               #immunology and healthcare etf
                'SFIX','W','GRUB','STMP','RVLV','TRIP','BABA',                    #online retail stocks------------------------------------
                'EXPE','BKNG','REAL','FLWS','ETSY','EBAY','QRTEA',
                'SSTK','CHWY','FLWS','GRPN','QUOT','MELI', 
                'SE','ATVI','EA','NTES','ZNGA',                                   #video games 
                'PCG','WEBL','VTIQ']                                              #regular shit
weekList = stocksList
objectList=[]
weekObjList=[]
cashAmount = 300000
df_all_data = pd.DataFrame()

def stopAndTakeCheck(obj):
    currentPrice = getPriceThree(obj.ticker)
    if currentPrice < obj.stopLoss:
        obj.sellState = True
    if currentPrice > obj.takeProfit:
        obj.sellState = True

def get_data():
    myString=''
    for stock in stocksList:
        myString+=f'{stock},'
    #df_all_data = getAlpacaDataLong(myString)
    df_all_data=calc_macD(myString)
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
            #stopAndTakeCheck(obj)
            #obj.smaDayTradeSell()
            obj.simple_ema_sell()
        elif obj.weeklyInvState == False:
            print('Buy Check!')
            #obj.smaDayTradeBuy()
            obj.simple_ema_buy()

        if obj.buyState == True:
            print('Buying!')      
            currentPrice = getPriceThree(obj.ticker)       
            obj.weeklyInv = int(cashAmount/(len(weekList))/int(currentPrice))
            #obj.stopLoss = currentPrice * 0.985
            #obj.takeProfit = currentPrice * 1.03
            placeWeeklyOrder(obj.ticker,obj.weeklyInv,'buy')
            obj.buyState = False
            obj.weeklyInvState = True

        if obj.sellState == True:
            print('Selling!') 
            placeWeeklyOrder(obj.ticker,obj.weeklyInv,'sell')
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


