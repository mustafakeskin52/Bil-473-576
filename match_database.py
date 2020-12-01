from pymongo import MongoClient
import datetime
import difflib

client = MongoClient('localhost', 27017)
#x = datetime.datetime(2020, 11, 28)
db = client['mydb']

city = "ankara"

"""
    Get dataset command
"""
coll_2 = db['db_2']

restaurants = coll_2.distinct('restaurant_name')
locations = coll_2.distinct('location')

coll_3 = db['db_3']

myquery = {"corresponding_menu": {"$ne":None}}
mydoc = coll_2.find(myquery)

for i in range(len(restaurants)):
    print("Percent", i/len(restaurants))
    for j in range(len(locations)):
       query =  {"city": city, "restaurant_name": restaurants[i], "location": locations[j]}
       comments = coll_2.find(query)
       menu = coll_3.find(query).distinct('menu')
       if menu != [] and comments != []:
         for comment in comments:
           if comment['comments'] != []:
             is_existed = False
             for m in menu:
                if is_existed == False:
                    menu_part = m.split(" ")
                    for finding_ing in menu_part:
                      sub_parts = comment['comments'].split()
                      found_part = difflib.get_close_matches(finding_ing, sub_parts, cutoff=1)
                      if len(found_part) > 0:
                        is_existed = True
                        query = {"city": city, "restaurant_name": restaurants[i], "location": locations[j], "comments": comment['comments']}
                        updated_query = {"$set": {"city": city, "restaurant_name": restaurants[i], "location": locations[j],  "comments": comment['comments'], "corresponding_menu": m}}
                        coll_2.update_one(query, updated_query)
                        break
                else:
                    break
              #difflib.get_close_matches(m, comment['comments'], n = 4,cutoff = 0.3)

