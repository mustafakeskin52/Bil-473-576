import json
from pymongo import MongoClient
from datetime import datetime, timedelta
import numpy as np
import os

path = os.getcwd()

with open(path +"\\save_ankara.txt", "r") as fp:
    city_objects = json.load(fp)

[names, locations, speed, service, flavour, all_restaurant_menu, all_comments] = city_objects

for i in range(len(locations)):
    locations[i] = locations[i].strip().lower()

for i in range(len(names)):
    names[i] = names[i].strip().lower()

different_locations = list(set(locations))
price_list = []
menu_list = []
for i in range(len(all_restaurant_menu)):
    price_list.append([])
    menu_list.append([])
    price_list[i].append(all_restaurant_menu[i][1::2])
    menu_list[i].append(all_restaurant_menu[i][::2])

"""
    Comments database
"""
comments = []
comments_rate = []
comments_date = []

for i in range(len(all_comments)):
    comments_rate.append([])
    comments_date.append([])
    comments.append([])
    for j in range(len(all_comments[i])):
        if all_comments[i][j].find("Hız") >= 0 and all_comments[i][j].find("| Servis: ") >= 0 :

            if (all_comments[i][j-1].find("gün") >= 0 or all_comments[i][j-1].find("ay") >= 0) and all_comments[i][j-1].find(
                "önce") >= 0:
                comments[i].append([])
            else:
                comments[i].append(all_comments[i][j - 1])
            comments_rate[i].append(all_comments[i][j])
            comments_date[i].append(all_comments[i][j+1])


#Creating a pymongo client
client = MongoClient('localhost', 27017)

#Getting the database instance
db = client['mydb']

#Creating a collection
coll = db['db_1']
city = "ankara"
#Inserting document into a collection
#[names, locations, speed, service, flavour, all_restaurant_menu, all_comments]
for i in range(len(names)):
     speed[i] = speed[i].replace(',', '.')
     service[i] = service[i].replace(',', '.')
     flavour[i] = flavour[i].replace(',', '.')

     if speed[i] == '-':
         speed[i] = 0
     if service[i] == '-':
         service[i] = 0
     if flavour[i] == '-':
         flavour[i] = 0

     doc1 = {"city": "ankara", "location": locations[i], "restaurant_name": names[i],"res_speed": float(speed[i]),"res_service":float(service[i]),"res_flavour": float(flavour[i])}

     coll.insert_one(doc1)

coll = db['db_2']

for i in range(len(names)):
    for j in range(len(comments[i])):
         doc1 = {"city":city, "location": locations[i],"restaurant_name": names[i], "comments": comments[i][j],"corresponding_menu": None}
         coll.insert_one(doc1)

coll = db['db_3']

#city restaurant menu price
for i in range(len(names)):
    for j in range(len(menu_list[i][0])):
         if menu_list[i][0][j].find('(Kampanya koşulları için restoranın Promosyonlar bölümüne göz atınız.') >= 0:
             menu_list[i][0][j] = menu_list[i][0][j].replace('(Kampanya koşulları için restoranın Promosyonlar bölümüne göz atınız. İndirimli fiyat ürün sepete eklendikten sonra uygulanır.)','')
         if  menu_list[i][0][j].find('Şu anda mevcut değil') >= 0:
             menu_list[i][0][j] = menu_list[i][0][j].replace('Şu anda mevcut değil', '')
         doc1 = {"city": city, "location": locations[i], "restaurant_name": names[i], "menu": menu_list[i][0][j],"price": price_list[i][0][j]}
         coll.insert_one(doc1)

coll = db['db_4']
for i in range(len(names)):
    for j in range(len(comments[i])):
         speed = float(comments_rate[i][j].split('|')[0].split(':')[1].strip())
         service = float(comments_rate[i][j].split('|')[1].split(':')[1].strip())
         flavour = float(comments_rate[i][j].split('|')[2].split(':')[1].strip())
         time = comments_date[i][j].split('önce')[0]

         if time.find('gün') >= 0:
            if time.find('bugün') >= 0:
                amount = 1
            else:
                amount = int(time.split('gün')[0])
            d = datetime.today() - timedelta(days=1*amount)

            #print("", d)
         elif time.find('ay') >= 0:
            if time.find('bu') >= 0:
                amount = 1
            else:
                amount = int(time.split('ay')[0])
            d = datetime.today() - timedelta(days=1 * amount*30)

         doc1 = {"city": city, "location": locations[i], "restaurant_name": names[i], "comments": comments[i][j],"com_speed":speed,
                "com_service":service, "com_flavour": flavour, "com_date":d}
         coll.insert_one(doc1)
#coll.insert_one(doc1)
#print(coll.find_one())
