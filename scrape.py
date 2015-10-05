import time
import bs4
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def search(query):
    # driver = init_driver()
    # driver.get("http://www.amazon.com")
    # try:
    #     box = driver.wait.until(EC.presence_of_element_located(
    #         (By.NAME, "field-keywords")))
    #     button = driver.wait.until(EC.element_to_be_clickable(
    #         (By.CLASS_NAME, "nav-input")))
    #     box.send_keys(query)
    #     button.click()
    # except TimeoutException:
    #     print("Box or Button not found in amazon.com")

    # time.sleep(5)
    # url = driver.current_url
    url = 'http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias' \
          '%3Daps&field-keywords={}'.format(query.replace(' ', '+'))
    product_list = scrape(url)
    print(len(product_list))
    print(product_list)


def scrape(url):
    response = requests.get(url,
                            headers={'User-agent': 'Mozilla/5.0 (Windows NT '
                                                   '6.2; WOW64) AppleWebKit/'
                                                   '537.36 (KHTML, like '
                                                   'Gecko) Chrome/37.0.2062.'
                                                   '120 Safari/537.36'})

    soup = bs4.BeautifulSoup(response.content, "html.parser")
    prod_list = []
    prods = {}

    # for page in soup.find_all('div', id='atfResults'):
    for tag in soup.find_all('li', {'class': 's-result-item'}):
        # print(len(tag))
        # print(len(tag.find_all('li', limit=None, id=re.compile('result_\d'))))

        # print(len(tag.find('ul', id='s-results-list-atf').find_all('li', limit=None)))
        # for tag in page.find_all('li', {'class': 's-result-item'}):
        # for tag in page.find_all('li', id=re.compile('result_\d')):
        # for tag in page.find('ul', id='s-results-list-atf').\
        #         find_all('li', limit=None):
            # print('this should be the result 0-26 {}'.
            #       format(tag._attr_value_as_string('id')))

        prods['title'] = tag.find_all('h2')[0].string

        by_list = tag.find_all('span',
                         {'class': 'a-size-small '
                                   'a-color-secondary'})
        if len(by_list) > 0:
            prods['by'] = by_list[1].string

        price_list = tag.find_all('span',
                         {'class': 'a-size-base '
                                   'a-color-price '
                                   's-price a-text-bold'})
        if len(price_list) > 0:
            prods['price'] = price_list[0].string

        review_list = tag.find_all('a', {'class': 'a-size-small '
                                                      'a-link-normal '
                                                      'a-text-normal'})
        if len(review_list) > 0:
            if 'Show' in review_list[0].string:
                prods['review'] = review_list[1].string
            else:
                prods['review'] = review_list[0].string

        stars_list = tag.find_all('span',
                                  {'class': 'a-icon-alt'})
        if len(stars_list) > 0:
            if stars_list[0].string == 'Prime':
                if len(stars_list) > 1:
                    prods['stars'] = stars_list[1].string
            else:
                prods['stars'] = stars_list[0].string

        prod_url_list = tag.find_all('a',
                                    {'class': 'a-link-normal '
                                              's-access-detail-page  '
                                              'a-text-normal'},
                                     href=True)

        if len(prod_url_list) > 0:
            prods['product_url'] = prod_url_list[0]['href']

        img_url_list = tag.find_all('img',
                                    {'class': 's-access-image '
                                              'cfMarker'})
        prods['img_url'] = img_url_list[0]['src']

        prod_list.append(prods.copy())

    return prod_list


if __name__ == "__main__":

    search_string = input('what would you like to search for? ')
    search(search_string)
    time.sleep(5)

    # driver.quit()
