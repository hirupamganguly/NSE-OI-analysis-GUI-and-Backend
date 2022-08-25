import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from pytz import timezone 
from datetime import date
try:
    conn = MongoClient("mongodb://localhost:27017/")
    print("Connected successfully!!!")
except:  
    print("Could not connect to MongoDB")
# DATABSE

# {
#   "_id": {
#     "$oid": "63011f5e37c89c3154437cbc"
#   },
#   "timestamp": "2022-08-15",
#   "client_future_index_long": "251591",
#   "client_future_index_short": "210671",
#   "client_future_stock_long": "1246282",
#   "client_future_stock_short": "318002",
#   "client_option_index_call_long": "3048975",
#   "client_option_index_put_long": "2125356",
#   "client_option_index_call_short": "2843805",
#   "client_option_index_put_short": "2332376",
#   "client_option_stock_call_long": "1229748",
#   "client_option_stock_put_long": "482802",
#   "client_option_stock_call_short": "871648",
#   "client_option_stock_put_short": "539532",
#   "client_total_long_contracts": "8384753",
#   "client_total_short_contracts": "7116033",
#   "dii_future_index_long": "42529",
#   "dii_future_index_short": "68491",
#   "dii_future_stock_long": "48252",
#   "dii_future_stock_short": "1444445",
#   "dii_option_index_call_long": "719",
#   "dii_option_index_put_long": "113347",
#   "dii_option_index_call_short": "0",
#   "dii_option_index_put_short": "0",
#   "dii_option_stock_call_long": "0",
#   "dii_option_stock_put_long": "0",
#   "dii_option_stock_call_short": "92928",
#   "dii_option_stock_put_short": "0",
#   "dii_total_long_contracts": "204847",
#   "dii_total_short_contracts": "1605864",
#   "fii_future_index_long": "93581",
#   "fii_future_index_short": "99631",
#   "fii_future_stock_long": "1264544",
#   "fii_future_stock_short": "882610",
#   "fii_option_index_call_long": "371152",
#   "fii_option_index_put_long": "425975",
#   "fii_option_index_call_short": "314761",
#   "fii_option_index_put_short": "261856",
#   "fii_option_stock_call_long": "45147",
#   "fii_option_stock_put_long": "41541",
#   "fii_option_stock_call_short": "63979",
#   "fii_option_stock_put_short": "30369",
#   "fii_total_long_contracts": "2241940",
#   "fii_total_short_contracts": "1653206",
#   "pro_future_index_long": "41398",
#   "pro_future_index_short": "50306",
#   "pro_future_stock_long": "288399",
#   "pro_future_stock_short": "202420",
#   "pro_option_index_call_long": "866659",
#   "pro_option_index_put_long": "777303",
#   "pro_option_index_call_short": "1128938",
#   "pro_option_index_put_short": "847750",
#   "pro_option_stock_call_long": "370324",
#   "pro_option_stock_put_long": "389210",
#   "pro_option_stock_call_short": "616664",
#   "pro_option_stock_put_short": "343652",
#   "pro_total_long_contracts": "2733293",
#   "pro_total_short_contracts": "3189729",
#   "total_future_index_long": "429099",
#   "total_future_index_short": "429099",
#   "total_future_stock_long": "2847477",
#   "total_future_stock_short": "2847477",
#   "total_option_index_call_long": "4287503",
#   "total_option_index_put_long": "3441981",
#   "total_option_index_call_short": "4287503",
#   "total_option_index_put_short": "3441981",
#   "total_option_stock_call_long": "1645219",
#   "total_option_stock_put_long": "913553",
#   "total_option_stock_call_short": "1645219",
#   "total_option_stock_put_short": "913553",
#   "total_total_long_contracts": "13564832",
#   "total_total_short_contracts": "13564832"
# }


# ------------------------
databse = conn["NseOI"]
participantWiseCollection = databse["ParticipantWiseOI"]
def csv_to_json(filename, header=None):
    data = pd.read_csv(filename, header=header)
    data.to_dict('records')
    return data.to_dict('records')

data=csv_to_json('fao_participant_oi_19082022.csv')

headrs=[data[1][0],data[1][1],data[1][2],data[1][3],data[1][4],data[1][5],data[1][6],data[1][7],data[1][8],data[1][9],data[1][10],data[1][11],data[1][12],data[1][13],data[1][14]]
participantWiseoi={
    "timestamp":datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d'),
#client
    data[2][0].lower()+"_"+headrs[1].replace(" ", "_").replace("\t", "").lower():data[2][1],
    data[2][0].lower()+"_"+headrs[2].replace(" ", "_").replace("\t", "").lower():data[2][2],
    data[2][0].lower()+"_"+headrs[3].replace(" ", "_").replace("\t", "").lower():data[2][3],
    data[2][0].lower()+"_"+headrs[4].replace(" ", "_").replace("\t", "").lower():data[2][4],
    data[2][0].lower()+"_"+headrs[5].replace(" ", "_").replace("\t", "").lower():data[2][5],
    data[2][0].lower()+"_"+headrs[6].replace(" ", "_").replace("\t", "").lower():data[2][6],
    data[2][0].lower()+"_"+headrs[7].replace(" ", "_").replace("\t", "").lower():data[2][7],
    data[2][0].lower()+"_"+headrs[8].replace(" ", "_").replace("\t", "").lower():data[2][8],
    data[2][0].lower()+"_"+headrs[9].replace(" ", "_").replace("\t", "").lower():data[2][9],
    data[2][0].lower()+"_"+headrs[10].replace(" ", "_").replace("\t", "").lower():data[2][10],
    data[2][0].lower()+"_"+headrs[11].replace(" ", "_").replace("\t", "").lower():data[2][11],
    data[2][0].lower()+"_"+headrs[12].replace(" ", "_").replace("\t", "").lower():data[2][12],
    data[2][0].lower()+"_"+headrs[13].replace(" ", "_").replace("\t", "").lower():data[2][13],
    data[2][0].lower()+"_"+headrs[14].replace(" ", "_").replace("\t", "").lower():data[2][14],
#DII+"_".lower()
    data[3][0].lower()+"_"+headrs[1].replace(" ", "_").replace("\t", "").lower():data[3][1],
    data[3][0].lower()+"_"+headrs[2].replace(" ", "_").replace("\t", "").lower():data[3][2],
    data[3][0].lower()+"_"+headrs[3].replace(" ", "_").replace("\t", "").lower():data[3][3],
    data[3][0].lower()+"_"+headrs[4].replace(" ", "_").replace("\t", "").lower():data[3][4],
    data[3][0].lower()+"_"+headrs[5].replace(" ", "_").replace("\t", "").lower():data[3][5],
    data[3][0].lower()+"_"+headrs[6].replace(" ", "_").replace("\t", "").lower():data[3][6],
    data[3][0].lower()+"_"+headrs[7].replace(" ", "_").replace("\t", "").lower():data[3][7],
    data[3][0].lower()+"_"+headrs[8].replace(" ", "_").replace("\t", "").lower():data[3][8],
    data[3][0].lower()+"_"+headrs[9].replace(" ", "_").replace("\t", "").lower():data[3][9],
    data[3][0].lower()+"_"+headrs[10].replace(" ", "_").replace("\t", "").lower():data[3][10],
    data[3][0].lower()+"_"+headrs[11].replace(" ", "_").replace("\t", "").lower():data[3][11],
    data[3][0].lower()+"_"+headrs[12].replace(" ", "_").replace("\t", "").lower():data[3][12],
    data[3][0].lower()+"_"+headrs[13].replace(" ", "_").replace("\t", "").lower():data[3][13],
    data[3][0].lower()+"_"+headrs[14].replace(" ", "_").replace("\t", "").lower():data[3][14],
#FII+"_".lower()
    data[4][0].lower()+"_"+headrs[1].replace(" ", "_").replace("\t", "").lower():data[4][1],
    data[4][0].lower()+"_"+headrs[2].replace(" ", "_").replace("\t", "").lower():data[4][2],
    data[4][0].lower()+"_"+headrs[3].replace(" ", "_").replace("\t", "").lower():data[4][3],
    data[4][0].lower()+"_"+headrs[4].replace(" ", "_").replace("\t", "").lower():data[4][4],
    data[4][0].lower()+"_"+headrs[5].replace(" ", "_").replace("\t", "").lower():data[4][5],
    data[4][0].lower()+"_"+headrs[6].replace(" ", "_").replace("\t", "").lower():data[4][6],
    data[4][0].lower()+"_"+headrs[7].replace(" ", "_").replace("\t", "").lower():data[4][7],
    data[4][0].lower()+"_"+headrs[8].replace(" ", "_").replace("\t", "").lower():data[4][8],
    data[4][0].lower()+"_"+headrs[9].replace(" ", "_").replace("\t", "").lower():data[4][9],
    data[4][0].lower()+"_"+headrs[10].replace(" ", "_").replace("\t", "").lower():data[4][10],
    data[4][0].lower()+"_"+headrs[11].replace(" ", "_").replace("\t", "").lower():data[4][11],
    data[4][0].lower()+"_"+headrs[12].replace(" ", "_").replace("\t", "").lower():data[4][12],
    data[4][0].lower()+"_"+headrs[13].replace(" ", "_").replace("\t", "").lower():data[4][13],
    data[4][0].lower()+"_"+headrs[14].replace(" ", "_").replace("\t", "").lower():data[4][14],
#PRO+"_".lower()
    data[5][0].lower()+"_"+headrs[1].replace(" ", "_").replace("\t", "").lower():data[5][1],
    data[5][0].lower()+"_"+headrs[2].replace(" ", "_").replace("\t", "").lower():data[5][2],
    data[5][0].lower()+"_"+headrs[3].replace(" ", "_").replace("\t", "").lower():data[5][3],
    data[5][0].lower()+"_"+headrs[4].replace(" ", "_").replace("\t", "").lower():data[5][4],
    data[5][0].lower()+"_"+headrs[5].replace(" ", "_").replace("\t", "").lower():data[5][5],
    data[5][0].lower()+"_"+headrs[6].replace(" ", "_").replace("\t", "").lower():data[5][6],
    data[5][0].lower()+"_"+headrs[7].replace(" ", "_").replace("\t", "").lower():data[5][7],
    data[5][0].lower()+"_"+headrs[8].replace(" ", "_").replace("\t", "").lower():data[5][8],
    data[5][0].lower()+"_"+headrs[9].replace(" ", "_").replace("\t", "").lower():data[5][9],
    data[5][0].lower()+"_"+headrs[10].replace(" ", "_").replace("\t", "").lower():data[5][10],
    data[5][0].lower()+"_"+headrs[11].replace(" ", "_").replace("\t", "").lower():data[5][11],
    data[5][0].lower()+"_"+headrs[12].replace(" ", "_").replace("\t", "").lower():data[5][12],
    data[5][0].lower()+"_"+headrs[13].replace(" ", "_").replace("\t", "").lower():data[5][13],
    data[5][0].lower()+"_"+headrs[14].replace(" ", "_").replace("\t", "").lower():data[5][14],
#TOTAL+"_".lower()
    data[6][0].lower()+"_"+headrs[1].replace(" ", "_").replace("\t", "").lower():data[6][1],
    data[6][0].lower()+"_"+headrs[2].replace(" ", "_").replace("\t", "").lower():data[6][2],
    data[6][0].lower()+"_"+headrs[3].replace(" ", "_").replace("\t", "").lower():data[6][3],
    data[6][0].lower()+"_"+headrs[4].replace(" ", "_").replace("\t", "").lower():data[6][4],
    data[6][0].lower()+"_"+headrs[5].replace(" ", "_").replace("\t", "").lower():data[6][5],
    data[6][0].lower()+"_"+headrs[6].replace(" ", "_").replace("\t", "").lower():data[6][6],
    data[6][0].lower()+"_"+headrs[7].replace(" ", "_").replace("\t", "").lower():data[6][7],
    data[6][0].lower()+"_"+headrs[8].replace(" ", "_").replace("\t", "").lower():data[6][8],
    data[6][0].lower()+"_"+headrs[9].replace(" ", "_").replace("\t", "").lower():data[6][9],
    data[6][0].lower()+"_"+headrs[10].replace(" ", "_").replace("\t", "").lower():data[6][10],
    data[6][0].lower()+"_"+headrs[11].replace(" ", "_").replace("\t", "").lower():data[6][11],
    data[6][0].lower()+"_"+headrs[12].replace(" ", "_").replace("\t", "").lower():data[6][12],
    data[6][0].lower()+"_"+headrs[13].replace(" ", "_").replace("\t", "").lower():data[6][13],
    data[6][0].lower()+"_"+headrs[14].replace(" ", "_").replace("\t", "").lower():data[6][14],
}
participantRecordID = participantWiseCollection.insert_one(participantWiseoi)
# header = [ "Client Type", "Future Index Long", "Future Index Short","Future Stock Long","Future Stock Short","Option Index Call Long","Option Index Put Long","Option Index Call Short","Option Index Put Short","Option Stock Call Long","Option Stock Put Long","Option Stock Call Short","Option Stock Put Short"]