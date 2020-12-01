from pymongo import MongoClient
import datetime
import difflib
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from dateutil import parser
from datetime import datetime, timedelta
client = MongoClient('localhost', 27017)
current_path = os.getcwd()
output_path = current_path + "\\" + ""
#x = datetime.datetime(2020, 11, 28)
db = client['mydb']
coll = db['db_1']
#python getdataset.py ankara n n 9 9 9
#python getdataset.py ankara tunalı n 5 5 5

#python city location restaurant_name speed service flavour

if len(sys.argv) != 7:
    print("Not enough input")
    exit(1)

"""
    Get dataset command
"""

"""
    Database 1
"""

myquery = {}
if sys.argv[1] != 'n':
    myquery['city'] = sys.argv[1]
if sys.argv[2]  != 'n':
    myquery['location'] = sys.argv[2]
if sys.argv[3]  != 'n':
    myquery['restaurant_name'] =sys.argv[3]
if sys.argv[4]  != 'n':
    myquery['res_speed'] = {"$gt":float(sys.argv[4])}
if sys.argv[5]  != 'n':
    myquery['res_service'] = {"$gt": float(sys.argv[5])}
if sys.argv[6]  != 'n':
    myquery['res_flavour'] = {"$gt": float(sys.argv[6])}
#myquery = {"city": city, "location": location, "res_speed": {"$gt": res_speed}, "res_service": {"$gt": res_service},"res_flavour": {"$gt": res_flavour}}

database_1 = coll.find(myquery)

restaurant_filters = database_1.distinct(('restaurant_name'))

#for x in mydoc:
  #print(x)
"""
    Database 2
"""
coll_2 = db['db_2']
coll_3 = db['db_3']
coll_4 = db['db_4']

myquery = {}
if sys.argv[1]  != 'n':
    myquery['city'] = sys.argv[1]
if sys.argv[2] != 'n':
    myquery['location'] = sys.argv[2]

myquery['restaurant_name'] = {"$in":restaurant_filters}

database_2 = coll_2.find(myquery)#Extracted corresponding values from database
database_3 = coll_3.find(myquery)
database_4 = coll_4.find(myquery)

df_1 = pd.DataFrame.from_dict(database_1)
del df_1['_id']
df_2 = pd.DataFrame.from_dict(database_2)
del df_2['_id']
df_3 = pd.DataFrame.from_dict(database_3)
del df_3['_id']
df_4 = pd.DataFrame.from_dict(database_4)
del df_4['_id']

print(df_1)
df_1.to_csv(output_path+"output_dataset\\database_1.csv", encoding='utf-8-sig')
df_2.to_csv(output_path+"output_dataset\\database_2.csv", encoding='utf-8-sig')
df_3.to_csv(output_path+"output_dataset\\"+"database_3.csv", encoding='utf-8-sig')
df_4.to_csv(output_path+"output_dataset\\"+"database_4.csv", encoding='utf-8-sig')


