#!/usr/bin/env python
# coding: utf-8

# ## Data Pre Processing And Cleaning

# Apart from customer reviews we have columns like 'Date Of Stay', 'Customer Rating', and 'Owner Responded'. This data is scrapped from the tripadvisor website as is and need some pre procesing / cleaning to be in a usable format

# In[45]:


import pandas as pd
import numpy as np
import re
from datetime import datetime


# In[46]:


df = pd.read_csv('../data/oberoi_delhi_reviews.csv')
df.head()


# In[47]:


# Custom function to set trip type value
def set_customer_rating(customer_rating) :
  if (customer_rating is np.NAN) :
    return
  elif 'bubble_50' == customer_rating:
    return 'Excellent'
  elif 'bubble_40' == customer_rating:
    return 'Very Good'
  elif 'bubble_30' == customer_rating:
    return 'Average'
  elif 'bubble_20' == customer_rating:
    return 'Poor'
  elif 'bubble_10' == customer_rating:
    return 'Terrible'


# In[48]:


df['Customer Rating'] = df['Customer Rating'].apply(set_customer_rating)


# In[49]:


# Set owner's response from collected date (Yes or No)
def set_owners_response(owners_response) :
  if (owners_response is np.NaN) :
    return 'No'
  else :
    return 'Yes'


# In[50]:


df['Owner Responded'] = df['Owner Responded'].apply(set_owners_response)


# The extracted date is in the form of string. We will convert this string into date format, so that it becomes easier to perform EDA using this column

# In[51]:


# Extract date from string
import datetime
def set_review_date(date_string) :
  if (date_string is np.NaN) :
    return
  else :
    extracted_date = date_string.partition(': ')[2]
    return datetime.datetime.strptime(extracted_date, '%B %Y').strftime('%m/%y')


# In[52]:


df['Date Of Stay'] = df['Date Of Stay'].apply(set_review_date)


# Write the cleaned data to a csv file. The output file will have reviews that are yet to be cleaned which will do further

# In[53]:


df.to_csv('../data/cleaned_data.csv', index = False)


# Check if there are any rows that have missing reviews

# In[58]:


data = pd.read_csv('../data/cleaned_data.csv')
data.isnull().sum()


# In[ ]:




