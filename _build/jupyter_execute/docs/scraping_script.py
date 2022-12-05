#!/usr/bin/env python
# coding: utf-8

# ## Web Scraping Review Data From Trip Advisor For Oberoi Delhi

# In[16]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


# In[2]:


# Set up requests for trip advisor
headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en,mr;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

url = "https://www.tripadvisor.ca/Hotel_Review-g304551-d304216-Reviews-The_Oberoi_New_Delhi-New_Delhi_National_Capital_Territory_of_Delhi.html"
req = requests.get(url,headers=headers,timeout=5,verify=False)
print (req.status_code)
soup = BeautifulSoup(req.content, 'html.parser')


# In[18]:


# Loop through review pages and create a list of list for reviews
master_review_list = []
# for complete review set 0, 2900, 10
# for last page 2880, 2900, 10

for x in tqdm(range(0, 2900, 10)):
  url = "https://www.tripadvisor.ca/Hotel_Review-g304551-d304216-Reviews-or" + str(x) + "-The_Oberoi_New_Delhi-New_Delhi_National_Capital_Territory_of_Delhi.html#REVIEWS"
  # url = "https://www.tripadvisor.ca/Hotel_Review-g304551-d304216-Reviews-or2890-The_Oberoi_New_Delhi-New_Delhi_National_Capital_Territory_of_Delhi.html#REVIEWS"
  req = requests.get(url,headers=headers,timeout=5,verify=True)
  soup = BeautifulSoup(req.content, 'html.parser')
  for y in soup.body.find_all(class_="YibKl"):
    review_content = []
    # Review content
    if y.find("q", {"class": "QewHA"}) :
      review_content.append(y.select_one('q[class*="QewHA"]').text)
    else :
      review_content.append(None)
    # Trip type i.e. solo, family, couple, business - we will work with this if we have the time
    # if y.find("span", {"class": "TDKzw"}) :
    #   review_content.append(y.select_one('span[class*="TDKzw"]').text)
    # else :
    #   review_content.append(None)
    # Date of stay
    if y.find("span", {"class": "teHYY"}) :
      review_content.append(y.select_one('span[class*="teHYY"]').text)
    else :
      review_content.append(None)
    # Rating
    if y.find("div", {"class": "Hlmiy F1"}) :
      review_content.append(y.find("div", {"class": "Hlmiy F1"}).span['class'][1])
    else :
      review_content.append(None)
    # Owner's response
    if y.find("span", {"class": "MInAm"}) :
      review_content.append(y.select_one('span[class*="MInAm"]').text)
    else :
      review_content.append(None)
    master_review_list.append(review_content)


# In[19]:


# Convert list to a data frame
reviews_df = pd.DataFrame(master_review_list, columns = ['Customer Review', 'Date Of Stay', 'Customer Rating', 'Owner Responded'])


# In[20]:


# Write scrapped data to csv file
reviews_df.to_csv('../data/oberoi_delhi_reviews.csv', index = False)

