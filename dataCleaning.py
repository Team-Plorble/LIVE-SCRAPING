#!/usr/bin/env python
# coding: utf-8

# In[5]:


import re
import os
from bs4 import BeautifulSoup


# In[103]:


def get_file_paths(folder_name):
    dir_path = folder_name + '/'
    dir_files = []
    # Iterate directory
    if os.path.exists(dir_path):
        for file in os.listdir(dir_path):
            if ".txt" in file:
                dir_files.append(dir_path+file)
    return sorted(dir_files)


# In[104]:


def contains_only_english(my_string):
    """
    Check if the string contains only English letters or all English punctuations.
    """
    import string
    english_set = set(string.ascii_letters + string.punctuation + string.digits + string.whitespace)
    status = all(c in english_set for c in my_string)
    return status


# In[105]:


def get_lyrics(dir_files):
    data_dict = {}
    for filepath in dir_files:
        with open(filepath, 'r',encoding='utf-8') as f:
            lines = f.read()
            soup = BeautifulSoup(lines, 'html.parser')
            div_lyric = soup.find('div', id='lyric-content')
            try:
                code = div_lyric.prettify()
                lyrics = re.findall('^(?! *<).*', code, re.MULTILINE)
                lyrics = [lyric.lstrip() for lyric in lyrics if lyric and contains_only_english(lyric)]
                if lyrics:
                    title = soup.find('div', attrs={'class': 'tit'}).text
                    p_element = soup.select_one('div.cnt p:contains("歌手：")')

                    a_elements = p_element.find_all('a')

                    artists = [a.text for a in a_elements]

                    artist = artists[0]
                    feature = artists[1:]
                    year = 2023
                    song_id = re.findall(r"(?<=id)[0-9]+", filepath)[0]

                    data_dict[song_id] = [title, artist, feature, year, lyrics]
            except:
                pass
    return data_dict

if __name__ == '__main__':
    dir_files = get_file_paths('2023-03-03')
    test_dict = get_lyrics(dir_files)


# In[106]:


# In[ ]:




