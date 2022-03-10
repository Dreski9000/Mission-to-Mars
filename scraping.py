#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# define primary scraping function
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    # Visits the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    try:
        # assign title and summary text to variable
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Find the relative image url w/ error handling
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None


    # Use the base URL to create an absolute URL
    img_url = f"https://spaceimages-mars.com/{img_url_rel}"

    return img_url

def mars_hemispheres(browser):
    # Visit URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse HTML with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Scrape image and title elements  
    titles = img_soup.find_all('h3')
    titles = titles[:-1]

    # Find all possible hemisphere image links 
    imgs = img_soup.find_all("a", class_="itemLink product-item")

    # Extract href links 
    hemi_links = [i.get('href') for i in imgs]

    # Reduce to unique set
    hemi_links = list(set(hemi_links[:-1]))

    # Loop through the links and extract full images
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

    # Define list of dictionaries for return value
    hemisphere_image_urls = [{"image": f"{url}{images[i].get('src')}", "title": titles[i].text} for i in range(len(images))]

    return hemisphere_image_urls
# ## Mars Facts

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index of a dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert the dataframe into HTML format, add bootstrap
    return df.to_html()



if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())



