from mystock import myStock
from alpaca_test import (place_second_order,place_main_order,
                        closePositions,marketHoursCheck,
                        getPriceThree,sma_and_rsi_data,calc_macD)
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
                'KZR','ATSG','WMG']                                  

main_obj_list=[]
cashAmount = 300000
df_all_data = pd.DataFrame()

def get_data():
    myString=''
    for stock in stocksList:
        myString+=f'{stock},'
    df_all_data = sma_and_rsi_data(myString)
    #df_all_data=calc_macD(myString)
    return df_all_data

def setup():
    #CREATE STOCK OBJECTS
    for stock in stocksList:
        main_obj_list.append(myStock(stock))

    closePositions()   
    stock_loop_one()

def stock_loop_one():
    df_all_data = get_data()
    for obj in main_obj_list:
        obj.stockInterval = 'minute'
        obj.df_stock = df_all_data.loc[obj.ticker]
        print('now loading: {}'.format(obj.ticker))

        if obj.main_inv_state == True:
            print('Sell Check!')
            obj.smaDayTradeSell()
            #obj.simple_ema_sell()
        elif obj.main_inv_state == False:
            print('Buy Check!')
            obj.smaDayTradeBuy()
            #obj.simple_ema_buy()

        if obj.buyState == True:
            print('Buying!')      
            currentPrice = getPriceThree(obj.ticker)       
            obj.main_inv = cashAmount/(len(stocksList))/int(currentPrice)
            place_main_order(obj.ticker,obj.main_inv,'buy')
            place_second_order(obj.ticker,obj.main_inv,'buy')
            obj.buyState = False
            obj.main_inv_state = True

        if obj.sellState == True:
            print('Selling!') 
            place_main_order(obj.ticker,obj.main_inv,'sell')
            place_second_order(obj.ticker,obj.main_inv,'sell')
            obj.sellState = False
            obj.main_inv_state = False
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
        stock_loop_one()
    if is_time_between_int(12,58,13,00):
        closePositions()
        time.sleep(1)
        flag = False


