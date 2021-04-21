# consumer_affairs.py
# Authors - Jonika Rathi, Shubhang Seth
# This is the program utility used to scrape consumer affairs website and obtain state level pricing for solar panel
# installation
# This file is imported by main.py

# Pandas is used to read the html table available on page
import pandas as pd


# This function reads the table from the page and drops unwanted columns
def scrape_state_wise_cost():
    df = pd.read_html('https://www.consumeraffairs.com/solar-energy/how-much-do-solar-panels-cost.html')[0]
    del df['Starting cost for 6-kW system*']
    del df['2020 federal tax credit value (26%)']
    del df['2021 federal tax credit value (22%']

    #print(df[df['State'] == 'Pennsylvania'])

    return df


# This is for testing purpose only
if __name__ == "__main__":
    print(scrape_state_wise_cost())
