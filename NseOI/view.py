from time import time
from unicodedata import name
from pymongo import MongoClient
from datetime import datetime
from pytz import timezone 
from datetime import date
import dash
from dash import html as dhtml
from dash import dcc
import plotly.graph_objects as pgo
from dash.dependencies import Output, Input
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
    return df

def docLatestNifty():
    print("fetched data for: docLatestNifty")
    ce_oi_map={}
    pe_oi_map={}
    chng_ce_oi_map={}
    chng_pe_oi_map={}
    for i in range (niftyAtmStrike-2000,niftyAtmStrike+2000,500):
        nfOneCursor=niftyCollection.find({"strikePrice":i}).sort('_id', -1).limit(1)
        for nfData in nfOneCursor:
            ce_oi_map[i]=nfData["ce_openInterest"]
            pe_oi_map[i]=nfData["pe_openInterest"]
            chng_ce_oi_map[i]=nfData["ce_changeinOpenInterest"]
            chng_pe_oi_map[i]=nfData["pe_changeinOpenInterest"]
    df=pd.DataFrame({'strike':ce_oi_map.keys(),'ce_oi':list(ce_oi_map.values()),'chng_ce_oi':list(chng_ce_oi_map.values()),'pe_oi':list(pe_oi_map.values()),'chng_pe_oi':list(chng_pe_oi_map.values())})
    return df



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
app.layout=dhtml.Div([ 
    dbc.Row([
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-barchart1",animate=True,style=BarGraphStyle,
            )
        ])),
        dbc.Col(dhtml.Div([
            dcc.Graph(id="live-update-barchart2",animate=True,style=BarGraphStyle,
            )
        ]))
    ]),
    dbc.Row([
        dcc.DatePickerSingle(
            id='which-date-oi',
            style=DateStyle,
            min_date_allowed=date(int(dateArr[0]),int(dateArr[1])-6,int(dateArr[2])),
            max_date_allowed=date(int(dateArr[0]),int(dateArr[1]),int(dateArr[2])),
            initial_visible_month=date(int(dateArr[0]),int(dateArr[1]),int(dateArr[2])),
            date=date(int(dateArr[0]),int(dateArr[1]),int(dateArr[2])),
        ),
    ]),
    dbc.Row([
        # Col 1
        dbc.Col(dhtml.Div([
            dbc.Row([ 
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
                ])),
            ]),
        dbc.Row([
            dbc.Col(dhtml.Div([
                dcc.Graph(id="live-update-graph1",animate=True)]),style=ColumnStyle,),
            ]),
        ])),

        # Col 2
        dbc.Col(dhtml.Div([
            dbc.Row([ 
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
                ])),
            ]),
        dbc.Row([
            dbc.Col(dhtml.Div([
                dcc.Graph(id="live-update-graph2",animate=True)]),style=ColumnStyle,),
            ]),
        ])),
    
    ]),
    dcc.Interval(
        id="interval-component",interval=100*1000,n_intervals=0
    ),
])  

@app.callback(
    Output('live-update-graph1','figure'),
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
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data"),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data"),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data"),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=10),legend_orientation="h")
        fig.update_xaxes(title_text="Time")
        fig.update_yaxes(title_text="CHNG_OI-Data",secondary_y=False)
        fig.update_yaxes(title_text="LTP-Data",secondary_y=True)
        fig.update_yaxes(title_text="IV-Data",secondary_y=True)
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data"),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data"),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data"),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=10),legend_orientation="h")
        fig.update_xaxes(title_text="Time")
        fig.update_yaxes(title_text="CHNG_OI-Data",secondary_y=False)
        fig.update_yaxes(title_text="LTP-Data",secondary_y=True)
        fig.update_yaxes(title_text="IV-Data",secondary_y=True)
        fig.layout.autosize=True
    return fig


@app.callback(
    Output('live-update-graph2','figure'),
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
            pgo.Scatter(x=fetched_time_list,y=ce_ltp_fetched,name="LTP-Data"),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=ce_impvol_fetched,name="IV-Data"),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= ce_chng_oi_fetched,name="CHNG-OI-Data"),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=10),legend_orientation="h")
        fig.update_xaxes(title_text="Time")
        fig.update_yaxes(title_text="CHNG_OI-Data",secondary_y=False)
        fig.update_yaxes(title_text="LTP-Data",secondary_y=True)
        fig.update_yaxes(title_text="IV-Data",secondary_y=True)
        fig.layout.autosize=True
    else:
        fig=make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_ltp_fetched,name="LTP-Data"),secondary_y=False,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y=pe_impvol_fetched,name="IV-Data"),secondary_y=True,
        )
        fig.add_trace(
            pgo.Scatter(x=fetched_time_list,y= pe_chng_oi_fetched,name="CHNG-OI-Data"),secondary_y=True,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=10),legend_orientation="h")
        fig.update_xaxes(title_text="Time")
        fig.update_yaxes(title_text="CHNG_OI-Data",secondary_y=False)
        fig.update_yaxes(title_text="LTP-Data",secondary_y=True)
        fig.update_yaxes(title_text="IV-Data",secondary_y=True)
        fig.layout.autosize=True
    return fig

@app.callback(
    Output('live-update-barchart1','figure'),
    Input('interval-component', 'n_intervals')
)
def updateBarChart1(n):
    df=docLatestBankNifty()
    fig = px.bar(df, x = 'strike', y = ['ce_oi','pe_oi'])
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=10),barmode='group'),
    fig.layout.autosize=True
    return fig


@app.callback(
    Output('live-update-barchart2','figure'),
    Input('interval-component', 'n_intervals')
)
def updateBarChart2(n):
    df=docLatestNifty()
    fig = px.bar(df, x = 'strike', y = ['ce_oi','pe_oi'])
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=10),barmode='group'),
    fig.layout.autosize=True
    return fig

app.run_server()
