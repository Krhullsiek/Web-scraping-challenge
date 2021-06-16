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

#define our scrape method and path
def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


# In[3]:
#go to url

    url = 'https://redplanetscience.com/'
    browser.visit(url)


# In[4]:

#use beautiful soup to parse through data on website
    html=browser.html
    soup=bs(html, 'html.parser')

#create a dict for our scrape materials
# In[5]:
    mars_dict ={}

#find the title and news info in website html
    title = soup.find_all('div', class_='content_title')[0].text
    #print(title)


# In[6]:


    news = soup.find_all('div', class_='article_teaser_body')[0].text
    #print(news)

#add scraped data to mars dict
    mars_dict.update({'Title':title,'News':news})
# In[7]:

#visit next url and follow same steps listed above to find featured image and then add to scraped mars dict
    img_url = 'https://spaceimages-mars.com'
    browser.visit(img_url)


# In[8]:


    html=browser.html
    img_soup=bs(html,'html.parser')
    relative_img_path = img_soup.find_all('img')[1]['src']
    relative_img_path

    
# In[9]:


    featured_image_url = img_url + '/' + relative_img_path
    featured_image_url

    mars_dict.update({'featured_image_url': featured_image_url})
# In[10]:
#go to new url and find mars vs earth facts anf turn that into an html table, then scrape and add to mars dict

    url2 = 'https://galaxyfacts-mars.com'
    browser.visit(url2)
    html=browser.html
    soup2=bs(html, 'html.parser')

# In[11]:


    mars_df = pd.read_html(url2)[0]
    mars_df = mars_df.rename(columns={0:'Stats', 1:'Mars', 2:'Earth'})
    mars_df


# In[12]:


    mars_html = mars_df.to_html()
    mars_html

    mars_dict.update({'mars_facts':mars_html})
# In[13]:


    mars_html.replace('\n', '')
    print(mars_html)


# In[14]:
#visit new url and use for loop to enter each seperate hemisphere page and scrape the image to add to mars dict

    hem_url = 'https://marshemispheres.com/'
    browser.visit(hem_url)


# In[15]:


    html = browser.html
    hem_soup = bs(html, 'html.parser')


# In[16]:


    hems = hem_soup.find('div', class_='collapsible results')
    items = hems.find_all('div', class_='item')
    hems
    items


# In[17]:


    hem_url="https://marshemispheres.com/"
    browser.visit(hem_url)
    html = browser.html
    hem_soup = bs(html, 'html.parser')

    hem_urls = []
    hemispheres = hem_soup.find_all('div', class_='item')

    for hem in hemispheres:
        name = hem.find('h3').text[:-9]
        hem_link = hem.find('a')['href']
        url = hem_url + hem_link
        browser.visit(url)
        html = browser.html
        hem_soup = bs(html, 'html.parser')
        h_img = hem_soup.find('img',class_='wide-image')
        h_img_link = h_img['src']
        hem_dict = {'title': name ,'image_url':hem_url + h_img_link}
        hem_urls.append(hem_dict)
    print(hem_urls)

    mars_dict.update({'hemispheres': hem_urls})
# In[18]:


    browser.quit()

# return the scraped data and print scrape to verify it worked
# In[ ]:

    return mars_dict

if __name__ == "__main__":
    
    # If run from shell
    print (scrape())
