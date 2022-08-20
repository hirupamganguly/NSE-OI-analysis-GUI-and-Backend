import pandas as pd
from pymongo import MongoClient

def csv_to_json(filename, header=None):
    data = pd.read_csv(filename, header=header)
    data.to_dict('records')
    return data.to_dict('records')

data=csv_to_json('fao_participant_oi_19082022.csv')
print(data[1:])

# header = [ "Client Type", "Future Index Long", "Future Index Short","Future Stock Long","Future Stock Short","Option Index Call Long","Option Index Put Long","Option Index Call Short","Option Index Put Short","Option Stock Call Long","Option Stock Put Long","Option Stock Call Short","Option Stock Put Short"]