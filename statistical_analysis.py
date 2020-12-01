from pymongo import MongoClient
import datetime
import difflib
import matplotlib.pyplot as plt
import numpy as np
import sys
from dateutil import parser
from datetime import datetime, timedelta
client = MongoClient('localhost', 27017)

db = client['mydb']
coll = db['db_1']
coll_2 = db['db_2']
coll_3 = db['db_3']
coll_4 = db['db_4']

"""
    Default example
"""

"""
    Default example
    python statistical_analysis.py ankara bilkent-merkez-kampüs burger-king
"""

#python
city = sys.argv[1]
location =  sys.argv[2].replace("-", " ")#"bilkent merkez kampüs"
restaurant_name = sys.argv[3].replace("-", " ")
print("Sys_1", city)
print("Sys_2", location)
print("Sys_3", restaurant_name)
#python statis
#For a chosen city,location,restaurant name give an statistics
myquery = {"city": city, "location": location, "restaurant_name": restaurant_name, "corresponding_menu": {"$ne": None}}

myset = coll_2.find(myquery)
query = {}
menu_frequency = {}
menu_flavour = {}#Menu comment rating

for x in myset:
    query['city'] = x['city']
    query['location'] = x['location']
    query['restaurant_name'] = x['restaurant_name']
    query['comments'] = x['comments']

    if x['corresponding_menu'] in menu_frequency:
        menu_frequency[x['corresponding_menu']] = menu_frequency[x['corresponding_menu']] + 1
    else:
        menu_frequency[x['corresponding_menu']] = 1

    #query
    corresponding_comments = coll_4.find(query)
    for y in corresponding_comments:
         if x['corresponding_menu'] in menu_flavour:
             menu_flavour[x['corresponding_menu']].append(y["com_flavour"])
         else:
             menu_flavour[x['corresponding_menu']] = [y["com_flavour"]]

average_flavour = {}
#Calculate average flavour
for key, value in menu_flavour.items():
    average_flavour[key] = sum(menu_flavour[key])/len(menu_flavour[key])
print("Menu Total Counts")
print("menu", menu_frequency)
print("Menu Flavour List")
print("menu", menu_flavour)
print("Menu Average List")
print("menu", average_flavour)

myquery = {"city": city, "location": location, "restaurant_name": restaurant_name}
myset = coll_4.find(myquery)
montly_data = []
montly_flavour = []
montly_speed = []
montly_service = []
for x in myset:
    month = x['com_date'].strftime("%m")
    #print("x", month)
    montly_data.append(int(month))
    montly_flavour.append(x['com_flavour'])
    montly_service.append(x['com_service'])
    montly_speed.append(x['com_speed'])

months_info = list(set(montly_data))
months_info = np.asarray(list(map(int, months_info)))
montly_flavour = np.asarray(montly_flavour)
montly_speed = np.asarray(montly_speed)
montly_service = np.asarray(montly_service)
montly_data = np.asarray(montly_data)
montly_average_flavours = []
montly_average_service = []
montly_average_speed = []

for d in months_info:
    indices = (montly_data == d)
    montly_average_flavours.append(sum(montly_flavour[indices])/montly_flavour[indices].shape[0])
    montly_average_service.append(sum(montly_service[indices]) / montly_service[indices].shape[0])
    montly_average_speed.append(sum(montly_speed[indices]) / montly_speed[indices].shape[0])

#print(coll.distinct('restaurant_name'))
#print(coll.distinct('location'))

plt.suptitle('Frequency of comments at restuarant', color = 'r',fontsize=16)
plt.xlabel('Months', color = 'b',fontsize=12)
plt.ylabel('Number of comments',color = 'b',fontsize=12)
plt.hist(montly_data)
plt.show()

plt.suptitle('Monthly Flavour Rate', color = 'r',fontsize=16)
plt.plot(months_info, montly_average_flavours)
plt.xlabel('Months', color='b', fontsize=12)
plt.ylabel('Flavour Rate', color='b', fontsize=12)
plt.show()

plt.suptitle('Monthly Service Rate', color = 'r',fontsize=16)
plt.plot(months_info, montly_average_service)
plt.xlabel('Months', color='b', fontsize=12)
plt.ylabel('Service Rate', color='b', fontsize=12)
plt.show()

plt.suptitle('Monthly Speed Rate', color = 'r',fontsize=16)
plt.plot(months_info, montly_average_speed)
plt.xlabel('Months', color='b', fontsize=12)
plt.ylabel('Speed Rate', color='b', fontsize=12)
plt.show()