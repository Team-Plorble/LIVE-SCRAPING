#!/usr/bin/env python
# coding: utf-8

# In[4]:


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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import csv


# In[10]:


def writeCSV(date, data_dict):
    # Creating CSV File
    # Define the header row
    date_str = date.strftime('%Y-%m-%d')
    if data_dict:
        with open(date_str+'.csv', 'a', newline='', encoding='utf-8') as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(['title','tag', 'artist', 'year', 'views', 'features', 'lyrics', 'id'])

            for song_id, data in data_dict.items():
                title = data[0]
                artist = data[1]
                features = ', '.join(data[2])
                year = data[3]
                lyrics = ',\n'.join(data[4])  # Add comma and new line character
                writer.writerow([title, '', artist, year, '', '', lyrics, ''])


if __name__ == '__main__':
    writeCSV(my_date, data_dict)


# In[ ]:




