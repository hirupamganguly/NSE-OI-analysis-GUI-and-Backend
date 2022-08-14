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
import plotly.express as px
import dash_bootstrap_components as dbc
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
bnfOne=bankNiftyCollection.find_one()
bankNiftyAtmStrike= round(int(bnfOne["underlyingValue"])/100)*100

nfOne=niftyCollection.find_one()
niftyAtmStrike= round(int(nfOne["underlyingValue"])/50)*50



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
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": ".05rem .05rem",
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
app.layout=dhtml.Div(
    [   dbc.Row([
            dcc.DatePickerSingle(
            id='which-date-oi',
            style=DateStyle,
            min_date_allowed=date(int(dateArr[0]),int(dateArr[1])-6,int(dateArr[2])),
            max_date_allowed=date(int(dateArr[0]),int(dateArr[1]),int(dateArr[2])),
            initial_visible_month=date(int(dateArr[0]),int(dateArr[1]),int(dateArr[2])),
            date=date(int(dateArr[0]),int(dateArr[1]),int(dateArr[2])),
        ),
    ]),
        
        dbc.Row(
            [
                dbc.Col(dhtml.Div([
                    dcc.Dropdown(
                        id='dropdownstrike',
                        style=ColumnStyle,
                        options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                        value=str(bankNiftyAtmStrike),
                    ),
                    dcc.Graph(id="live-update-graph",animate=True)]),style=ColumnStyle,),
                dbc.Col(dhtml.Div(
                    [
                        dcc.Dropdown(
                            id='dropdownstrike1',
                            style=ColumnStyle,
                            options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                            value=str(bankNiftyAtmStrike),
                        ),
                        dcc.Graph(id="live-update-graph1",animate=True),]),style=ColumnStyle,),
                dbc.Col(dhtml.Div( [
                        dcc.Dropdown(
                            id='dropdownstrike2',
                            style=ColumnStyle,
                            options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                            value=str(bankNiftyAtmStrike),
                        ),
                        dcc.Graph(id="live-update-graph2",animate=True),
                    ]),style=ColumnStyle,),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dhtml.Div( [
                        dcc.Dropdown(
                            id='dropdownstrike3',
                            style=ColumnStyle,
                            options=[{"label":str(i),"value":str(i)} for i in range(niftyAtmStrike-500,niftyAtmStrike+500,50)],
                            value=str(niftyAtmStrike),
                        ),
                        dcc.Graph(id="live-update-graph3",animate=True),
                    ]),style=ColumnStyle,),
                dbc.Col(dhtml.Div( [
                        dcc.Dropdown(
                            id='dropdownstrike4',
                            style=ColumnStyle,
                            options=[{"label":str(i),"value":str(i)} for i in range(niftyAtmStrike-500,niftyAtmStrike+500,50)],
                            value=str(niftyAtmStrike),
                        ),
                        dcc.Graph(id="live-update-graph4",animate=True),
                    ]),style=ColumnStyle,),
                dbc.Col(dhtml.Div( [
                        dcc.Dropdown(
                            id='dropdownstrike5',
                            style=ColumnStyle,
                            options=[{"label":str(i),"value":str(i)} for i in range(niftyAtmStrike-500,niftyAtmStrike+500,50)],
                            value=str(niftyAtmStrike),
                        ),
                        dcc.Graph(id="live-update-graph5",animate=True),
                    ]),style=ColumnStyle,),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dhtml.Div( [
                        dcc.Dropdown(
                            id='dropdownstrike6',
                            style=ColumnStyle,
                            options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                            value=str(bankNiftyAtmStrike),
                        ),
                        dcc.Graph(id="live-update-graph6",animate=True),
                    ]),style=ColumnStyle,),
                dbc.Col(dhtml.Div( [
                        dcc.Dropdown(
                            id='dropdownstrike7',
                            style=ColumnStyle,
                            options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                            value=str(bankNiftyAtmStrike),
                        ),
                        dcc.Graph(id="live-update-graph7",animate=True),
                    ]),style=ColumnStyle,),
                dbc.Col(dhtml.Div( [
                        dcc.Dropdown(
                            id='dropdownstrike8',
                            style=ColumnStyle,
                            options=[{"label":str(i),"value":str(i)} for i in range(bankNiftyAtmStrike-1000,bankNiftyAtmStrike+1000,100)],
                            value=str(bankNiftyAtmStrike),
                        ),
                        dcc.Graph(id="live-update-graph8",animate=True),
                    ]),style=ColumnStyle,),
            ]
        ),
        dcc.Interval(
            id="interval-component",interval=100*1000,n_intervals=0
        ),
    ]
)

@app.callback(
    Output('live-update-graph','figure'),
    Input('which-date-oi','date'),
    Input('dropdownstrike','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph(date_value,strikeValue,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
    fig=px.line(x=fetched_time_list,y=ce_oi_fetched,markers=True,labels=dict(x="Time", y="OI",))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=10),)
    fig.layout.autosize=True
    return fig



@app.callback(
    Output('live-update-graph1','figure'),
    Input('which-date-oi','date'),
    Input('dropdownstrike1','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph1(date_value,strikeValue,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
   
    fig=px.line(x=fetched_time_list,y=ce_oi_fetched,markers=True,labels=dict(x="Time", y="OI",))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=10),)
    fig.layout.autosize=True
    return fig


@app.callback(
    Output('live-update-graph2','figure'),
    Input('which-date-oi','date'),
    Input('dropdownstrike2','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
   
    fig=px.line(x=fetched_time_list,y=ce_oi_fetched,markers=True, labels=dict(x="Time", y="OI",))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=10),)
    fig.layout.autosize=True
    return fig



@app.callback(
    Output('live-update-graph3','figure'),
    Input('which-date-oi','date'),
    Input('dropdownstrike3','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateNifty(int(strikeValue),date_string)
   
    fig=px.line(x=fetched_time_list,y=ce_oi_fetched,markers=True, labels=dict(x="Time", y="OI",))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=10),)
    fig.layout.autosize=True
    return fig



@app.callback(
    Output('live-update-graph4','figure'),
    Input('which-date-oi','date'),
    Input('dropdownstrike4','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateNifty(int(strikeValue),date_string)
   
    fig=px.line(x=fetched_time_list,y=ce_oi_fetched,markers=True, labels=dict(x="Time", y="OI",))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=10),)
    fig.layout.autosize=True
    return fig


@app.callback(
    Output('live-update-graph5','figure'),
    Input('which-date-oi','date'),
    Input('dropdownstrike5','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateNifty(int(strikeValue),date_string)
   
    fig=px.line(x=fetched_time_list,y=ce_oi_fetched,markers=True, labels=dict(x="Time", y="OI",))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=10),)
    fig.layout.autosize=True
    return fig


@app.callback(
    Output('live-update-graph6','figure'),
    Input('which-date-oi','date'),
    Input('dropdownstrike6','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
   
    fig=px.line(x=fetched_time_list,y=ce_oi_fetched,markers=True, labels=dict(x="Time", y="OI",))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=10),)
    fig.layout.autosize=True
    return fig


@app.callback(
    Output('live-update-graph7','figure'),
    Input('which-date-oi','date'),
    Input('dropdownstrike7','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
   
    fig=px.line(x=fetched_time_list,y=ce_oi_fetched,markers=True, labels=dict(x="Time", y="OI",))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=10),)
    fig.layout.autosize=True
    return fig


@app.callback(
    Output('live-update-graph8','figure'),
    Input('which-date-oi','date'),
    Input('dropdownstrike8','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
   
    fig=px.line(x=fetched_time_list,y=ce_oi_fetched,markers=True, labels=dict(x="Time", y="OI",))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=10),)
    fig.layout.autosize=True
    return fig


@app.callback(
    Output('live-update-graph9','figure'),
    Input('which-date-oi','date'),
    Input('dropdownstrike9','value'),
    Input('interval-component','n_intervals')
)
def update_strike_graph2(date_value,strikeValue,n):
    date_string=""
    if date_value is not None:
        date_obj=date.fromisoformat(date_value)
        date_string=date_obj.strftime('%Y-%m-%d')
    ce_oi_fetched,ce_chng_oi_fetched,ce_impvol_fetched,ce_ltp_fetched,pe_oi_fetched,pe_chng_oi_fetched,pe_impvol_fetched,pe_ltp_fetched,fetched_time_list=docBystrikeAndDateBanknifty(int(strikeValue),date_string)
   
    fig=px.line(x=fetched_time_list,y=ce_oi_fetched,markers=True, labels=dict(x="Time", y="OI",))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=10),)
    fig.layout.autosize=True
    return fig

app.run_server()
