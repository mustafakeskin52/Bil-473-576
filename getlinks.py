import pandas as pd
from selenium import webdriver
import time
import json

# start web browser1
browser = webdriver.Chrome(executable_path="C:\\Users\\Hasan\\Desktop\\chromedriver.exe")

# get source code
browser.get("https://www.yemeksepeti.com/istanbul/restoran-arama")

SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")
link_list = []

while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    elems = browser.find_elements_by_xpath("//a[@href]")

    for elem in elems:
        link_list.append(elem.get_attribute("href"))
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")

    with open("link_list.txt", "w") as fp:
        json.dump(link_list, fp)

    if new_height == last_height:
        break
    last_height = new_height


# close web browser

browser.close()