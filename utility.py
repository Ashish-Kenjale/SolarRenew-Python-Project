# utility.py
# Authors - Jonika Rathi, Shubhang Seth
# This is the program utility used to scrape the state wise electric utility charges

# We use selenium to perform dynamic scraping
from selenium import webdriver
import time


# using zipcode from google to run method
def getUtilityRate(pincode):
    # For using the default system chromedriver
    # driver = webdriver.Chrome()

    # For using the package chromedriver
    chromedriver = './chromedriver'
    driver = webdriver.Chrome(chromedriver)

    driver.get(
        'https://openei.org/apps/USURDB/?utilRateFindByZip=' + pincode + '&sectors%5B%5D=Residential&service_type=&effective_date=2021-03-08&approved=1&is_default=1&search=')

    time.sleep(1)
    
    try:
        # Pulling the page up, takes you to another page to find the rates.    
        residential = driver.find_element_by_partial_link_text("View")
        residential.click()

        # Rates are listed on the third tab of the page
        tab3 = driver.find_element_by_xpath("//li[@aria-labelledby='ui-id-3']")
        tab3.click()
        

        # Energy rate pulled from Tier 1
        energy = driver.find_element_by_xpath("//*[@id='energy_rate_strux_table']/div[1]/div[5]").text

        driver.close()

        return float(energy)

    except Exception as e:
        print(e)

        # Something bad happened. Quit the driver
        driver.quit()

        return 1


# This is for testing purpose only
if __name__ == '__main__':
    getUtilityRate('15217')
