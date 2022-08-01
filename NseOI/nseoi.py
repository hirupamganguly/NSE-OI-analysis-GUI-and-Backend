import requests
import pytz
from pymongo import MongoClient
from datetime import datetime
import json
import time
from pytz import timezone 

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; '
            'x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

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
    main_url = "https://www.nseindia.com/"
    response = requests.get(main_url, headers=headers)
    print(response.status_code)
    cookies = response.cookies

    bankNiftyUrl = "https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"
    bank_nifty_oi_data = requests.get(bankNiftyUrl, headers=headers, cookies=cookies)
    print("BN OI StatusCode",bank_nifty_oi_data.status_code)

    NiftyUrl = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    nifty_oi_data = requests.get(NiftyUrl, headers=headers, cookies=cookies)
    print("Nifty OI StatusCode",nifty_oi_data.status_code)

    IST = pytz.timezone('Asia/Kolkata')
    now = datetime.now(IST)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
   
    bankNiftyJson = json.loads(bank_nifty_oi_data.text)
    niftyJson = json.loads(nifty_oi_data.text)
   
    timestamp=datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
    fetchedTime=datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S %Z %z')

    #BankNifty
    bankNiftyfirstStrike=bankNiftyJson["records"]["data"][30]
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
        if strikePrice in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100):
            if expiryDate in expiry_Dates:
                bankNiftyObjmap={"date":timestamp,"nse_timestamp":time_stamp,"strikePrice":data["strikePrice"],"expiryDate":data["expiryDate"],"underlyingValue":data["CE"]["underlyingValue"],"ce_lastPrice":data["CE"]["lastPrice"],"ce_openInterest":data["CE"]["openInterest"],"ce_changeinOpenInterest":data["CE"]["changeinOpenInterest"],"ce_totalTradedVolume":data["CE"]["totalTradedVolume"],"ce_impliedVolatility":data["CE"]["impliedVolatility"],"ce_totalBuyQuantity":data["CE"]["totalBuyQuantity"],"ce_totalSellQuantity":data["CE"]["totalSellQuantity"],"pe_lastPrice":data["PE"]["lastPrice"],"pe_openInterest":data["PE"]["openInterest"],"pe_changeinOpenInterest":data["PE"]["changeinOpenInterest"],"pe_totalTradedVolume":data["PE"]["totalTradedVolume"],"pe_impliedVolatility":data["PE"]["impliedVolatility"],"pe_totalBuyQuantity":data["PE"]["totalBuyQuantity"],"pe_totalSellQuantity":data["PE"]["totalSellQuantity"],"current_expiry":expiryDates[0],"next_expiry":expiryDates[1],"fetched_time":fetchedTime}
                bankNiftyObjlist.append(bankNiftyObjmap)

    #Nifty
    niftyfirstStrike=niftyJson["records"]["data"][20]
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
        if strikePrice in range(niftyAtmStrike-300,niftyAtmStrike+300,50):
            if expiryDate in expiry_Dates:
                niftyObjmap={"date":timestamp,"nse_timestamp":time_stamp,"strikePrice":data["strikePrice"],"expiryDate":data["expiryDate"],"underlyingValue":data["CE"]["underlyingValue"],"ce_lastPrice":data["CE"]["lastPrice"],"ce_openInterest":data["CE"]["openInterest"],"ce_changeinOpenInterest":data["CE"]["changeinOpenInterest"],"ce_totalTradedVolume":data["CE"]["totalTradedVolume"],"ce_impliedVolatility":data["CE"]["impliedVolatility"],"ce_totalBuyQuantity":data["CE"]["totalBuyQuantity"],"ce_totalSellQuantity":data["CE"]["totalSellQuantity"],"pe_lastPrice":data["PE"]["lastPrice"],"pe_openInterest":data["PE"]["openInterest"],"pe_changeinOpenInterest":data["PE"]["changeinOpenInterest"],"pe_totalTradedVolume":data["PE"]["totalTradedVolume"],"pe_impliedVolatility":data["PE"]["impliedVolatility"],"pe_totalBuyQuantity":data["PE"]["totalBuyQuantity"],"pe_totalSellQuantity":data["PE"]["totalSellQuantity"],"current_expiry":expiryDates[0],"next_expiry":expiryDates[1],"fetched_time":fetchedTime}
                niftyObjlist.append(niftyObjmap)
    bankNiftyRecordID = bankNiftyCollection.insert_many(bankNiftyObjlist)
    niftyRecordID = niftyCollection.insert_many(niftyObjlist)
    print("timeStamp",fetchedTime," BankNifty ID: ",bankNiftyRecordID," Nifty ID: ",niftyRecordID)
    time.sleep(200)
