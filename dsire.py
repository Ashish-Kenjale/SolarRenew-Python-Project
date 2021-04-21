# dsire.py
# Authors - Jonika Rathi, Shubhang Seth
# This is the program utility used to scrape DSIRE website and obtain state level policies for solar energy.
# This file is imported by main.py

# This program uses selenium to perform dynamic scraping
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os


# This function is used to scrape a single detail page of policy
def scrape_detail_page(driver, link):
    print('Starting scraping for details of ' + link.get_attribute('innerHTML'))
    print(link.get_attribute("href"))
    href = link.get_attribute("href")

    response = {}

    # Open link
    # open new blank tab
    driver.execute_script("window.open();")

    # switch to the new window which is second in window_handles array
    driver.switch_to.window(driver.window_handles[1])
    driver.get(href)

    # Wait for 1 secs
    time.sleep(1)

    # Find the main div
    info_div = driver.find_element_by_class_name('programOverview')
    list_items = info_div.find_element_by_tag_name('ul').find_elements_by_tag_name('li')

    # Each item has 2 divs. One for heading and one for value
    # We will use the heading as key and value as value for our response dict
    for item in list_items:
        # print(item.get_attribute('innerHTML'))
        divs = item.find_elements_by_tag_name('div')
        response[divs[0].get_attribute('innerHTML')] = divs[1].get_attribute('innerHTML')

    driver.close()

    return response


# This function is used in main.py to get all the policies available in a state, related to solar energy
def get_policies(pincode):
    # Loading the  chromedriver for headless browsing
    chromedriver = './chromedriver'
    os.environ['webdriver.chrome.driver'] = chromedriver
    driver = webdriver.Chrome(chromedriver)

    try:
        # Open the website
        print('Opening DSIRE website')
        driver.get('https://programs.dsireusa.org/system/program?zipcode=' + pincode)

        # Get the filter div
        div_ele = driver.find_element_by_id('DataTables_Table_0_filter')

        # Get the child input element from filter div
        search_field = div_ele.find_element_by_tag_name('input')
        search_field.send_keys('Solar')
        search_field.send_keys(Keys.RETURN)

        # Wait for 5 secs to load the data
        time.sleep(2)

        # Get the table which has the data
        table = driver.find_element_by_id('DataTables_Table_0')
        table_body = table.find_element_by_tag_name('tbody')
        rows = table_body.find_elements_by_css_selector('tr')

        # Get our result array ready
        programs = []

        # Loop through table rows
        for row in rows:
            # Here we just want the first cell for extracting the link
            link = row.find_element_by_css_selector('td').find_element_by_css_selector('a')
            programs.append(scrape_detail_page(driver, link))
            driver.switch_to.window(driver.window_handles[0])

        return programs
    except Exception as e:
        print(e)

        # Something bad happened. Quit the driver
        driver.quit()

        return []


# This is for testing purpose only
if __name__ == '__main__':
    print(get_policies('15217'))
