import pandas as pd
import os
import requests
import time
from splinter import Browser
from bs4 import BeautifulSoup

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/Users/pogom/OneDrive/Desktop/BootCamp/13-Web-Scraping-and-Document-Databases/Homework/Mission-to-Mars"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    browser = init_browser()
    # create mars_data dict that we can insert into mongo
    scrape_mars = {}

    #NASA Mars News - Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    #Assign the text to variables that you can reference later.

    browser = Browser('chrome', headless=False)
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)

    mars_html_news = browser.html
    mars_soup_news = BeautifulSoup(mars_html_news, 'html.parser')

    div1 = mars_soup_news.find('div', class_='content_title')
    
    news_title = div1.find('a').text
    news_p = mars_soup_news.find('div', class_='article_teaser_body').text

    # add them into mars_data dict
    scrape_mars['news_title'] = news_title
    scrape_mars['news_p'] = news_p

    #JPL Mars Space Images - Featured Image

    #Find image url
    browser = Browser('chrome', headless=False)
    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_img)
    browser.click_link_by_partial_text('FULL IMAGE')

    # Current featured mars image
    nasa_html_img = browser.html
    nasa_soup_img = BeautifulSoup(nasa_html_img, 'html.parser')

    nasa_home = nasa_soup_img.find('article', class_="carousel_item")
    nasa_link = nasa_home.a['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + nasa_link

    # add it into scrape_mars dict
    scrape_mars['featured_image_url'] = featured_image_url

    # Mars Weather - Visit the Mars Weather twitter account

    # Visit the Mars Weather twitter account
    mars_url_weather = 'https://twitter.com/marswxreport?lang=en'
    mars_html_weather = requests.get(mars_url_weather)
    mars_soup_weather = BeautifulSoup(mars_html_weather.text, 'html.parser')

    tweet = mars_soup_weather.find('div', class_='stream')
    mars_weather = tweet.find(text="Mars Weather").findNext('p').text

    # add it into scrape_mars dict
    scrape_mars['mars_weather'] = mars_weather

    # Mars Facts and create a html table using pandas

    mars_facts_url = 'https://space-facts.com/mars/'
    mars_tables = pd.read_html(mars_facts_url)
    mars_df = mars_tables[0]
    mars_df.columns = ['Description', 'Value']
    mars_df.set_index('Description', inplace=True)
    mars_df.to_html('Mars_df.html')

    # Export scraped table into an html script    
    mars_facts = mars_df.to_html()
    mars_facts.replace("\n","")
    mars_df.to_html('mars_facts.html')

    # Store html file to dictionary
    scrape_mars['mars_facts'] = mars_facts

    browser = Browser('chrome', headless=False)
    url_hemisperes = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemisperes)

    #Mars Hemispheres
    mars_html_hemisperes = browser.html
    mars_soup_hemisperes = BeautifulSoup(mars_html_hemisperes, 'html.parser')
    mars_images = mars_soup_hemisperes.find_all('div', class_='description')

    # loop through each hemisphere image and find large image url
    hemisphere_urls = []

    for image in mars_images:
        
        image_dict = {}
        
        href = image.find('h3').text
        image_dict['title'] = href
        browser.click_link_by_partial_text(href)
        
        mars_html2 = browser.html
        mars_soup2 = BeautifulSoup(mars_html2, 'html.parser')
        
        url = mars_soup2.find('img', class_='wide-image')['src']
        image_dict['img_url'] = 'https://astrogeology.usgs.gov' + url
        
        hemisphere_urls.append(image_dict)
        browser.click_link_by_partial_text('Back')
        
       
    # Store hemisphere image urls to dictionary
    scrape_mars['hemisphere_urls'] = hemisphere_urls

    return scrape_mars