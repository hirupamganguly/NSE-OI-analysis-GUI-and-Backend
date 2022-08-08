import string
import requests
import pytz
from pymongo import MongoClient
from datetime import datetime
import json
import time
from pytz import timezone 

class Datum:
    strikePrice: int
    expiryDate: string
    underlying: string
    identifier: str
    openInterest: int
    changeinOpenInterest: int
    pchangeinOpenInterest: float
    totalTradedVolume: int
    impliedVolatility: float
    lastPrice: float
    change: float
    pChange: float
    totalBuyQuantity: int
    totalSellQuantity: int
    bidQty: int
    bidprice: float
    askQty: int
    askPrice: float
    underlyingValue: float

    def __init__(self, strikePrice: int, expiryDate: string, underlying: string, identifier: str, openInterest: int, changeinOpenInterest: int, pchangeinOpenInterest: float, totalTradedVolume: int, impliedVolatility: float, lastPrice: float, change: float, pChange: float, totalBuyQuantity: int, totalSellQuantity: int, bidQty: int, bidprice: float, askQty: int, askPrice: float, underlyingValue: float) -> None:
        self.strikePrice = strikePrice
        self.expiryDate = expiryDate
        self.underlying = underlying
        self.identifier = identifier
        self.openInterest = openInterest
        self.changeinOpenInterest = changeinOpenInterest
        self.pchangeinOpenInterest = pchangeinOpenInterest
        self.totalTradedVolume = totalTradedVolume
        self.impliedVolatility = impliedVolatility
        self.lastPrice = lastPrice
        self.change = change
        self.pChange = pChange
        self.totalBuyQuantity = totalBuyQuantity
        self.totalSellQuantity = totalSellQuantity
        self.bidQty = bidQty
        self.bidprice = bidprice
        self.askQty = askQty
        self.askPrice = askPrice
        self.underlyingValue = underlyingValue

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
        if strikePrice in range(bankNiftyAtmStrike-28000,bankNiftyAtmStrike+28000,100):
            if expiryDate in expiry_Dates:
                if expiryDate in expiry_Dates:
                    if "PE" not in data:  
                        dataDefaultValuePE=Datum(data["CE"]["strikePrice"],data["CE"]["expiryDate"],data["CE"]["underlying"],data["CE"]["identifier"],0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
                        print("defaukt added for PE strike: ",data["CE"]["strikePrice"]," and expiry: ",data["CE"]["expiryDate"])
                        getattr(data, 'PE', dataDefaultValuePE)
                    if "CE" not in data:  
                        dataDefaultValueCE=Datum(data["PE"]["strikePrice"],data["PE"]["expiryDate"],data["PE"]["underlying"],data["PE"]["identifier"],0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
                        print("defaukt added for CE strike: ",data["PE"]["strikePrice"]," and expiry: ",data["PE"]["expiryDate"])
                        getattr(data, 'CE', dataDefaultValueCE)

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
        if strikePrice in range(niftyAtmStrike-2000,niftyAtmStrike+2000,50):
            if expiryDate in expiry_Dates:
                if "PE" not in data:  
                    dataDefaultValuePE=Datum(data["CE"]["strikePrice"],data["CE"]["expiryDate"],data["CE"]["underlying"],data["CE"]["identifier"],0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
                    print("defaukt added for PE strike: ",data["CE"]["strikePrice"]," and expiry: ",data["CE"]["expiryDate"])
                    getattr(data, 'PE', dataDefaultValuePE)
                if "CE" not in data:  
                     dataDefaultValueCE=Datum(data["PE"]["strikePrice"],data["PE"]["expiryDate"],data["PE"]["underlying"],data["PE"]["identifier"],0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
                     print("defaukt added for CE strike: ",data["PE"]["strikePrice"]," and expiry: ",data["PE"]["expiryDate"])
                     getattr(data, 'CE', dataDefaultValueCE)
                niftyObjmap={"date":timestamp,"nse_timestamp":time_stamp,"strikePrice":data["strikePrice"],"expiryDate":data["expiryDate"],"underlyingValue":data["CE"]["underlyingValue"],"ce_lastPrice":data["CE"]["lastPrice"],"ce_openInterest":data["CE"]["openInterest"],"ce_changeinOpenInterest":data["CE"]["changeinOpenInterest"],"ce_totalTradedVolume":data["CE"]["totalTradedVolume"],"ce_impliedVolatility":data["CE"]["impliedVolatility"],"ce_totalBuyQuantity":data["CE"]["totalBuyQuantity"],"ce_totalSellQuantity":data["CE"]["totalSellQuantity"],"pe_lastPrice":data["PE"]["lastPrice"],"pe_openInterest":data["PE"]["openInterest"],"pe_changeinOpenInterest":data["PE"]["changeinOpenInterest"],"pe_totalTradedVolume":data["PE"]["totalTradedVolume"],"pe_impliedVolatility":data["PE"]["impliedVolatility"],"pe_totalBuyQuantity":data["PE"]["totalBuyQuantity"],"pe_totalSellQuantity":data["PE"]["totalSellQuantity"],"current_expiry":expiryDates[0],"next_expiry":expiryDates[1],"fetched_time":fetchedTime}
                niftyObjlist.append(niftyObjmap)
    bankNiftyRecordID = bankNiftyCollection.insert_many(bankNiftyObjlist)
    niftyRecordID = niftyCollection.insert_many(niftyObjlist)
    print("timeStamp",fetchedTime," BankNifty ID: ",bankNiftyRecordID," Nifty ID: ",niftyRecordID)
    time.sleep(200)
