#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from lxml import etree
from bs4 import BeautifulSoup
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import queue
import os
import threading
import random
import datetime
import dataCleaning
import crawl
import sys
from tqdm import tqdm
import writeFiles
import dataCleaning
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from apscheduler.schedulers.blocking import BlockingScheduler


# In[ ]:


def job():
    
    chromedriverpath=r'C:\Users\Administrator\.cache\selenium\chromedriver\win32\109.0.5414.74\chromedriver.exe'
    
    print("Code running every day")
    my_date = crawl.get_date()
    links = crawl.get_links(my_date, chromedriverpath)
    with tqdm(total=len(links)) as pbar:
        crawl.scrape_urls(links, pbar, chromedriverpath)
    my_date_string = my_date.strftime('%Y-%m-%d')
    dir_files = dataCleaning.get_file_paths(my_date_string)
    if not dir_files:
        print(f'\033[1;31mNo album is updated today, today is {my_date_string}\033[0m')
    else:
        print(f'\033[1;32mAlbum updated today, today is {my_date_string}\033[0m')
    data_dict = dataCleaning.get_lyrics(dir_files)
    writeFiles.writeCSV(my_date, data_dict)
    
try: 
    scheduler = BlockingScheduler()

    scheduler.add_job(job, 'cron', hour=17, minute=0)

    scheduler.start()
except:
    scheduler.shutdown(wait=False)
