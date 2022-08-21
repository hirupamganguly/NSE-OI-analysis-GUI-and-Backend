from time import time
from pymongo import MongoClient
from datetime import datetime
from pytz import timezone 
from datetime import date
import dash
from dash import html as dhtml
from dash import dcc
import plotly.graph_objects as pgo
from dash.dependencies import Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import pandas as pd
try:
    conn = MongoClient("mongodb://localhost:27017/")
    print("Connected successfully!!!")
except:  
    print("Could not connect to MongoDB")

# database
databse = conn["NseOI"]
bankNiftyCollection = databse["BankNifty"]
niftyCollection = databse["Nifty"]
participantWiseCollection = databse["ParticipantWiseOI"]
noteCollection = databse["Notes"]

today_date=datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
dateArr=str.split(today_date,'-')
bnfOneCursor=bankNiftyCollection.find().sort('_id', -1).limit(1)
bnfOne={}
for bnf in bnfOneCursor:
    bnfOne=bnf
    break
bankNiftyAtmStrike= round(int(bnfOne["underlyingValue"])/100)*100

nfOneCursor=niftyCollection.find().sort('_id', -1).limit(1)
nfOne={}
for nf in nfOneCursor:
    nfOne=nf
    break
niftyAtmStrike= round(int(nfOne["underlyingValue"])/50)*50

def docLatestBankNifty():
    print("fetched data for: docLatestBankNifty")
    ce_oi_map={}
    pe_oi_map={}
    chng_ce_oi_map={}
    chng_pe_oi_map={}
    for i in range (bankNiftyAtmStrike-4000,bankNiftyAtmStrike+4000,100):
        bnfOneCursor=bankNiftyCollection.find({"strikePrice":i}).sort('_id', -1).limit(1)
        for bnfData in bnfOneCursor:
            ce_oi_map[i]=bnfData["ce_openInterest"]
            pe_oi_map[i]=bnfData["pe_openInterest"]
            chng_ce_oi_map[i]=bnfData["ce_changeinOpenInterest"]
            chng_pe_oi_map[i]=bnfData["pe_changeinOpenInterest"]
    df=pd.DataFrame({'strike':ce_oi_map.keys(),'ce_oi':list(ce_oi_map.values()),'chng_ce_oi':list(chng_ce_oi_map.values()),'pe_oi':list(pe_oi_map.values()),'chng_pe_oi':list(chng_pe_oi_map.values())})
    return df ,ce_oi_map,pe_oi_map,chng_ce_oi_map,chng_pe_oi_map

def docLatestNifty():
    print("fetched data for: docLatestNifty")
    ce_oi_map={}
    pe_oi_map={}
    chng_ce_oi_map={}
    chng_pe_oi_map={}
    for i in range (niftyAtmStrike-2000,niftyAtmStrike+2000,50):
        nfOneCursor=niftyCollection.find({"strikePrice":i}).sort('_id', -1).limit(1)
        for nfData in nfOneCursor:
            ce_oi_map[i]=nfData["ce_openInterest"]
            pe_oi_map[i]=nfData["pe_openInterest"]
            chng_ce_oi_map[i]=nfData["ce_changeinOpenInterest"]
            chng_pe_oi_map[i]=nfData["pe_changeinOpenInterest"]
    df=pd.DataFrame({'strike':ce_oi_map.keys(),'ce_oi':list(ce_oi_map.values()),'chng_ce_oi':list(chng_ce_oi_map.values()),'pe_oi':list(pe_oi_map.values()),'chng_pe_oi':list(chng_pe_oi_map.values())})
    return df ,ce_oi_map,pe_oi_map,chng_ce_oi_map,chng_pe_oi_map

def docOfParticipantWiseOI(date):
    doc=participantWiseCollection.find_one({'timestamp':date})
    if doc==None:
        proX=['0','0']
        proY=[0,0]
        fiiX=['0','0']
        fiiY=[0,0]
        diiX=['0','0']
        diiY=[0,0]
        clientX=['0','0']
        clientY=[0,0]
        return proX,proY,fiiX,fiiY,diiX,diiY,clientX,clientY
    clientFutPos=int(doc['client_future_index_long'])-int(doc['client_future_index_short'])
    clientFutStockPos=int(doc['client_future_stock_long'])-int(doc['client_future_stock_short'])
    clientOPLongPos=int(doc['client_option_index_call_long'])-int(doc['client_option_index_put_long'])
    clientOPShortPos=int(doc['client_option_index_call_short'])-int(doc['client_option_index_put_short'])
    clientStockLongPos=int(doc['client_option_stock_call_long'])-int(doc['client_option_stock_put_long'])
    clientStockShortPos=int(doc['client_option_stock_call_short'])-int(doc['client_option_stock_put_short'])

    diiFutPos=int(doc['dii_future_index_long'])-int(doc['dii_future_index_short'])
    diiFutStockPos=int(doc['dii_future_stock_long'])-int(doc['dii_future_stock_short'])
    diiOPLongPos=int(doc['dii_option_index_call_long'])-int(doc['dii_option_index_put_long'])
    diiOPShortPos=int(doc['dii_option_index_call_short'])-int(doc['dii_option_index_put_short'])
    diiStockLongPos=int(doc['dii_option_stock_call_long'])-int(doc['dii_option_stock_put_long'])
    diiStockShortPos=int(doc['dii_option_stock_call_short'])-int(doc['dii_option_stock_put_short'])

    fiiFutPos=int(doc['fii_future_index_long'])-int(doc['fii_future_index_short'])
    fiiFutStockPos=int(doc['fii_future_stock_long'])-int(doc['fii_future_stock_short'])
    fiiOPLongPos=int(doc['fii_option_index_call_long'])-int(doc['fii_option_index_put_long'])
    fiiOPShortPos=int(doc['fii_option_index_call_short'])-int(doc['fii_option_index_put_short'])
    fiiStockLongPos=int(doc['fii_option_stock_call_long'])-int(doc['fii_option_stock_put_long'])
    fiiStockShortPos=int(doc['fii_option_stock_call_short'])-int(doc['fii_option_stock_put_short'])

    proFutPos=int(doc['pro_future_index_long'])-int(doc['pro_future_index_short'])
    proFutStockPos=int(doc['pro_future_stock_long'])-int(doc['pro_future_stock_short'])
    proOPLongPos=int(doc['pro_option_index_call_long'])-int(doc['pro_option_index_put_long'])
    proOPShortPos=int(doc['pro_option_index_call_short'])-int(doc['pro_option_index_put_short'])
    proStockLongPos=int(doc['pro_option_stock_call_long'])-int(doc['pro_option_stock_put_long'])
    proStockShortPos=int(doc['pro_option_stock_call_short'])-int(doc['pro_option_stock_put_short'])
    proX=['P_FUT_INDX','P_FUT_STK','P_OP_LONG','P_OP_SHORT','P_STK_LONG','P_STK_SHORT']
    proY=[proFutPos,proFutStockPos,proOPLongPos,proOPShortPos,proStockLongPos,proStockShortPos]
    fiiX=['FI_FUT_INDX','FI_FUT_STK','FI_OP_LONG','FI_OP_SHORT','FI_STK_LONG','FI_STK_SHORT']
    fiiY=[fiiFutPos,fiiFutStockPos,fiiOPLongPos,fiiOPShortPos,fiiStockLongPos,fiiStockShortPos]
    diiX=['DI_FUT_INDX','DI_FUT_STK','DI_OP_LONG','DI_OP_SHORT','DI_STK_LONG','DI_STK_SHORT']
    diiY=[diiFutPos,diiFutStockPos,diiOPLongPos,diiOPShortPos,diiStockLongPos,diiStockShortPos]
    clientX=['CL_FUT_INDX','CL_FUT_STK','CL_OP_LONG','CL_OP_SHORT','CL_STK_LONG','CL_STK_SHORT']
    clientY=[clientFutPos,clientFutStockPos,clientOPLongPos,clientOPShortPos,clientStockLongPos,clientStockShortPos]
    return proX,proY,fiiX,fiiY,diiX,diiY,clientX,clientY

    

def docBystrikeAndDateBanknifty(strike,today_date):
    print("fetched data for: ",strike,"ATM is: ",bankNiftyAtmStrike ,"date: ",today_date)
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
                fetched_time=bnfByStrikeAndDate["fetched_time"]
                fetched_time_listArr=str.split(fetched_time,' ')
                time=fetched_time_listArr[1]
                objMap["fetched_time"]=time
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
                fetched_time=bnfByStrikeAndDate["fetched_time"]
                fetched_time_listArr=str.split(fetched_time,' ')
                time=fetched_time_listArr[1]
                objMap["fetched_time"]=time
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

def docBystrikeAndDateNifty(strike,today_date):
    print("fetched data for: ",strike,"ATM is: ",niftyAtmStrike ,"date: ",today_date)
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
    nfByStrikeAndDateCursor=niftyCollection.find({"strikePrice":strike,"date":today_date})

    for nfByStrikeAndDate in nfByStrikeAndDateCursor: 
        objMap={}
        if date.today().weekday() == 3 or date.today().weekday() == 2: # for wednessday and thursday add oi and chnginoi of current and next expiry
            if nfByStrikeAndDate["expiryDate"]==nfByStrikeAndDate["current_expiry"] or nfByStrikeAndDate["expiryDate"]==nfByStrikeAndDate["next_expiry"]:
                if objMap.get("ce_openInterest")==None:
                    objMap["ce_openInterest"]=nfByStrikeAndDate["ce_openInterest"]
                    ce_oi=nfByStrikeAndDate["ce_openInterest"]
                else:
                     objMap["ce_openInterest"]=nfByStrikeAndDate["ce_openInterest"]+ce_oi
                if objMap.get("ce_changeinOpenInterest")==None:
                    objMap["ce_changeinOpenInterest"]=nfByStrikeAndDate["ce_changeinOpenInterest"]
                    ce_chng_oi=nfByStrikeAndDate["ce_changeinOpenInterest"]
                else:
                     objMap["ce_changeinOpenInterest"]=nfByStrikeAndDate["ce_changeinOpenInterest"]+ce_chng_oi

                if objMap.get("pe_openInterest")==None:
                    objMap["pe_openInterest"]=nfByStrikeAndDate["pe_openInterest"]
                    pe_oi=nfByStrikeAndDate["pe_openInterest"]
                else:
                     objMap["pe_openInterest"]=nfByStrikeAndDate["pe_openInterest"]+pe_oi
                if objMap.get("pe_changeinOpenInterest")==None:
                    objMap["pe_changeinOpenInterest"]=nfByStrikeAndDate["pe_changeinOpenInterest"]
                    pe_chng_oi=nfByStrikeAndDate["pe_changeinOpenInterest"]
                else:
                     objMap["pe_changeinOpenInterest"]=nfByStrikeAndDate["pe_changeinOpenInterest"]+pe_chng_oi
                # otherdata       
                objMap["nse_timestamp"]=nfByStrikeAndDate["nse_timestamp"]
                objMap["strikePrice"]=nfByStrikeAndDate["strikePrice"]
                objMap["expiryDate"]=nfByStrikeAndDate["expiryDate"]
                objMap["underlyingValue"]=nfByStrikeAndDate["underlyingValue"]
                objMap["ce_lastPrice"]=nfByStrikeAndDate["ce_lastPrice"]
                objMap["ce_impliedVolatility"]=nfByStrikeAndDate["ce_impliedVolatility"]  
                objMap["pe_impliedVolatility"]=nfByStrikeAndDate["pe_impliedVolatility"]    
                objMap["pe_lastPrice"]=nfByStrikeAndDate["pe_lastPrice"]
                objMap["fetched_time"]=nfByStrikeAndDate["fetched_time"]
                fetched_time=nfByStrikeAndDate["fetched_time"]
                fetched_time_listArr=str.split(fetched_time,' ')
                time=fetched_time_listArr[1]
                objMap["fetched_time"]=time
                ce_oi_fetched.append(objMap["ce_openInterest"])
                pe_oi_fetched.append(objMap["pe_openInterest"])
                ce_chng_oi_fetched.append(objMap["ce_changeinOpenInterest"])
                pe_chng_oi_fetched.append(objMap["pe_changeinOpenInterest"])
                ce_ltp_fetched.append(objMap["ce_lastPrice"])
                pe_ltp_fetched.append(objMap["pe_lastPrice"])
                ce_impvol_fetched.append(objMap["ce_impliedVolatility"])
                pe_impvol_fetched.append(objMap["pe_impliedVolatility"])
        else:
            if nfByStrikeAndDate["expiryDate"]==nfByStrikeAndDate["current_expiry"]: # for other days just show current expiry data
                objMap["nse_timestamp"]=nfByStrikeAndDate["nse_timestamp"]
                objMap["strikePrice"]=nfByStrikeAndDate["strikePrice"]
                objMap["expiryDate"]=nfByStrikeAndDate["expiryDate"]
                objMap["underlyingValue"]=nfByStrikeAndDate["underlyingValue"]
                objMap["ce_lastPrice"]=nfByStrikeAndDate["ce_lastPrice"]
                objMap["ce_openInterest"]=nfByStrikeAndDate["ce_openInterest"]
                objMap["ce_changeinOpenInterest"]=nfByStrikeAndDate["ce_changeinOpenInterest"]
                objMap["ce_impliedVolatility"]=nfByStrikeAndDate["ce_impliedVolatility"]    
                objMap["pe_openInterest"]=nfByStrikeAndDate["pe_openInterest"]
                objMap["pe_changeinOpenInterest"]=nfByStrikeAndDate["pe_changeinOpenInterest"]
                objMap["pe_impliedVolatility"]=nfByStrikeAndDate["pe_impliedVolatility"]    
                objMap["pe_lastPrice"]=nfByStrikeAndDate["pe_lastPrice"]
                fetched_time=nfByStrikeAndDate["fetched_time"]
                fetched_time_listArr=str.split(fetched_time,' ')
                time=fetched_time_listArr[1]
                objMap["fetched_time"]=time
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

app=dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
ColumnStyle = {
    "margin-left": "1rem",
    "margin-right": "1rem",
    "padding": ".02rem .02rem",
}
DateStyle = {
    "background-color": "black",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "margin-top": ".2rem",
    "margin-bottom": ".22rem",
    "padding": ".05rem .05rem",
    "width": "100%",
    "text-align": "center"
}
BarGraphStyle={
    "width": "100%",
}
NoteStyle={
    'width': '100%', 
    'height': 200,
    "margin-left": "1rem",
    "margin-right": "1rem",
    "margin-top": "1rem",
    "margin-bottom": "1rem",
    "padding": ".1rem .2rem",
}
ButtonStyle={
    'width': '100%', 
    'height': 50,
    "margin-left": "1rem",
    "margin-right": "1rem",
    "padding": ".02rem .02rem",
    'background-color': '#05404a',
    'color': 'white',
}
NoteShowStyle={
    'whiteSpace': 'pre-line',
    'width': '100%', 
    'height': 200,
    "margin-left": "1rem",
    "margin-right": "1rem",
    "margin-top": "1rem",
    "margin-bottom": "1rem",
    "padding": ".1rem .2rem",
}
TxtAlignCenter={
    'text-align': 'center'
}

app.layout=dhtml.Div([ 
    dbc.Row([ #------DatePicker
        dcc.DatePickerSingle(
            id='which-date-oi',
            style=DateStyle,
            min_date_allowed=date(int(dateArr[0]),int(dateArr[1])-6,int(dateArr[2])),
            max_date_allowed=date(int(dateArr[0]),int(dateArr[1]),int(dateArr[2])),
            initial_visible_month=date(int(dateArr[0]),int(dateArr[1]),int(dateArr[2])),
            date=date(int(dateArr[0]),int(dateArr[1]),int(dateArr[2])),
        ),
    ]), #------DatePicker
    dbc.Row([ #-----Bar Chart
        dhtml.Div([dhtml.H5("Open-Interest BankNifty and Nifty",style=TxtAlignCenter)]),
        dbc.Col(dhtml.Div([
            dcc.Graph(id='live-update-bar-chart-bnf',animate=False,)
        ]),width=6, lg=6),
        dbc.Col(dhtml.Div([
            dcc.Graph(id='live-update-bar-chart-nf',animate=False)
        ]),width=6, lg=6)
    ]),
    
    dbc.Row([
        dhtml.Div([dhtml.H5("Change In Open-Interest BankNifty and Nifty",style=TxtAlignCenter)]),
        dbc.Col(dhtml.Div([
            dcc.Graph(id='live-update-bar-chart-chng-bnf',animate=False)
        ]),width=6, lg=6),
        dbc.Col(dhtml.Div([
            dcc.Graph(id='live-update-bar-chart-chng-nf',animate=False)
        ]),width=6, lg=6)
    ]),
    #-----Bar Chart
    dhtml.Div([dhtml.H5("Multi Strike Change In OI, IV, LTP Graphs",style=TxtAlignCenter)]),
    dbc.Row([
        dbc.Col(dhtml.Div([
            dbc.Row([ #------DropDown-1
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smalldropdownStrike1',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                value=str(bankNiftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smalldropdownType1',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-1
    dbc.Row([ #------Graph1
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-smallBNF1",animate=False)]),style=ColumnStyle,),
    ]),
        ]),width=6, lg=3),

         dbc.Col(dhtml.Div([
            dbc.Row([ #------DropDown-1
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smalldropdownStrike2',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                value=str(bankNiftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smalldropdownType2',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-1
    dbc.Row([ #------Graph1
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-smallBNF2",animate=False)]),style=ColumnStyle,),
    ]),
        ]),width=6, lg=3),

         dbc.Col(dhtml.Div([
            dbc.Row([ #------DropDown-1
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smalldropdownStrike3',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                value=str(bankNiftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smalldropdownType3',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-1
    dbc.Row([ #------Graph1
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-smallBNF3",animate=False)]),style=ColumnStyle,),
    ]),
        ]),width=6, lg=3),

         dbc.Col(dhtml.Div([
            dbc.Row([ #------DropDown-1
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smalldropdownStrike4',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                value=str(bankNiftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smalldropdownType4',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-1
    dbc.Row([ #------Graph1
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-smallBNF4",animate=False)]),style=ColumnStyle,),
    ]),
        ]),width=6, lg=3),
    ]),
    dbc.Row([
        dbc.Col(dhtml.Div([
            dbc.Row([ #------DropDown-1
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smallNFdropdownStrike1',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(niftyAtmStrike-1000,niftyAtmStrike+1000,50)],
                value=str(niftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smallNFdropdownType1',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-1
    dbc.Row([ #------Graph1
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-smallNF1",animate=False)]),style=ColumnStyle,),
    ]),
        ]),width=6, lg=3),

         dbc.Col(dhtml.Div([
            dbc.Row([ #------DropDown-1
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smallNFdropdownStrike2',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(niftyAtmStrike-1000,niftyAtmStrike+1000,50)],
                value=str(niftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smallNFdropdownType2',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-1
    dbc.Row([ #------Graph1
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-smallNF2",animate=False)]),style=ColumnStyle,),
    ]),
        ]),width=6, lg=3),

         dbc.Col(dhtml.Div([
            dbc.Row([ #------DropDown-1
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smallNFdropdownStrike3',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(niftyAtmStrike-1000,niftyAtmStrike+1000,50)],
                value=str(niftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smallNFdropdownType3',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-1
    dbc.Row([ #------Graph1
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-smallNF3",animate=False)]),style=ColumnStyle,),
    ]),
        ]),width=6, lg=3),

         dbc.Col(dhtml.Div([
            dbc.Row([ #------DropDown-1
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smallNFdropdownStrike4',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(niftyAtmStrike-1000,niftyAtmStrike+1000,50)],
                value=str(niftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='smallNFdropdownType4',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-1
    dbc.Row([ #------Graph1
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-smallNF4",animate=False)]),style=ColumnStyle,),
    ]),
        ]),width=6, lg=3),
    ]),

    #------- BankNifty
    dbc.Row([ #------DropDown-1
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownStrike1',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                value=str(bankNiftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownType1',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-1
    dbc.Row([ #------Graph1
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-BNF",animate=False)]),style=ColumnStyle,),
    ]), #------Graph1
    dbc.Row([ #------DropDown-2
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownStrike2',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                value=str(bankNiftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownType2',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-2
    dbc.Row([ #------Graph2
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-BNF-2",animate=False)]),style=ColumnStyle,),
    ]), #------Graph2

    dbc.Row([ #------DropDown-1
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownStrike3',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(niftyAtmStrike-1000,niftyAtmStrike+1000,50)],
                value=str(niftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownType3',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-1
    dbc.Row([ #------Graph1
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-NF",animate=False)]),style=ColumnStyle,),
    ]), #------Graph1
    #---- Nifty
    dbc.Row([ #------DropDown-2
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownStrike4',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(niftyAtmStrike-1000,niftyAtmStrike+1000,50)],
                value=str(niftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownType4',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-2
    dbc.Row([ #------Graph2
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-NF-2",animate=False)]),style=ColumnStyle,),
    ]), #------Graph2
   
    dbc.Row([ #------DropDown-1
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownStrike5',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                value=str(bankNiftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownType5',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-1
    dbc.Row([ #------Graph1
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-BNF-3",animate=False)]),style=ColumnStyle,),
    ]), #------Graph1
    #---- Nifty
    dbc.Row([ #------DropDown-2
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownStrike6',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                value=str(bankNiftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownType6',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-2
    dbc.Row([ #------Graph2
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-BNF-4",animate=False)]),style=ColumnStyle,),
    ]), #------Graph2
   
    dbc.Row([ #------DropDown-1
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownStrike7',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(niftyAtmStrike-1000,niftyAtmStrike+1000,50)],
                value=str(niftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownType7',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-1
    dbc.Row([ #------Graph1
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-NF-3",animate=False)]),style=ColumnStyle,),
    ]), #------Graph1
    #---- Nifty
    dbc.Row([ #------DropDown-2
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownStrike8',
                style=ColumnStyle,
                options=[{"label":str(i),"value":str(i)} for i in range(niftyAtmStrike-1000,niftyAtmStrike+1000,50)],
                value=str(niftyAtmStrike),
            ),
        ])),
        dbc.Col(dhtml.Div([
            dcc.Dropdown(
                id='dropdownType8',
                style=ColumnStyle,
                options=[{"label":"CE", "value":"CE"},{"label":"PE", "value":"PE"}],
                value="CE",
            ),
        ]))
    ]), #------DropDown-2
    dbc.Row([ #------Graph2
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-graph-NF-4",animate=False)]),style=ColumnStyle,),
    ]), #------Graph2
  
    # DB Futures Update:
    dhtml.Div([dhtml.H4("Previous Day Participant Wise OI",style=TxtAlignCenter)]),
    dbc.Row([
        dbc.Col(dhtml.Div([dcc.Graph(id='live-update-bar-participants-client',animate=False,)]),width=6, lg=3),
        dbc.Col(dhtml.Div([dcc.Graph(id='live-update-bar-participants-fii',animate=False,)]),width=6, lg=3),
        dbc.Col(dhtml.Div([dcc.Graph(id='live-update-bar-participants-dii',animate=False,)]),width=6, lg=3),
        dbc.Col(dhtml.Div([dcc.Graph(id='live-update-bar-participants-pro',animate=False,)]),width=6, lg=3),
    ]),
    # DB NOTES ADD:
    dbc.Row([
        dhtml.Div([dhtml.H5("--------------Trade-Journal--------------",style=TxtAlignCenter)]),
        dbc.Col(dhtml.Div([
            dcc.Textarea(
                id='textarea-state',
                value='',
                style=NoteStyle,
            ),
            dbc.Col(dhtml.Div([
                dbc.Row([
                    dbc.Col(dhtml.Div([
                        dhtml.Button('Submit', id='textarea-state-button', n_clicks=0, style=ButtonStyle,),
                    ])),
                    dbc.Col(dhtml.Div([
                        dbc.Button("ERASE-DB (double click)", id="example-button", style=ButtonStyle, n_clicks=0),
                        dhtml.Span(id="example-output", style={"verticalAlign": "middle"}),
                    ])),
                ]),
            ])),
        ])),
        dbc.Col(dhtml.Div([
            dhtml.Div(id='textarea-state-output', style=NoteShowStyle)
        ]))
    ]),
    
    dcc.Interval(
        id="interval-component",interval=100*1000,n_intervals=0
    ),
])  

#BANKNIFTY-  OI BAR
@app.callback(
    Output('live-update-bar-chart-bnf','figure'),
    Input('interval-component', 'n_intervals')
)
def updateBarChartBnf(n):
    df,ce_oi_map,pe_oi_map,chng_ce_oi_map,chng_pe_oi_map=docLatestBankNifty()
    fig = pgo.Figure()
    fig.add_trace(pgo.Scatter(x=df['strike'], y=df['ce_oi'],
                    mode='lines+markers',
                    marker_color='green',
                    name='BNF: CE_OI'))
    fig.add_trace(pgo.Scatter(x=df['strike'], y=df['pe_oi'],
                    mode='lines+markers',
                    marker_color='red',
                    name='BNF: PE_OI'))
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest',)
    fig.layout.autosize=True
    return fig

#NIFTY-  OI BAR
@app.callback(
    Output('live-update-bar-chart-nf','figure'),
    Input('interval-component', 'n_intervals')
)
def updateBarChartNf(n):
    df,ce_oi_map,pe_oi_map,chng_ce_oi_map,chng_pe_oi_map=docLatestNifty()
    fig = pgo.Figure()
    fig.add_trace(pgo.Scatter(x=df['strike'], y=df['ce_oi'],
                    mode='lines+markers',
                    marker_color='green',
                    name='NF: CE_OI'))
    fig.add_trace(pgo.Scatter(x=df['strike'], y=df['pe_oi'],
                    mode='lines+markers',
                    marker_color='red',
                    name='NF: PE_OI'))
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
    fig.layout.autosize=True
    return fig

#BANKNIFTY-  CHNG_OI BAR
@app.callback(
    Output('live-update-bar-chart-chng-bnf','figure'),
    Input('interval-component', 'n_intervals')
)
def updateBarChartChngNf(n):
    df,ce_oi_map,pe_oi_map,chng_ce_oi_map,chng_pe_oi_map=docLatestBankNifty()
    fig = pgo.Figure()
    fig.add_trace(pgo.Scatter(x=df['strike'], y=df['chng_ce_oi'],
                    mode='lines+markers',
                    marker_color='green',
                    name='BNF: CHNG_CE_OI'))
    fig.add_trace(pgo.Scatter(x=df['strike'], y=df['chng_pe_oi'],
                    mode='lines+markers',
                    marker_color='red',
                    name='BNF: CHNG_PE_OI'))
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
    fig.layout.autosize=True
    return fig

#NIFTY-  CHNG_OI BAR
@app.callback(
    Output('live-update-bar-chart-chng-nf','figure'),
    Input('interval-component', 'n_intervals')
)
def updateBarChartChngNf(n):
    df,ce_oi_map,pe_oi_map,chng_ce_oi_map,chng_pe_oi_map=docLatestNifty()
    fig = pgo.Figure()
    fig.add_trace(pgo.Scatter(x=df['strike'], y=df['chng_ce_oi'],
                    mode='lines+markers',
                    marker_color='green',
                    name='NF: CHNG_CE_OI'))
    fig.add_trace(pgo.Scatter(x=df['strike'], y=df['chng_pe_oi'],
                    mode='lines+markers',
                    marker_color='red',
                    name='NF: CHNG_PE_OI'))
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
    fig.layout.autosize=True
    return fig

@app.callback(
    Output('live-update-graph-smallBNF1','figure'),
    Input('which-date-oi','date'),
    Input('smalldropdownStrike1','value'),
    Input('smalldropdownType1','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph1_small_1(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig

@app.callback(
    Output('live-update-graph-smallBNF2','figure'),
    Input('which-date-oi','date'),
    Input('smalldropdownStrike2','value'),
    Input('smalldropdownType2','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph1_small_2(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig

@app.callback(
    Output('live-update-graph-smallBNF3','figure'),
    Input('which-date-oi','date'),
    Input('smalldropdownStrike3','value'),
    Input('smalldropdownType3','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph1_small_3(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig

@app.callback(
    Output('live-update-graph-smallBNF4','figure'),
    Input('which-date-oi','date'),
    Input('smalldropdownStrike4','value'),
    Input('smalldropdownType4','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph1_small_4(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig

@app.callback(
    Output('live-update-graph-BNF','figure'),
    Input('which-date-oi','date'),
    Input('dropdownStrike1','value'),
    Input('dropdownType1','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph1(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig


@app.callback(
    Output('live-update-graph-BNF-2','figure'),
    Input('which-date-oi','date'),
    Input('dropdownStrike2','value'),
    Input('dropdownType2','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines'),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines'),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines'),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig

@app.callback(
    Output('live-update-graph-smallNF1','figure'),
    Input('which-date-oi','date'),
    Input('smallNFdropdownStrike1','value'),
    Input('smallNFdropdownType1','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2_NF_1(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateNifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines'),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines'),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines'),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig
@app.callback(
    Output('live-update-graph-smallNF2','figure'),
    Input('which-date-oi','date'),
    Input('smallNFdropdownStrike2','value'),
    Input('smallNFdropdownType2','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2_NF_2(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateNifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines'),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines'),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines'),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig
@app.callback(
    Output('live-update-graph-smallNF3','figure'),
    Input('which-date-oi','date'),
    Input('smallNFdropdownStrike3','value'),
    Input('smallNFdropdownType3','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2_NF_3(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateNifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines'),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines'),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines'),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig

@app.callback(
    Output('live-update-graph-smallNF4','figure'),
    Input('which-date-oi','date'),
    Input('smallNFdropdownStrike4','value'),
    Input('smallNFdropdownType4','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2_NF_4(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateNifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines'),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines'),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines'),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig


@app.callback(
    Output('live-update-graph-NF','figure'),
    Input('which-date-oi','date'),
    Input('dropdownStrike3','value'),
    Input('dropdownType3','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateNifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines'),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines'),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines'),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig


@app.callback(
    Output('live-update-graph-NF-2','figure'),
    Input('which-date-oi','date'),
    Input('dropdownStrike4','value'),
    Input('dropdownType4','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateNifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines'),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines'),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines'),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig

@app.callback(
    Output('live-update-graph-BNF-3','figure'),
    Input('which-date-oi','date'),
    Input('dropdownStrike5','value'),
    Input('dropdownType5','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph1(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig


@app.callback(
    Output('live-update-graph-BNF-4','figure'),
    Input('which-date-oi','date'),
    Input('dropdownStrike6','value'),
    Input('dropdownType6','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines'),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines'),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines'),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig  



@app.callback(
    Output('live-update-graph-NF-3','figure'),
    Input('which-date-oi','date'),
    Input('dropdownStrike7','value'),
    Input('dropdownType7','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateNifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines'),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines'),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines'),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig

@app.callback(
    Output('live-update-graph-NF-4','figure'),
    Input('which-date-oi','date'),
    Input('dropdownStrike8','value'),
    Input('dropdownType8','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,strikeType,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateNifty(int(strikeValue),date_string)
    if strikeType=="CE":
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data",mode='lines',),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data",mode='lines',),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data",mode='lines',),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data",mode='lines'),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data",mode='lines'),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data",mode='lines'),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',legend_orientation="h",hovermode='closest')
        fig.layout.autosize=True
    return fig

#DB Futures
@app.callback(
    Output('live-update-bar-participants-client','figure'),
    Input('which-date-oi','date'),
)
def updateliveupdatebarparticipantsclient(date):
    dateArr=str.split(date,'-')
    dateNumber=int(dateArr[2])-1
    dateString=dateArr[0]+'-'+dateArr[1]+'-'+str(dateNumber)
    proX,proY,fiiX,fiiY,diiX,diiY,clientX,clientY=docOfParticipantWiseOI(date=dateString)
    fig = px.bar(x=clientX, y=clientY)
    fig.update_yaxes(title='')
    fig.update_xaxes(title='0> CE side, 0< PE side')
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',)
    return fig

@app.callback(
    Output('live-update-bar-participants-fii','figure'),
    Input('which-date-oi','date'),
)
def updateliveupdatebarparticipantsfii(date):
    dateArr=str.split(date,'-')
    dateNumber=int(dateArr[2])-1
    dateString=dateArr[0]+'-'+dateArr[1]+'-'+str(dateNumber)
    proX,proY,fiiX,fiiY,diiX,diiY,clientX,clientY=docOfParticipantWiseOI(date=dateString)
    fig = px.bar(x=fiiX, y=fiiY)
    fig.update_yaxes(title='')
    fig.update_xaxes(title='0> CE side, 0< PE side')
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',)
    return fig

@app.callback(
    Output('live-update-bar-participants-dii','figure'),
    Input('which-date-oi','date'),
)
def updateliveupdatebarparticipantsdii(date):
    dateArr=str.split(date,'-')
    dateNumber=int(dateArr[2])-1
    dateString=dateArr[0]+'-'+dateArr[1]+'-'+str(dateNumber)
    proX,proY,fiiX,fiiY,diiX,diiY,clientX,clientY=docOfParticipantWiseOI(date=dateString)
    fig = px.bar(x=diiX, y=diiY,)
    fig.update_yaxes(title='')
    fig.update_xaxes(title='0> CE side, 0< PE side')
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',)
    return fig

@app.callback(
    Output('live-update-bar-participants-pro','figure'),
    Input('which-date-oi','date'),
)
def updateliveupdatebarparticipantspro(date):
    dateArr=str.split(date,'-')
    dateNumber=int(dateArr[2])-1
    dateString=dateArr[0]+'-'+dateArr[1]+'-'+str(dateNumber)
    proX,proY,fiiX,fiiY,diiX,diiY,clientX,clientY=docOfParticipantWiseOI(date=dateString)
    fig = px.bar(x=proX, y=proY)
    fig.update_yaxes(title='')
    fig.update_xaxes(title='0> CE side, 0< PE side')
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20),plot_bgcolor='rgba(255, 255, 255,100)',)
    return fig

#Notes
@app.callback(
    Output('textarea-state-output', 'children'),
    Input('textarea-state-button', 'n_clicks'),
    State('textarea-state', 'value')
)
def update_output(n_clicks, value):
    crTime=datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
    if n_clicks > 0:
        notes={'time':crTime,'note':value}
        notesRecordID = noteCollection.insert_one(notes)
        notesCursor=noteCollection.find({'time':crTime}).sort('_id', -1)
        notesArr=""
        for noteDoc in notesCursor:
            notesArr=notesArr+"\n"+noteDoc['note']
        return '{}'.format(notesArr)

@app.callback(
    Output("example-output", "children"), [Input("example-button", "n_clicks")]
)
def on_button_click(n):
    crTime=datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
    if n is None:
        return "Double Click to Delete."
    else:
        if n > 1:
            noteCollection.delete_many({'time':crTime})
            return f"DB-DELETED"

app.run_server()
