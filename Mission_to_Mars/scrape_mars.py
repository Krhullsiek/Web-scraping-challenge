#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import pymongo
from bs4 import BeautifulSoup as bs
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time



# In[2]:

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    mars_dict ={}

# In[3]:


    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html=browser.html
    soup=bs(html, 'html.parser')


# In[4]:


    title = soup.find_all('div', class_='content_title')[0].text
    print(title)


# In[5]:


    news = soup.find_all('div', class_='article_teaser_body')[0].text
    print(news)


# In[6]:


    img_url = 'https://spaceimages-mars.com'
    browser.visit(img_url)


# In[7]:


    html=browser.html
    img_soup=bs(html,'html.parser')
    relative_img_path = img_soup.find_all('img')[1]['src']
    relative_img_path


# In[8]:


    featured_image_url = img_url + '/' + relative_img_path
    featured_image_url


# In[9]:


    url2 = 'https://galaxyfacts-mars.com'
    browser.visit(url2)
    html=browser.html
    soup2=bs(html, 'html.parser')


# In[10]:


    mars_df = pd.read_html(url2)[0]
    mars_df = mars_df.rename(columns={0:'Stats', 1:'Mars', 2:'Earth'})
    mars_df


# In[11]:


    mars_html = mars_df.to_html()
    mars_html


# In[12]:


    mars_html.replace('\n', '')
    print(mars_html)


# In[13]:


    hem_url = 'https://marshemispheres.com/'
    browser.visit(hem_url)


# In[14]:


    html = browser.html
    hem_soup = bs(html, 'html.parser')


# In[15]:


    hems = hem_soup.find('div', class_='collapsible results')
    items = hems.find_all('div', class_='item')
    hems
    items


# In[17]:


    hem_urls = []

    for x in items:

        h_title = x.find('div', class_= 'description').find('a', class_='itemLink product-item').h3.text
        hem_img_url = hem_url + x.find('a', class_ = 'itemLink product-item')['href']
        browser.visit(hem_img_url)
        html_= browser.html
        hem_img_soup = bs(html, 'html.parser')
        img_link= hem_img_soup.find('div', class_ = 'page-background')
        img_url= img_link
    
    
        hem_urls.append({'Title':h_title, 'Img_URL':img_url})
    
    print(hem_urls)


    mars_dict = { 'news_title': title,'news':news, 'featured_img_url':featured_image_url,
    'mars_table':str(mars_html), 'hempispheres':hem_urls}



# In[ ]:


    browser.quit()


# In[ ]:


    return mars_dict

if __name__ == "__main__":
    
    # If run from shell
    print (scrape())
