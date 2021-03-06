#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
# Import Pandas
import pandas as pd


# Set up the executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visits the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# assign title and summary text to variable
slide_elem.find('div', class_='content_title')


# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f"https://spaceimages-mars.com/{img_url_rel}"


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Populate title list
titles = img_soup.find_all('h3')
titles = titles[:-1]

# Hardcoding hemisphere names to find hrefs via partial match
hemisphere_names = ['cerberus', 'schiaparelli', 'syrtis', 'valles']

# Find all possible hemisphere image links 
imgs = img_soup.find_all("a", class_="itemLink product-item")

# Extract href links 
hemi_links = [i.get('href') for i in imgs]

# Reduce to unique set
hemi_links = list(set(hemi_links[:-1]))


images = []
for link in hemi_links:
    #Build full url f-string
    new_url = f"{url}{link}"
    # Visit new url
    browser.visit(new_url)
    # Extract html w/ splinter
    html = browser.html
    # Optional delay 
    browser.is_element_present_by_id('div.wide-image', wait_time=1)
    # Parse html with soup
    img_soup = soup(html, 'html.parser')
    # Find full img url and append to list
    full_img = img_soup.find('img', class_='wide-image')
    images.append(full_img)

hemisphere_image_urls = [{"image": images[i].get('src'), "title": titles[i].text} for i in range(len(images))]


print(hemisphere_image_urls)


print(len(full_images))


print(len(imgs[0]))

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()




