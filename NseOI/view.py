from time import time
from pymongo import MongoClient
from datetime import datetime
from pytz import timezone 
from datetime import date
import dash
from dash import html as dhtml
from dash import dcc
import plotly.graph_objects as pgo
from dash.dependencies import Output, Input


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

    # data comming from DB get 3 expiry data of a strike of Today
    bnfByStrikeAndDateCursor=bankNiftyCollection.find({"strikePrice":strike,"date":today_date})

    for bnfByStrikeAndDate in bnfByStrikeAndDateCursor: 
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
    return ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list

def docByRecent():
    recentDocCursor=bankNiftyCollection.find({"strikePrice":{"$gte":bankNiftyAtmStrike-1000,"$lt":bankNiftyAtmStrike+1000},"nse_timestamp":bnfOne["nse_timestamp"]})
    ce_oi_fetched=[]
    pe_oi_fetched=[]
    ce_chng_oi_fetched=[]
    pe_chng_oi_fetched=[]
    for recentDoc in recentDocCursor:
        if recentDoc["expiryDate"]==recentDoc["current_expiry"]:
            ce_oi_fetched.append(recentDoc["ce_openInterest"])
            ce_chng_oi_fetched.append(recentDoc["ce_changeinOpenInterest"])
            pe_oi_fetched.append(recentDoc["pe_openInterest"])
            pe_chng_oi_fetched.append(recentDoc["pe_changeinOpenInterest"])
    return ce_oi_fetched,pe_oi_fetched,ce_chng_oi_fetched,pe_chng_oi_fetched

app=dash.Dash()


app.layout=dhtml.Div(
    [
        dcc.Graph(id="live-update-graph",animate=True),
        dcc.Interval(
            id="interval-component",interval=100*1000,n_intervals=0
        ),
    ]
)
@app.callback(
    Output("live-update-graph","figure"),
    Input("interval-component","n_intervals")
)
def update_strike_graph(n):
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDate(bankNiftyAtmStrike,today_date)
    graph=pgo.Scatter(x=fetched_time_list,y=ce_oi_fetched)
    fig=pgo.Figure(graph)
    fig.layout.autosize=True
    print("CHECK")
    return fig

app.run_server()
