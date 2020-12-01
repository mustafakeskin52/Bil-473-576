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
import os
from bs4 import BeautifulSoup
path = "C:\\Users\\Hasan\\Desktop\\chromedriver.exe"
# get source code
def get_restaurant(browser, link_name):
    i = 1
    previous_url = browser.current_url
    comments_list = []

    browser.get(link_name)
    tag = '/html/body/div[2]/div/span[2]'
    """
        Restaurant Names
    """
    restaurant_name = browser.find_element_by_xpath(tag)
    location = restaurant_name.text
    print("location", location)
    """
        Rates 
    """
    speed_tag = '//*[@id="restaurantDetail"]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]'
    restaurant_rank_speed = browser.find_element_by_xpath(speed_tag)
    speed = restaurant_rank_speed.text

    service_tag = '//*[@id="restaurantDetail"]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]'
    restaurant_rank_service = browser.find_element_by_xpath(service_tag)

    service = restaurant_rank_service.text


    flavor_tag = '//*[@id="restaurantDetail"]/div[1]/div/div[2]/div[2]/div[1]/div/div[3]'
    restaurant_rank_flavor_tag = browser.find_element_by_xpath(flavor_tag)

    flavor = restaurant_rank_flavor_tag.text


    """
        Menu and prices 
    """
    all_menu_list = []
    k = 0
    while True:
        #NEXT_BUTTON_XPATH = '//*[@id="menu_0"]'

        try:
            NEXT_BUTTON_XPATH = '//*[@id="menu_' + str(k) + '"]'
            print("", NEXT_BUTTON_XPATH)
            menu = browser.find_element_by_xpath(NEXT_BUTTON_XPATH)

            k = k + 1
            all_menu_list.append(menu.text)
        except:
                break
    """
        Comments 
    """
    all_comments_list = []
    i = 1
    while True:

        browser.get(link_name + '?section=comments&page='+str(i))
        currentURL = browser.current_url
        print("",currentURL)
        if previous_url == currentURL:
            break

        previous_url = currentURL

        i = i + 1

        NEXT_BUTTON_XPATH = '//*[@id="restaurant_comments"]/div[4]'
        comments = browser.find_element_by_xpath(NEXT_BUTTON_XPATH)

        all_comments_list.append(comments.text)
    #print("comments_list",comments_list)

    return location, speed, service, flavor, all_menu_list, all_comments_list
    #2 11 12 13 14 15 19 26 29 39

with open("link_list.txt", "r") as fp:
    b = json.load(fp)
#print("b",len(b))

myset = list(set(b))

with open("link_list_set.txt", "w") as fp:
    json.dump(myset,fp)
with open("link_list_set.txt", "r") as fp:
    myset = json.load(fp)
#print("",myset[2])
browser = webdriver.Chrome(executable_path=path)
#link_name = myset[2]
#location, speed, service, flavor, all_menu_list, comments_list_full = get_restaurant(browser, "https://www.yemeksepeti.com/acil-yesim-express-emek-ankara")
#print("comment_list",comments_list_full)
#print("location",location)
#print("speed",speed)
#print("service",service)
#print("flavor",flavor)
#print("all_menu_list",all_menu_list)


path = "F:\\Mert\\HW\\data"
#link_name = 'https://www.yemeksepeti.com/paksu-corba-doner-kecioren-yukseltepe-mah-ankara'
for i in range(0, len(myset)):

    print("i",i)

    link_name = myset[i]
    print("",link_name)
    try:
        location, speed, service, flavor, all_menu_list, comments_list_full = get_restaurant(browser, link_name)
        save_objects = [location, speed, service, flavor, all_menu_list, comments_list_full]
        try:
            os.makedirs(path+"\\"+str(i))
            with open(path+"\\"+str(i)+"\\save_objects.txt", "w") as fp:
                json.dump(save_objects, fp)
        except:
            print("full")
    except:
        print("pass")


