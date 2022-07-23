from pymongo import MongoClient
from datetime import datetime
from pytz import timezone 
from datetime import date

try:
    conn = MongoClient("mongodb://localhost:27017/")
    print("Connected successfully!!!")
except:  
    print("Could not connect to MongoDB")

# database
databse = conn["NseOI"]
bankNiftyCollection = databse["BankNifty"]
niftyCollection = databse["Nifty"]

today_date=datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
bnfOne=bankNiftyCollection.find_one()
bankNiftyAtmStrike= round(int(bnfOne["underlyingValue"])/100)*100

def docBystrikeAndDate(strike,today_date):
    objMapList=[]
    ce_oi_fetched=[]
    pe_oi_fetched=[]
    fetched_time_list=[]
    ce_chng_oi_fetched=[]
    pe_chng_oi_fetched=[]
    ce_impvol_fetched=[]
    pe_impvol_fetched=[]
    ce_ltp_fetched=[]
    pe_ltp_fetched=[]
    ce_oi=0
    ce_chng_oi=0
    pe_oi=0
    pe_chng_oi=0
    bnfByStrikeAndDateCursor=bankNiftyCollection.find({"strikePrice":strike,"date":today_date})
    for bnfByStrikeAndDate in bnfByStrikeAndDateCursor: # get 3 expiry data of a strike of Today
        objMap={}
        if date.today().weekday() == 3 or date.today().weekday() == 2: # for wednessday and thursday add oi and chnginoi of current and next expiry
            if bnfByStrikeAndDate["expiryDate"]==bnfByStrikeAndDate["current_expiry"] or bnfByStrikeAndDate["expiryDate"]==bnfByStrikeAndDate["next_expiry"]:
                if objMap.get("ce_openInterest")==None:
                    objMap["ce_openInterest"]=bnfByStrikeAndDate["ce_openInterest"]
                    ce_oi=bnfByStrikeAndDate["ce_openInterest"]
                else:
                     objMap["ce_openInterest"]=bnfByStrikeAndDate["ce_openInterest"]+ce_oi
                if objMap.get("ce_changeinOpenInterest")==None:
                    objMap["ce_changeinOpenInterest"]=bnfByStrikeAndDate["ce_changeinOpenInterest"]
                    ce_chng_oi=bnfByStrikeAndDate["ce_changeinOpenInterest"]
                else:
                     objMap["ce_changeinOpenInterest"]=bnfByStrikeAndDate["ce_changeinOpenInterest"]+ce_chng_oi

                if objMap.get("pe_openInterest")==None:
                    objMap["pe_openInterest"]=bnfByStrikeAndDate["pe_openInterest"]
                    pe_oi=bnfByStrikeAndDate["pe_openInterest"]
                else:
                     objMap["pe_openInterest"]=bnfByStrikeAndDate["pe_openInterest"]+pe_oi
                if objMap.get("pe_changeinOpenInterest")==None:
                    objMap["pe_changeinOpenInterest"]=bnfByStrikeAndDate["pe_changeinOpenInterest"]
                    pe_chng_oi=bnfByStrikeAndDate["pe_changeinOpenInterest"]
                else:
                     objMap["pe_changeinOpenInterest"]=bnfByStrikeAndDate["pe_changeinOpenInterest"]+pe_chng_oi
                # otherdata       
                objMap["nse_timestamp"]=bnfByStrikeAndDate["nse_timestamp"]
                objMap["strikePrice"]=bnfByStrikeAndDate["strikePrice"]
                objMap["expiryDate"]=bnfByStrikeAndDate["expiryDate"]
                objMap["underlyingValue"]=bnfByStrikeAndDate["underlyingValue"]
                objMap["ce_lastPrice"]=bnfByStrikeAndDate["ce_lastPrice"]
                objMap["ce_impliedVolatility"]=bnfByStrikeAndDate["ce_impliedVolatility"]  
                objMap["pe_impliedVolatility"]=bnfByStrikeAndDate["pe_impliedVolatility"]    
                objMap["pe_lastPrice"]=bnfByStrikeAndDate["pe_lastPrice"]
                objMap["fetched_time"]=bnfByStrikeAndDate["fetched_time"]
                fetched_time_list.append[objMap["fetched_time"]]
                ce_oi_fetched.append(objMap["ce_openInterest"])
                pe_oi_fetched.append(objMap["pe_openInterest"])
                ce_chng_oi_fetched.append(objMap["ce_changeinOpenInterest"])
                pe_chng_oi_fetched.append(objMap["pe_changeinOpenInterest"])
                ce_ltp_fetched.append(objMap["ce_lastPrice"])
                pe_ltp_fetched.append(objMap["pe_lastPrice"])
                ce_impvol_fetched.append(objMap["ce_impliedVolatility"])
                pe_impvol_fetched.append(objMap["pe_impliedVolatility"])
        else:
            if bnfByStrikeAndDate["expiryDate"]==bnfByStrikeAndDate["current_expiry"]: # for other days just show current expiry data
                objMap["nse_timestamp"]=bnfByStrikeAndDate["nse_timestamp"]
                objMap["strikePrice"]=bnfByStrikeAndDate["strikePrice"]
                objMap["expiryDate"]=bnfByStrikeAndDate["expiryDate"]
                objMap["underlyingValue"]=bnfByStrikeAndDate["underlyingValue"]
                objMap["ce_lastPrice"]=bnfByStrikeAndDate["ce_lastPrice"]
                objMap["ce_openInterest"]=bnfByStrikeAndDate["ce_openInterest"]
                objMap["ce_changeinOpenInterest"]=bnfByStrikeAndDate["ce_changeinOpenInterest"]
                objMap["ce_impliedVolatility"]=bnfByStrikeAndDate["ce_impliedVolatility"]    
                objMap["pe_openInterest"]=bnfByStrikeAndDate["pe_openInterest"]
                objMap["pe_changeinOpenInterest"]=bnfByStrikeAndDate["pe_changeinOpenInterest"]
                objMap["pe_impliedVolatility"]=bnfByStrikeAndDate["pe_impliedVolatility"]    
                objMap["pe_lastPrice"]=bnfByStrikeAndDate["pe_lastPrice"]
                objMap["fetched_time"]=bnfByStrikeAndDate["fetched_time"]
                fetched_time_list.append(objMap["fetched_time"])
                ce_oi_fetched.append(objMap["ce_openInterest"])
                pe_oi_fetched.append(objMap["pe_openInterest"])
                ce_chng_oi_fetched.append(objMap["ce_changeinOpenInterest"])
                pe_chng_oi_fetched.append(objMap["pe_changeinOpenInterest"])
                ce_ltp_fetched.append(objMap["ce_lastPrice"])
                pe_ltp_fetched.append(objMap["pe_lastPrice"])
                ce_impvol_fetched.append(objMap["ce_impliedVolatility"])
                pe_impvol_fetched.append(objMap["pe_impliedVolatility"])
    return ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched

ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched=docBystrikeAndDate(bankNiftyAtmStrike,today_date)
