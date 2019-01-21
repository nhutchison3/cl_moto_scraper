from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import urllib.request

import pandas as pd
import numpy as np

class CraigslistScraper(object):
    def __init__(self, location, postal, min_price, max_price, radius):
        self.location = location
        self.postal = postal
        self.min_price = min_price
        self.max_price = max_price
        self.radius = radius
        self.url = f"http://{location}.craigslist.org/search/mca?search_distance={radius}&postal={postal}&min_price={min_price}&max_price={max_price}"

        self.driver = webdriver.Firefox()
        self.delay = 3

    def load_craigslist_url(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.ID, "searchform")))
            print ("Page is ready")
        except TimeoutException:
            print("Loading took too much time")

    def extract_post_information(self):

        self.titles = []
        self.prices = []
        self.dates = []
       
        all_posts = self.driver.find_elements_by_class_name("result-row")
        #you could change to other thing to find instead of name from http
        self.post_title_list = []
        for post in all_posts:
            title = post.text.split('$')
            if title[0] == '':
                title = title[1]
            else:
                title = title[0]
            title = title.split("\n")
            price = title[0]
            title = title[-1]
            title = title.split(" ")
            month = title[0]
            day = title[1]
            date = month + " " + day
            title = ' '.join(title[2:])
            print("POST DATE: " + date)
            print("TITLE: " + title)
            print("$" + price)

            self.titles.append(title)
            self.prices.append(price)
            self.dates.append(date)
           
            self.post_title_list.append(post.text)
        return self.post_title_list
        print(self.post_title_list)
        #you could change to other thing to find instead of name from http


    def extract_post_urls(self):
        self.url_list = []
        #self.hyperlink_friendly = []
        html_page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(html_page, "html.parser")
        for link in soup.findAll("a",{"class": "result-title hdrlnk"}):
            self.url_list.append(link["href"])
        return self.url_list

    def create_pivot(self):
        d = {'Titles' : self.post_title_list, 'URL' : self.url_list}
        df = pd.DataFrame(data=d)
        print(df)
        df.to_csv('posts_of_interest.csv')
       

    def quit(self):
        self.driver.close()


#location = input("What city are you searching in?")
#postal = input("Please enter zip code")
#min_price = input("Enter minimum price")
#max_price = input("Enter max price")
#radius = input("How far are you willing to drive? Must be less than 200 miles. Do not include units.")

location = "Atlanta"
postal = "30306"
min_price = "1000"
max_price = "1500"
radius = "10"
#this is to expedite testing, can switch to tagged out "custom" parameters if desired.

scraper = CraigslistScraper(location, postal, min_price, max_price, radius)
scraper.load_craigslist_url()
scraper.extract_post_information()
scraper.extract_post_urls()
scraper.create_pivot()
scraper.quit()
	
	
	
