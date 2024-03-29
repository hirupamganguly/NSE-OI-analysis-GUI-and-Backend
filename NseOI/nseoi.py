import string
import requests
import pytz
from pymongo import MongoClient
from datetime import datetime
import json
import time
from datetime import datetime
from pytz import timezone 
import sys
from datetime import date

def determineMarketCloseTime(curTime):
    if date.today().weekday() == 5 or date.today().weekday() == 6: 
        return False
    arr=str.split(str(curTime),":")
    if (int(arr[0])>16 or int(arr[0])<8):
        return False
    else:
        return True

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; '
            'x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
retry=0
try:
    conn = MongoClient("mongodb://localhost:27017/")
    print("Connected successfully!!!")
except:  
    print("Could not connect to MongoDB")

# database
databse = conn["NseOI"]
bankNiftyCollection = databse["BankNifty"]
niftyCollection = databse["Nifty"]
while True:
    main_url = ".."
    try:
        response = requests.get(main_url, headers=headers)
        retry=0
    except:
        retry=retry+1
        if retry<60:
            continue
        else:
            print("RETRY Exceeded: count- ",retry)
            break
    print(response.status_code)
    cookies = response.cookies
    retryCounter=0
    while True:
        bankNiftyUrl = ".."
        try:
            bank_nifty_oi_data = requests.get(bankNiftyUrl, headers=headers, cookies=cookies)
            retryCounter=0
        except:
            retryCounter=retryCounter+1
            if retryCounter<3:
                continue
            else:
                break
        print("BN OI StatusCode",bank_nifty_oi_data.status_code)

        NiftyUrl = ".."
        try:
            nifty_oi_data = requests.get(NiftyUrl, headers=headers, cookies=cookies)
            retryCounter=0
        except:
            retryCounter=retryCounter+1
            if retryCounter<3:
                continue
            else:
                break
        print("Nifty OI StatusCode",nifty_oi_data.status_code)

        IST = pytz.timezone('Asia/Kolkata')
        now = datetime.now(IST)
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
        bankNiftyJson = json.loads(bank_nifty_oi_data.text)
        niftyJson = json.loads(nifty_oi_data.text)
    
        timestamp=datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
        fetchedTime=datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S %Z %z')

        #BankNifty
        if "records" not in bankNiftyJson:
            retryCounter=retryCounter+1
            if retryCounter<3:
                continue
            else:
                break
        bankNiftyfirstStrike=bankNiftyJson["records"]["data"][0]
        bankNiftyUnderlyting=bankNiftyfirstStrike["PE"]["underlyingValue"]
        bankNiftyAtmStrike= round(int(bankNiftyUnderlyting)/100)*100
        
        expiryDates=bankNiftyJson["records"]["expiryDates"]
        time_stamp=bankNiftyJson["records"]["timestamp"]
        expiry_Dates=[]
        expiry_Dates.append(expiryDates[0])
        expiry_Dates.append(expiryDates[1])
        expiry_Dates.append(expiryDates[2])
        bankNiftyObjlist=[]
        
        for data in bankNiftyJson["records"]["data"]:
            strikePrice=data["strikePrice"]
            expiryDate=data["expiryDate"]
            if strikePrice in range(bankNiftyAtmStrike-4000,bankNiftyAtmStrike+4000,100):
                if expiryDate in expiry_Dates:
                    if "PE" not in data:  
                        data["PE"]={}
                        data["PE"]["strikePrice"] = strikePrice
                        data["PE"]["expiryDate"] = expiryDate
                        data["PE"]["underlying"] = data["CE"]["underlying"]
                        data["PE"]["identifier"] = data["CE"]["identifier"]
                        data["PE"]["openInterest"] = 0
                        data["PE"]["changeinOpenInterest"] = 0
                        data["PE"]["pchangeinOpenInterest"] = 0
                        data["PE"]["totalTradedVolume"] = 0
                        data["PE"]["impliedVolatility"] = 0
                        data["PE"]["lastPrice"] = 0
                        data["PE"]["change"] = 0
                        data["PE"]["pChange "]= 0
                        data["PE"]["totalBuyQuantity"] = 0
                        data["PE"]["totalSellQuantity"]= 0
                        data["PE"]["bidQty"] = 0
                        data["PE"]["bidprice"] = 0
                        data["PE"]["askQty"] = 0
                        data["PE"]["askPrice"] = 0
                        data["PE"]["underlyingValue"] = bankNiftyUnderlyting
                    else:
                        if "totalSellQuantity" not in data["PE"]:
                            data["PE"]["totalSellQuantity"]= 0
                        if "totalBuyQuantity" not in data["PE"]:
                            data["PE"]["totalBuyQuantity "]= 0
                        if "openInterest" not in data["PE"]:
                            data["PE"]["openInterest "]= 0
                        if "changeinOpenInterest" not in data["PE"]:
                            data["PE"]["changeinOpenInterest "]= 0
                        if "pchangeinOpenInterest" not in data["PE"]:
                            data["PE"]["pchangeinOpenInterest "]= 0
                        if "totalTradedVolume" not in data["PE"]:
                            data["PE"]["totalTradedVolume "]= 0
                        if "impliedVolatility" not in data["PE"]:
                            data["PE"]["impliedVolatility "]= 0
                        if "lastPrice" not in data["PE"]:
                            data["PE"]["lastPrice "]= 0
                        if "change" not in data["PE"]:
                            data["PE"]["change "]= 0
                        if "pChange" not in data["PE"]:
                            data["PE"]["pChange "]= 0

                    if "CE" not in data:  
                        data["CE"]={}
                        data["CE"]["strikePrice"] = strikePrice
                        data["CE"]["expiryDate"] = expiryDate
                        data["CE"]["underlying"] = data["PE"]["underlying"]
                        data["CE"]["identifier"] = data["PE"]["identifier"]
                        data["CE"]["openInterest"] = 0
                        data["CE"]["changeinOpenInterest"] = 0
                        data["CE"]["pchangeinOpenInterest"] = 0
                        data["CE"]["totalTradedVolume"] = 0
                        data["CE"]["impliedVolatility"] = 0
                        data["CE"]["lastPrice"] = 0
                        data["CE"]["change"] = 0
                        data["CE"]["pChange "]= 0
                        data["CE"]["totalBuyQuantity"] = 0
                        data["CE"]["totalSellQuantity"]= 0
                        data["CE"]["bidQty"] = 0
                        data["CE"]["bidprice"] = 0
                        data["CE"]["askQty"] = 0
                        data["CE"]["askPrice"] = 0
                        data["CE"]["underlyingValue"] = bankNiftyUnderlyting
                    else:
                        if "totalSellQuantity" not in data["CE"]:
                            data["CE"]["totalSellQuantity"]= 0
                        if "totalBuyQuantity" not in data["CE"]:
                            data["CE"]["totalBuyQuantity "]= 0
                        if "openInterest" not in data["CE"]:
                            data["CE"]["openInterest "]= 0
                        if "changeinOpenInterest" not in data["CE"]:
                            data["CE"]["changeinOpenInterest "]= 0
                        if "pchangeinOpenInterest" not in data["CE"]:
                            data["CE"]["pchangeinOpenInterest "]= 0
                        if "totalTradedVolume" not in data["CE"]:
                            data["CE"]["totalTradedVolume "]= 0
                        if "impliedVolatility" not in data["CE"]:
                            data["CE"]["impliedVolatility "]= 0
                        if "lastPrice" not in data["CE"]:
                            data["CE"]["lastPrice "]= 0
                        if "change" not in data["CE"]:
                            data["CE"]["change "]= 0
                        if "pChange" not in data["CE"]:
                            data["CE"]["pChange "]= 0

                    bankNiftyObjmap={"date":timestamp,"nse_timestamp":time_stamp,"strikePrice":data["strikePrice"],"expiryDate":data["expiryDate"],"underlyingValue":data["CE"]["underlyingValue"],"ce_lastPrice":data["CE"]["lastPrice"],"ce_openInterest":data["CE"]["openInterest"],"ce_changeinOpenInterest":data["CE"]["changeinOpenInterest"],"ce_totalTradedVolume":data["CE"]["totalTradedVolume"],"ce_impliedVolatility":data["CE"]["impliedVolatility"],"ce_totalBuyQuantity":data["CE"]["totalBuyQuantity"],"ce_totalSellQuantity":data["CE"]["totalSellQuantity"],"pe_lastPrice":data["PE"]["lastPrice"],"pe_openInterest":data["PE"]["openInterest"],"pe_changeinOpenInterest":data["PE"]["changeinOpenInterest"],"pe_totalTradedVolume":data["PE"]["totalTradedVolume"],"pe_impliedVolatility":data["PE"]["impliedVolatility"],"pe_totalBuyQuantity":data["PE"]["totalBuyQuantity"],"pe_totalSellQuantity":data["PE"]["totalSellQuantity"],"current_expiry":expiryDates[0],"next_expiry":expiryDates[1],"fetched_time":fetchedTime}

                    bankNiftyObjlist.append(bankNiftyObjmap)

        #Nifty
        if "records" not in niftyJson:
            retryCounter=retryCounter+1
            if retryCounter<3:
                continue
            else:
                break
        niftyfirstStrike=niftyJson["records"]["data"][0]
        niftyUnderlyting=niftyfirstStrike["PE"]["underlyingValue"]
        niftyAtmStrike= round(int(niftyUnderlyting)/50)*50
        
        expiryDates=niftyJson["records"]["expiryDates"]
        time_stamp=niftyJson["records"]["timestamp"]
        expiry_Dates=[]
        expiry_Dates.append(expiryDates[0])
        expiry_Dates.append(expiryDates[1])
        expiry_Dates.append(expiryDates[2])
        niftyObjlist=[]
        for data in niftyJson["records"]["data"]:
            strikePrice=data["strikePrice"]
            expiryDate=data["expiryDate"]
            if strikePrice in range(niftyAtmStrike-2000,niftyAtmStrike+2000,50):
                if expiryDate in expiry_Dates:
                    if "PE" not in data:  
                        data["PE"]={}
                        data["PE"]["strikePrice"] = strikePrice
                        data["PE"]["expiryDate"] = expiryDate
                        data["PE"]["underlying"] = data["CE"]["underlying"]
                        data["PE"]["identifier"] = data["CE"]["identifier"]
                        data["PE"]["openInterest"] = 0
                        data["PE"]["changeinOpenInterest"] = 0
                        data["PE"]["pchangeinOpenInterest"] = 0
                        data["PE"]["totalTradedVolume"] = 0
                        data["PE"]["impliedVolatility"] = 0
                        data["PE"]["lastPrice"] = 0
                        data["PE"]["change"] = 0
                        data["PE"]["pChange "]= 0
                        data["PE"]["totalBuyQuantity"] = 0
                        data["PE"]["totalSellQuantity"]= 0
                        data["PE"]["bidQty"] = 0
                        data["PE"]["bidprice"] = 0
                        data["PE"]["askQty"] = 0
                        data["PE"]["askPrice"] = 0
                        data["PE"]["underlyingValue"] = bankNiftyUnderlyting
                    else:
                        if "totalSellQuantity" not in data["PE"]:
                            data["PE"]["totalSellQuantity"]= 0
                        if "totalBuyQuantity" not in data["PE"]:
                            data["PE"]["totalBuyQuantity "]= 0
                        if "openInterest" not in data["PE"]:
                            data["PE"]["openInterest "]= 0
                        if "changeinOpenInterest" not in data["PE"]:
                            data["PE"]["changeinOpenInterest "]= 0
                        if "pchangeinOpenInterest" not in data["PE"]:
                            data["PE"]["pchangeinOpenInterest "]= 0
                        if "totalTradedVolume" not in data["PE"]:
                            data["PE"]["totalTradedVolume "]= 0
                        if "impliedVolatility" not in data["PE"]:
                            data["PE"]["impliedVolatility "]= 0
                        if "lastPrice" not in data["PE"]:
                            data["PE"]["lastPrice "]= 0
                        if "change" not in data["PE"]:
                            data["PE"]["change "]= 0
                        if "pChange" not in data["PE"]:
                            data["PE"]["pChange "]= 0

                    if "CE" not in data:  
                        data["CE"]={}
                        data["CE"]["strikePrice"] = strikePrice
                        data["CE"]["expiryDate"] = expiryDate
                        data["CE"]["underlying"] = data["PE"]["underlying"]
                        data["CE"]["identifier"] = data["PE"]["identifier"]
                        data["CE"]["openInterest"] = 0
                        data["CE"]["changeinOpenInterest"] = 0
                        data["CE"]["pchangeinOpenInterest"] = 0
                        data["CE"]["totalTradedVolume"] = 0
                        data["CE"]["impliedVolatility"] = 0
                        data["CE"]["lastPrice"] = 0
                        data["CE"]["change"] = 0
                        data["CE"]["pChange "]= 0
                        data["CE"]["totalBuyQuantity"] = 0
                        data["CE"]["totalSellQuantity"]= 0
                        data["CE"]["bidQty"] = 0
                        data["CE"]["bidprice"] = 0
                        data["CE"]["askQty"] = 0
                        data["CE"]["askPrice"] = 0
                        data["CE"]["underlyingValue"] = bankNiftyUnderlyting
                    else:
                        if "totalSellQuantity" not in data["CE"]:
                            data["CE"]["totalSellQuantity"]= 0
                        if "totalBuyQuantity" not in data["CE"]:
                            data["CE"]["totalBuyQuantity "]= 0
                        if "openInterest" not in data["CE"]:
                            data["CE"]["openInterest "]= 0
                        if "changeinOpenInterest" not in data["CE"]:
                            data["CE"]["changeinOpenInterest "]= 0
                        if "pchangeinOpenInterest" not in data["CE"]:
                            data["CE"]["pchangeinOpenInterest "]= 0
                        if "totalTradedVolume" not in data["CE"]:
                            data["CE"]["totalTradedVolume "]= 0
                        if "impliedVolatility" not in data["CE"]:
                            data["CE"]["impliedVolatility "]= 0
                        if "lastPrice" not in data["CE"]:
                            data["CE"]["lastPrice "]= 0
                        if "change" not in data["CE"]:
                            data["CE"]["change "]= 0
                        if "pChange" not in data["CE"]:
                            data["CE"]["pChange "]= 0

                    niftyObjmap={"date":timestamp,"nse_timestamp":time_stamp,"strikePrice":data["strikePrice"],"expiryDate":data["expiryDate"],"underlyingValue":data["CE"]["underlyingValue"],"ce_lastPrice":data["CE"]["lastPrice"],"ce_openInterest":data["CE"]["openInterest"],"ce_changeinOpenInterest":data["CE"]["changeinOpenInterest"],"ce_totalTradedVolume":data["CE"]["totalTradedVolume"],"ce_impliedVolatility":data["CE"]["impliedVolatility"],"ce_totalBuyQuantity":data["CE"]["totalBuyQuantity"],"ce_totalSellQuantity":data["CE"]["totalSellQuantity"],"pe_lastPrice":data["PE"]["lastPrice"],"pe_openInterest":data["PE"]["openInterest"],"pe_changeinOpenInterest":data["PE"]["changeinOpenInterest"],"pe_totalTradedVolume":data["PE"]["totalTradedVolume"],"pe_impliedVolatility":data["PE"]["impliedVolatility"],"pe_totalBuyQuantity":data["PE"]["totalBuyQuantity"],"pe_totalSellQuantity":data["PE"]["totalSellQuantity"],"current_expiry":expiryDates[0],"next_expiry":expiryDates[1],"fetched_time":fetchedTime}

                    niftyObjlist.append(niftyObjmap)
                    
        bankNiftyRecordID = bankNiftyCollection.insert_many(bankNiftyObjlist)
        niftyRecordID = niftyCollection.insert_many(niftyObjlist)
        print("timeStamp",fetchedTime," BankNifty ID: ",bankNiftyRecordID," Nifty ID: ",niftyRecordID)
        curTime=datetime.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S')
        isMarketOpen=determineMarketCloseTime(curTime=curTime)
        if not isMarketOpen:
            sys.exit()
        time.sleep(200)
