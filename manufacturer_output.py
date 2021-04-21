import pandas as pd
import os
from selenium import webdriver
import matplotlib.pyplot as plt


def get_manufacturer_data():
    # Loading the  chromedriver for headless browsing
    chromedriver = './chromedriver'
    os.environ['webdriver.chrome.driver'] = chromedriver
    driver = webdriver.Chrome(chromedriver)

    link = "https://news.energysage.com/what-is-the-power-output-of-a-solar-panel/#:~:text=Solar%20panels%20usually%20produce%20between%20250%20and%20400,different%20wattage%20panels%20will%20affect%20your%20unique%20system."

    print('Starting scraping for details of manufacturer output data')

    try:
        driver.get(link)
        rowdata = driver.find_elements_by_xpath('//*[@id="tablepress-10-no-2"]/tbody/tr')
        rowlen = len(rowdata)

        collen = len(driver.find_elements_by_xpath('//*[@id="tablepress-10-no-2"]/tbody/tr[1]/td'))

        solar_data = []
        for r in range(1, rowlen+1):
            solar_data_row = []
            for c in range(1, collen+1):
                val = driver.find_elements_by_xpath("//*[@id='tablepress-10-no-2']/tbody/tr["+str(r)+"]/td["+str(c)+"]")
                val_text = val[0].text

                try:
                    solar_data_row.append(float(val_text))
                except:
                    solar_data_row.append(val_text)

            solar_data.append(solar_data_row)

        solar_output_df = pd.DataFrame(solar_data, columns=['Solar Panel Manufacturer', 'Minimum', 'Maximum', 'Average (in Watts)'])
        #solar_output_df = solar_output_df.reset_index(drop=True, inplace=True)
        solar_output_df = solar_output_df.drop(columns=['Minimum', 'Maximum'])

        # Picking 3 random manufacturers
        solar_output_df = solar_output_df.sample(3)

        return solar_output_df

    except Exception as e:
        print(e)

        # Something bad happened. Quit the driver
        driver.quit()

        return []

if __name__ == '__main__':
    print(get_manufacturer_data())

