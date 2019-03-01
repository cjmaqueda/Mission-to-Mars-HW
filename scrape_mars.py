# import dependencies
from bs4 import BeautifulSoup
import pandas as pd
import requests

# set up function to execute all scraping code and return one Python dictionary containing all scraped data

def scrape():

    # define URL to be scraped
    url = 'https://mars.nasa.gov/news/'

    # create BeuatifulSoup object and read text with response and requests
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # print text to examine website content
    # print(soup.prettify())

    # collect the latest News Title
    news_title = soup.find_all('div', class_='content_title')[0].text
    # print(news_title)

    # collect the latest Paragraph Text
    news_paragraph = soup.find_all('div', class_='rollover_description')[0].text
    # print(news_paragraph)

    # to use splinter import Browser
    from splinter import Browser

    # use Splinter to scrape content from a page and then re-route to the next page and continue to scrape
    # setup chromedriver

    executable_path = {'executable_path':'chromedriver.exe'}
    # browser = Browser('chrome', headless=False)
    browser = Browser('chrome', **executable_path, headless=False)

    # visit the (https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image  
    # assign the url string to a variable called `featured_image_url`

    # url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # browser.visit(url)
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find image link with BeautifulSoup
    featured_img_base = "https://www.jpl.nasa.gov"
    featured_img_url_soup = soup.find('div', class_='carousel_items').find("article")["style"]
    featured_img_url = featured_img_url_soup.split("'")[1]
    featured_image_url = featured_img_base + featured_img_url
    # print(featured_image_url)

    # Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called `mars_weather`

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find("p", class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    # print(mars_weather)

    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including:
    # Diameter, Mass, etc.
    mars_facts_url = 'http://space-facts.com/mars/'
    table = pd.read_html(mars_facts_url)
    table[0]

    # create column headers
    mars_facts_df = table[0]
    mars_facts_df.columns = ["Facts", "Values"]
    mars_facts_df  

    # Use Pandas to convert the data to a HTML table string.
    mars_table_html = mars_facts_df.to_html()
    mars_table_html = mars_table_html.replace("\n", "")
    mars_table_html 

    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres
    base_hemispheres_url = "https://astrogeology.usgs.gov"
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)

    # loop through images
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
    
mars_hemispheres_images_url = []

links = soup.find_all("div", class_="item")

for link in links:
    img_dict = {}
    title = link.find("h3").text
    next_link = link.find("div", class_="description").a["href"]
    full_next_link = base_hemispheres_url + next_link
    
    browser.visit(full_next_link)
    
    pic_html = browser.html
    pic_soup = BeautifulSoup(pic_html, 'html.parser')
    
    url = pic_soup.find("img", class_="wide-image")["src"]

    img_dict["title"] = title
    img_dict["img_url"] = base_hemisphere_url + url
    # print(img_dict["img_url"])
    
    mars_hemispheres_images_url.append(img_dict)

mars_hemispheres_images_url

    overall_dict ={
		'news_title' : news_title,
    	'paragraph' : news_paragraph,
    	'featured_image_url' : featured_image_url,
    	'mars_weather' : mars_weather,
    	'mars_table' :  mars_table_html,
    	'hemisphere_images' : mars_hemispheres_images_url}

	return overall_dict

    