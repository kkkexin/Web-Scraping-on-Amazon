# Amazon Web Scraping Practice
import csv
from bs4 import BeautifulSoup

# Chrome & Firefox
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Microsoft Edge
from msedge.selenium_tools import Edge, EdgeOptions

# Chrome & Firefox
# driver = webdriver.Firefox()

# Edge
# options = EdgeOptions()
# options.use_chromium = True
# driver = Edge(options=options)

def get_url(search_term):
    "Generate a url from a search term"
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_2"
    search_term = search_term.replace(' ','+')

    url = template.format(search_term)

    # add term query to url
    url += "&page{}"

    return url

# # Prototype the record
# item = results[0]
# atag = item.h2.a
# description = atag.text.strip()
# url = "https://www.amazon.com" + atag.get('href')
# price_parent = item.find('span', 'a-price')
# price = price_parent.find('span', 'a-offscreen').text
# rating = item.i.text
# review_count = item.find('span',{'class':'a-size-base'}).text

def extract_record(item):

    # Description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.com" + atag.get('href')

    # Price
    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    # Rank and rating
    try:
        rating = item.i.text
        review_count = item.find('span',{'class':'a-size-base'}).text
    except AttributeError:
        rating = ''
        review_count = ''

    result = (description, price, rating, review_count, url)
    return result


def main(search_term):
    # startup the webdriver
    driver = webdriver.Chrome(ChromeDriverManager().install())

    records = []
    url = get_url(search_term)

    for page in range(1,21):
        driver.get(url.format(page))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type':'s-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

    driver.close()

    with open('webscraping_result.csv', 'w', newline = '', encoding = 'utf-8' ) as f:
        writer = csv.writer(f)
        writer.writerow(['Description','Price','Rating','ReviewCount','Url'])
        writer.writerows(records)

import time
time_start = time.time()
main('office chair')
time_end = time.time()
print('time_cost', time_end-time_start, 's')