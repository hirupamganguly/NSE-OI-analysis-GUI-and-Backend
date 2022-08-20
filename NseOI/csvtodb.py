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