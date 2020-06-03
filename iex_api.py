import requests
import json
import pandas as pd

iex_Api = 'pk_1b20bc084ae24a91a7856630d510f534'
iex_secret_Api = 'sk_ffbe751fad9b4f5f9ff8b4963a8a91b7'
iex_sandbox_Api = 'Tsk_66ee49ffb9734b00959007c66921da54'
iex_url = 'https://sandbox.iexapis.com'

def getIEXData(ticker,indicator,period=5):
    try:
        url = '{}/stable/stock/{}/indicator/{}?range=dynamic&period={}&token={}'.format(
                                    iex_url,ticker,indicator,period,iex_sandbox_Api)    
        response = requests.get(url)
        rsiData = json.loads(response.text)['indicator'] 
        df = pd.DataFrame(rsiData)
        df = df.transpose()
        df = df.rename(columns={0:indicator})
        df = df[df[indicator].notna()]
        df_rev = pd.DataFrame()

        for value in df[indicator].iloc[::-1]:
            df_rev = df_rev.append({indicator:value}, ignore_index=True)

        return df_rev
    except:
        print('api failed')
        pass

#getIEXData('amd','rsi')
#getIEXData('amd','sma')
