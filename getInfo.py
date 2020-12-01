import time
import json
import pickle
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
#https://www.yemeksepeti.com/arbys-macunkoy-podium-ankara
#https://www.yemeksepeti.com/basak-doner-mamak-ekin-mah-ankara

path = "F:\\Mert\\HW\\ankara"
locations = []
speed = []
flavor = []
service = []
names = []
menu = []
comments = []
j = 0
k = 0
#Komagene Etsiz Çiğ Köfte, Yenimahalle (Demetgül Mah.)
for i in range(0, 3136):
    objects = []
    try:
        with open(path + "\\" + str(i) + "\\save_objects.txt", "r") as fp:
            objects = json.load(fp)
    except:
            j = j + 1
    if objects != [] and len(objects[1]) != 0:
        locations.append(objects[0].split(",")[1].split("(")[0])
        names.append(objects[0].split(",")[0])
        # print("loc",objects[0].split(",")[1].split("(")[0])
        speed.append(objects[1].splitlines()[1])
        service.append(objects[2].splitlines()[1])
        flavor.append(objects[3].splitlines()[1])
        menu.append(objects[4])
        comments.append(objects[5])

def extract_menus_prices(menu):
    all_restaurant_menu = []
    for i in range(len(menu)):#Restaurants
        all_restaurant_menu.append([])
        for j in range(len(menu[i])):#menu 1.2...i
            for k in range(len(menu[i][j].splitlines())):#
               string = menu[i][j].splitlines()[k]
               if string.find("TL") >= 0 and len(string) <= 10:
                  #İçecekler,Yan Ürünler,Salatalar,Tatlılar
                  filters = ["İçecekler","Yan Ürünler","Salatalar","Tatlılar","Poşet","Dondurmalar","Börekler",
                             "Ürünler","Kadayıflar","Kurabiyeler","Kuru Pastalar","Yemekler","Atıştırmalıklar","Tostlar","Kahveler"]
                  if menu[i][j].splitlines()[k - 2].find("TL") < 0:
                      isadd = False
                      for m in range(len(filters)):
                          if menu[i][j].splitlines()[k - 2].find(filters[m]) >= 0:#one previous
                             # print("Menu", menu[i][j].splitlines()[k - 2])
                              all_restaurant_menu[i].append(menu[i][j].splitlines()[k-1])#menu
                              all_restaurant_menu[i].append(menu[i][j].splitlines()[k])#price
                              isadd = True
                              break;
                      if isadd == False:#Two previous case
                          all_restaurant_menu[i].append(menu[i][j].splitlines()[k - 2])  # menu
                          all_restaurant_menu[i].append(menu[i][j].splitlines()[k])  # price
                  else:
                      all_restaurant_menu[i].append(menu[i][j].splitlines()[k - 1])  # menu
                      all_restaurant_menu[i].append(menu[i][j].splitlines()[k])  # price
    return all_restaurant_menu
            #all_restaurant_menu.append()
#def extract_comments(comments):
#print("Location", locations[0])
def extract_comments(comments):
    all_comments = []
    for i in range(len(comments)):
        all_comments.append([])
        for j in range(len(comments[i])):#Page number
            comments_page = comments[i][j].splitlines()

            for k in range(len(comments_page)):
                if comments_page[k].find("...") >= 0 and len(comments_page[k]) < 5 and k+1 < len(comments_page):
                    all_comments[i].append(comments_page[k + 1])#comments
                    all_comments[i].append(comments_page[k - 2])#rates
                    all_comments[i].append(comments_page[k - 1])#date

    return all_comments

all_restaurant_menu = extract_menus_prices(menu)
all_comments = extract_comments(comments)

city_objects = [names, locations, speed, service, flavor, all_restaurant_menu,all_comments]
with open("F:\\Mert\\HW\\save_ankara.txt", "w") as fp:
    json.dump(city_objects, fp)
#print(len(all_comments[3])/3)
#print(len(names))
#print("menu",menu[80][2])
#print("locations",len(locations))
#print("all_comments",len(all_comments))
#print("menu",len(all_restaurant_menu))
#print("menu",speed)
#print("comments",comments[1])
#print("", j)
#print("objects", objects[0])

#print("objects", objects[2])
#print("objects", objects[3])
#print("objects",objects[4])
#print("objects",objects[4][5][:])
#print("objects",objects[4][0])
#//*[@id="restaurant_menu"]/div[1]/div[2]/ul/li[1]