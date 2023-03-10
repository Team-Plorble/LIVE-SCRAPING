#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from lxml import etree
from bs4 import BeautifulSoup
import json
import re
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import queue
import os
import threading
import random
import datetime
import apscheduler
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException


# In[2]:


def get_date():
    today = datetime.date.today()
    return today
# test only
if __name__ == '__main__':
    today = get_date()
    print(today, type(today))


# In[3]:


def get_links(date, chromedriverpath):
    count = 0
    page_index = 1
    LINKS = []
    DATE_status = False
    url = 'https://music.163.com/#/discover/album/m/?area=EA&index='
    while not DATE_status:
        try:
            while count < 1:
                try:
                    chrome_options= webdriver.ChromeOptions()
                    chrome_options.add_argument('--headless')
                    chrome_options.add_argument('--disable-gpu')
                    # driver = webdriver.Chrome(options=chrome_options)
                    driver = webdriver.Chrome(chromedriverpath,options=chrome_options)
                    driver.get(url+str(page_index))
                    print(f'driver gets {url+str(page_index)}')
                    driver.switch_to.frame("g_iframe")
                    time.sleep(random.uniform(3,5))                    
                    
                    # Find the links of albums
                    links = driver.find_elements(By.XPATH, '//a[contains(@href, "/album?id=")]')
                    # Remove duplicate links
                    links = [link for link in links if link.text]
                    # Remove the first ten links because they are recommended albums, not the newest albums
                    links = links[10:]
                    # Get the links of albums
                    links = [link.get_attribute('href') for link in links]
                    LINKS += links
                    # print(links)
                    # Check whether the last album is released before the date
                    driver.get(links[-1])
                    driver.switch_to.frame("g_iframe")
                    intr_eles = driver.find_elements(By.XPATH,"//p[@class='intr']")
                    for sth in intr_eles:
                        if '发行时间：' in sth.text:
                            mystr = sth.text
                            album_date = mystr.replace('发行时间：', '')

                    # print(album_date)
                    mydate = datetime.datetime.strptime(album_date, '%Y-%m-%d').date()
                    # print(mydate)
                    driver.quit()
                    print(f'driver finished getting {url+str(page_index)}')

                    if mydate < date:
                        DATE_status = True
                    elif page_index == 15:
                        DATE_status = True

                    page_index += 1

                    break
                except:
                    count += 1
        except:
            break
    
    return LINKS

# if __name__ == '__main__':
#     date_string = '2023-03-03'
#     date = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
#     LINKS = get_links(date)
#     print(LINKS)


# In[4]:

# def scrape_urls(link_list):
def scrape_urls(link_list, pbar, chromedriverpath):
    # define the number of threads to use
    num_threads = 18

    url_queue = queue.Queue()
    for link in link_list:
        url_queue.put(link)

    def worker():
        # loop over URLs in the queue and scrape each one
        while not url_queue.empty():
            url = url_queue.get()
            # print(f'Scraping {url}...')
            long_running_scraping_job(url, chromedriverpath)
            # print(f'Finished scraping {url}...')
            url_queue.task_done()
            pbar.update(1)

    # create and start the threads
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    # wait for all URLs to be scraped
    url_queue.join()

    # wait for all threads to finish
    for thread in threads:
        thread.join()

    print('All URLs have been scraped.')


# In[1]:


def long_running_scraping_job(url, chromedriverpath):
    # Scrape the website here
    count = 0
    while count < 3:
        try:
            chrome_options= webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            # driver = webdriver.Chrome(options=chrome_options)
            driver = webdriver.Chrome(chromedriverpath, options=chrome_options)
            time.sleep(random.uniform(1,3))
            driver.get(url)
            driver.switch_to.frame("g_iframe")
            data = driver.page_source

            intr_eles = driver.find_elements(By.XPATH,"//p[@class='intr']")
            for sth in intr_eles:
                if '发行时间：' in sth.text:
                    mystr = sth.text
                    album_date = mystr.replace('发行时间：', '')

            #click the song page
            num_links = len(driver.find_elements(By.XPATH, '//a[contains(@href, "/song?id")]'))


            for ind in range(num_links):
                links = driver.find_elements(By.XPATH, '//a[contains(@href, "/song?id")]')
                link = links[ind]

                song_id_link = link.get_attribute('href')
                song_id = re.findall(r"(?<=id=)[0-9]+", song_id_link)
                # print(song_id[0])
                time.sleep(random.uniform(3,5))
                driver.execute_script("arguments[0].click();", link)
                data = driver.page_source

                # save the results to a file or database
                if not os.path.exists(album_date):
                    os.mkdir(album_date)
                with open(album_date+'/id'+song_id[0]+'-page_source'+'.txt', 'w', encoding='utf-8') as fp:
                    fp.write(str(data))
                time.sleep(random.uniform(1,8))
                driver.back()
                driver.refresh()
                driver.switch_to.frame("g_iframe")
        #     time.sleep(5)
            driver.quit()
            # print('page source written in the file')
            break

        except KeyboardInterrupt:
            driver.quit()
            count = 10
            
        except:
            driver.quit()
            count += 1
# if __name__ == '__main__':
#     print(LINKS[0])
#     url=LINKS[0]
#     long_running_scraping_job(url)


# In[6]:


def crawler():
    date = get_date()
    links = get_links(date)
    scrape_website(links)


# In[7]:


if __name__ == '__main__':
    date_string = '2023-02-22'
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    links = get_links(date)
    scrape_urls(links)


# In[ ]:




