import numpy as np
from pymongo import MongoClient
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

client = MongoClient('localhost', 27017)

city = "ankara"
location = None
restaurant_name = None
res_speed = 5
res_service = 5
res_flavour = 5

db = client['mydb']
coll = db['db_1']
"""
    Get dataset command
"""

"""
    Database 1
"""
myquery = {}
if city != None:
    myquery['city'] = city
if location != None:
    myquery['location'] = location
if restaurant_name != None:
    myquery['restaurant_name'] = restaurant_name
if res_speed != None:
    myquery['res_speed'] = {"$gt": res_speed}
if res_service != None:
    myquery['res_service'] = {"$gt": res_service}
if res_flavour != None:
    myquery['res_flavour'] = {"$gt": res_flavour}

database_1 = coll.find(myquery)

x = 0
speed = []
service = []
flavour = []
for d in database_1:
    speed.append(d['res_speed'])
    service.append(d['res_service'])
    flavour.append(d['res_flavour'])
X = []
X.append([])
X.append([])
X.append([])
X[0].append(speed)
X[1].append(flavour)
X[2].append(service)
X = np.asarray(X).squeeze(axis=1)
X = np.transpose(X)

kmeans = KMeans(n_clusters=2, random_state=0).fit(X[:, 0:2])
y = kmeans.predict(X[:,0:2])

plt.suptitle('Speed-Flavour Restaurants', color = 'r',fontsize=16)
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='viridis')
plt.xlabel('Speed', color='b', fontsize=12)
plt.ylabel('Flavour', color='b', fontsize=12)

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)

plt.show()

kmeans = KMeans(n_clusters=2, random_state=0).fit(X[:, 1:3])
y = kmeans.predict(X[:,1:3])

plt.suptitle('Flavour-Service Restaurants', color = 'r',fontsize=16)
plt.scatter(X[:, 1], X[:, 2], c=y, s=50, cmap='viridis')
plt.xlabel('Flavour', color='b', fontsize=12)
plt.ylabel('Service', color='b', fontsize=12)

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)

plt.show()

kmeans = KMeans(n_clusters=2, random_state=0).fit(X[:,0::2])
y = kmeans.predict(X[:,0::2])

plt.suptitle('Speed-Service Restaurants', color = 'r',fontsize=16)
plt.scatter(X[:, 0], X[:, 2], c=y, s=50, cmap='viridis')
plt.xlabel('Flavour', color='b', fontsize=12)
plt.ylabel('Service', color='b', fontsize=12)

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)

plt.show()