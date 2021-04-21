# main.py
# Authors - Jonika Rathi, Shubhang Seth
# This is the main file of our Solar Renew application.
# Run this file to provide some basic user inputs and get an output pdf file that helps you make
# a decision regarding solar energy investment

# Imports from python interpreter
import re
import webbrowser

# Imports for parsing data, plotting data and converting to pdf
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF, HTMLMixin

# Custom imports of files that perform different scrapings as required by our application
import NSRDB_Solar_Irradiance_API_Get_Version3
import consumer_affairs
import dsire
import google
import line
import utility
import manufacturer_output

plt.rcdefaults()

# Defining a default efficiency of the solar system
efficiency = 1000 * 0.16


class MyFPDF(FPDF, HTMLMixin):
    pass


def validate_address(address):
    if address is None or address == '':
        print('Address is invalid. Please enter address in this format. \"Street, House, City, State, Zipcode\"')
        return False
    else:
        return address.strip()


def validate_space(space):
    try:
        space = float(space)

        # Check if its over the minimum requirement
        if space < 100:
            print('Your house doesn\'t qualify for solar panels. Minimum roof area required is 100sq.feet. Sorry!')
            return False

        return True
    except:
        print('Space provided is invalid. Please enter space in this format \'300.5, 200\' etc')
        return False


def validate_bill(monthly_bill):
    try:
        monthly_bill = float(monthly_bill)

        # Check if its over the minimum requirement
        if monthly_bill < 0:
            print('Please enter a valid electricity bill.')
            return False

        return True
    except:
        print('Bill provided is invalid. Please enter a valid bill amount in this format \'300.5, 200\' etc')
        return False


def get_user_input():
    while True:
        address = input('Please enter your complete address:').strip()
        if not validate_address(address):
            continue
        else:
            break

    while True:
        available_space = input('Please enter the approximate roof area of your house(in sq.feet):')
        if not validate_space(available_space):
            continue
        else:
            break

    while True:
        monthly_bill = input('Enter your average monthly electricity bill, for an accurate savings calculation: ')
        if not validate_bill(monthly_bill):
            continue
        else:
            break

    return address, available_space, monthly_bill


def get_payback_period(location, avg_cost_per_state, available_space, monthly_bill, pdf):
    # Federal incentive of 26% is constant
    fed_incentive = 26

    # Calculating the initial cost
    state_cost = (
        avg_cost_per_state[avg_cost_per_state['State'] == location['state'].capitalize()].iloc[:, 1]).item().replace(
        '$',
        '')
    cost = round(float(state_cost) * efficiency * (available_space * 0.092903), 2)
    #print(cost)
    
    #print("This is the state cost", state_cost)
    
    # Line is python program available in line.py. It is used for plotting the payback period graph.
    return line.plot(monthly_bill * 12, cost, fed_incentive)



def plot_solar_radiation(df, pdf):
    fig = plt.figure()
    jan_DNI = df.where(df['Month'] == 1)['DNI'].sum() / df.where(df['Month'] == 1)['DNI'].count() / 1000 * 24
    feb_DNI = df.where(df['Month'] == 2)['DNI'].sum() / df.where(df['Month'] == 2)['DNI'].count() / 1000 * 24
    mar_DNI = df.where(df['Month'] == 3)['DNI'].sum() / df.where(df['Month'] == 3)['DNI'].count() / 1000 * 24
    apr_DNI = df.where(df['Month'] == 4)['DNI'].sum() / df.where(df['Month'] == 4)['DNI'].count() / 1000 * 24
    may_DNI = df.where(df['Month'] == 5)['DNI'].sum() / df.where(df['Month'] == 5)['DNI'].count() / 1000 * 24
    jun_DNI = df.where(df['Month'] == 6)['DNI'].sum() / df.where(df['Month'] == 6)['DNI'].count() / 1000 * 24
    jul_DNI = df.where(df['Month'] == 7)['DNI'].sum() / df.where(df['Month'] == 7)['DNI'].count() / 1000 * 24
    aug_DNI = df.where(df['Month'] == 8)['DNI'].sum() / df.where(df['Month'] == 8)['DNI'].count() / 1000 * 24
    sep_DNI = df.where(df['Month'] == 9)['DNI'].sum() / df.where(df['Month'] == 9)['DNI'].count() / 1000 * 24
    oct_DNI = df.where(df['Month'] == 10)['DNI'].sum() / df.where(df['Month'] == 10)['DNI'].count() / 1000 * 24
    nov_DNI = df.where(df['Month'] == 11)['DNI'].sum() / df.where(df['Month'] == 11)['DNI'].count() / 1000 * 24
    dec_DNI = df.where(df['Month'] == 12)['DNI'].sum() / df.where(df['Month'] == 12)['DNI'].count() / 1000 * 24
    graph_df = pd.DataFrame(
        [jan_DNI, feb_DNI, mar_DNI, apr_DNI, may_DNI, jun_DNI, jul_DNI, aug_DNI, sep_DNI, oct_DNI, nov_DNI, dec_DNI],
        index=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        columns=['Avg Monthly DNI'])
    ax = graph_df.plot.bar(rot=70, title="Yearly Solar Radiation (kWH/m2/day)")
    # plt.show(block=True)
    ax.figure.savefig('solar_radiation.png', dpi=fig.dpi)
    pdf.image('solar_radiation.png', x=10, y=60, w=150, h=120)


if __name__ == '__main__':
    address, available_space, monthly_bill = get_user_input()
    available_space = float(available_space)
    monthly_bill = float(monthly_bill)

    # Get coordinates for the entered address
    location = google.get_coordinates(address)
    #location = {'state': 'Pennsylvania', 'postal_code': '15217', 'location': {'lat': 40.435271, 'lng': -79.929699}}
    # print(location)

    # Get the active solar policies in the zipcode
    # policies = [{'Implementing Sector:': 'Utility', 'Category:': 'Financial Incentive', 'State:': 'Pennsylvania',
    #              'Incentive Type:': 'Rebate Program',
    #              'Web Site:': '<a href="https://www.dlcwattchoices.com/residentialrebates/" class="ng-binding">https://www.dlcwattchoices.com/residentialrebates/</a>',
    #              'Start Date:': '12/01/2009', 'Utilities:': 'Duquesne Light Co',
    #              'Eligible Renewable/Other Technologies:': 'Solar Water Heat',
    #              'Applicable Sectors:': 'Residential, Multifamily Residential, Low Income Residential',
    #              'Incentive Amount:': '$300/system',
    #              'Eligible System Size:': 'No general size limitations for system, but solar storage tanks must have a capacity of at least 1.25 gallons/square foot of collector',
    #              'Installation Requirements:': 'Must be installed by a qualified contractor (NABCEP certification or a combination of experience and other training qualifies); must retrofit or replace an existing electric water heater; have an output at least 75% of optimal; and meet various other technical specifications (see application for details)',
    #              'Ownership of Renewable Energy Credits:': 'Not addressed. Systems are not eligible to produce Pennsylvania Solar Alternative Energy Credits (SAECs)'},
    #             {'Implementing Sector:': 'State', 'Category:': 'Financial Incentive', 'State:': 'Pennsylvania',
    #              'Incentive Type:': 'Loan Program',
    #              'Web Site:': '<a href="http://dced.pa.gov/programs/solar-energy-program-sep/#.WDSKnLIrJhE" class="ng-binding">http://dced.pa.gov/programs/solar-energy-program-sep/#.WDSKnLIrJhE</a>',
    #              'Administrator:': 'Department of Community and Economic Development (DCED) and the Department of Environmental Protection (DEP)',
    #              'Start Date:': '11/02/2016',
    #              'Eligible Renewable/Other Technologies:': 'Solar Water Heat, Solar Thermal Electric, Solar Photovoltaics',
    #              'Applicable Sectors:': 'Commercial, Industrial, Local Government, Nonprofit, Schools, Agricultural',
    #              'Maximum Loan:': 'Manufacturer of solar equipment: $40,000 for every new job projected to be created by 3 years <br>\nSolar energy generation or distribution project: $5 million or $3 per watt <br>\nSolar research and development facility: $5 million <br> <br>\n\n25% matching investment required for all loan amounts<br>',
    #              'Loan Term:': 'Not to exceed 22 years for equipment and 15 years for real estate.',
    #              'Interest Rate:': 'Interest rate: 10 year Treasury + 250 Basis Points (subject to change) <br>\nFixed interest rate determined at the time of approval of the loan. <br> <br>\n\n$100 non-refundable application fee<br>\n1% commitment fee on all approved loans <br>'},
    #             {'Implementing Sector:': 'State', 'Category:': 'Financial Incentive', 'State:': 'Pennsylvania',
    #              'Incentive Type:': 'Solar Renewable Energy Credit Program',
    #              'Web Site:': '<a href="http://paaeps.com/credit/" class="ng-binding">http://paaeps.com/credit/</a>',
    #              'Eligible Renewable/Other Technologies:': 'Solar Photovoltaics',
    #              'Applicable Sectors:': 'Commercial, Industrial, Local Government, Nonprofit, Residential, Schools, State Government, Installers/Contractors, Agricultural, Multifamily Residential, Low Income Residential',
    #              'Incentive Amount:': 'Varies based on market conditions; during 2015 the market price for PA-sourced SRECs has ranged from approximately $32 - $55/MWh ($0.032 - $0.055/kWh) although individual trades have taken place at substantially lower and higher prices.',
    #              'Maximum Incentive:': 'Varies based on market conditions; SACP does not represent a price ceiling because it is only determined after the fact',
    #              'Eligible System Size:': 'No system size limitations',
    #              'Equipment Requirements:': 'Systems generally require a utility-grade performance meter (exception exists for some facilities of 15 kW or smaller)'}]
    policies = dsire.get_policies(location['postal_code'])
    # print(policies)

    # Get the average cost of installation per state
    avg_cost_per_state = consumer_affairs.scrape_state_wise_cost()
    #print(avg_cost_per_state)

    # Get the solar radiation data
    result = NSRDB_Solar_Irradiance_API_Get_Version3.get_solar_radiation_data(location['location']['lat'],
                                                                              location['location']['lng'])
    solar_radiation = result[0]  # kWh / m2 / day

    # Get the utility rate for zipcode
    utility_rate = utility.getUtilityRate(location['postal_code'])

    # Estimate the monthly utility usage for the user
    monthly_energy_usage = monthly_bill / utility_rate
    # print(monthly_energy_usage)

    # Estimate the energy production with solar radiation
    solar_energy_per_day = solar_radiation * efficiency / (available_space * 0.092903)
    #print(solar_energy_per_day)

    # Generating the analysis
    # Source: https://www.geeksforgeeks.org/convert-text-and-text-file-to-pdf-using-python/
    pdf = MyFPDF()

    image_name, payback_period = get_payback_period(location, avg_cost_per_state, available_space, monthly_bill, pdf)
    

    # First page
    pdf.add_page()
    pdf.set_font('Arial', size=25, style='B')
    pdf.cell(0, 10, txt='SolarRenew Analysis', ln=1, align='C')
    pdf.set_font('Arial', size=12)
    pdf.ln(8)
    pdf.cell(0, 6, txt='Congratulations on evaluating whether or not solar power is right for you!', ln=1, align='L')
    pdf.cell(0, 6, txt='SolarRenew is here to assist you with your evaluation.', ln=1, align='L')
    pdf.ln(8)
    pdf.cell(0, 6, txt='SolarRenew took your address: ')
    pdf.set_font('Arial', size=12, style='B')
    pdf.ln(6)
    pdf.cell(0, 6, txt=address)
    pdf.set_font('Arial', size=12)
    pdf.ln(6)
    pdf.multi_cell(0, 6, txt='We calculated your location specific solar figures. This complicated process was made easier by experts at SolarRenew.',
                   align='L')
    pdf.ln(8)
    pdf.multi_cell(0, 6,
                   txt='In order to understand if solar panels are right for you, our program helps you holistically evaluate your personal situation by answering these 6 key questions: ',
                   align='L')
    pdf.cell(0, 6, txt='1. Where will the panels be installed?', ln=1, align='L')
    pdf.cell(0, 6, txt='2. What is your available area for panels', ln=1, align='L')
    pdf.cell(0, 6, txt='3. How much solar energy is available at your location?', ln=1, align='L')
    pdf.multi_cell(0, 6, txt='4. What are the local costs for solar installation (including how large your system is)?',
                   align='L')
    pdf.cell(0, 6, txt='5. What are the federal and state incentives available to you?', ln=1, align='L')
    pdf.cell(0, 6, txt='6. What is your local utility rate for energy?', ln=1, align='L')
    pdf.ln(8)
    pdf.multi_cell(0, 6,
                   txt='You provided SolarRenew your location and area available for panels. We took care of the rest!',
                   align='L')
    pdf.ln(8)
    pdf.set_font('Arial', size=15, style='B')
    pdf.cell(0, 12, txt='Results:', ln=1, align='L')
    pdf.set_font('Arial', size=12)
    savings = int(solar_radiation * available_space *0.12* 365 * 0.092903 * float(utility_rate))
    generate = int(solar_radiation *0.12* 365 * 0.092903* available_space)
    pdf.multi_cell(0, 6,
                   txt='Based on your location, you can generate ' + str(generate) + ' kWh annually from solar power! That will save approx. $' + str(savings) + ' dollars / year off your electricity bill, according to your local energy rate of ' + str(round(utility_rate,3)) + ' $/kWh.',
                   align='L')
    pdf.ln(8)
    install = round(available_space * efficiency/1000 * 0.092903, 1)
    estcost = int(install * 2.38 * 1000)
    pdf.multi_cell(0, 6,
                   txt='Based on your location and the area you provided, you can install a ' + str(install) + ' kW system. To install this system, it will cost an estimated $' + str(estcost) + ' to install.',
                   align='L')
    pdf.ln(8)
    govpaid = estcost * 0.26
    roundedpaid = int(govpaid)
    pdf.multi_cell(0, 6,
                   txt='Currently, there are federal incentives available to you. Until the end of 2021, the government will pay for 26% of your entire solar investment. The government will pay for $' +  str(roundedpaid) + ' of your cost of installation mentioned above!',
                   align='L')
    pdf.ln(8)
    pdf.multi_cell(0, 6,
                   txt='Based on your monthly utility bill, you likely use ' + str(12 * int(monthly_energy_usage)) + ' kWh annually. Your ' + str(install) + ' kW solar system could cover ' + str(int(generate/monthly_energy_usage * 100 / 12)) + '% of your energy needs!',
                   align='L')
    pdf.ln(8)
    pdf.multi_cell(0, 6,
                   txt='In summary, if you invested in solar panels today, your entire investment would be paid-off in ' + str(round(payback_period, 1)) + ' years. And after that point, your solar system will be providing you $' + str(savings) + ' of extra income annually.',
                   align='L')
    pdf.ln(8)
    pdf.multi_cell(0, 6,
                   txt='In addition to everything we covered, you might have additional state incentives to assist more. For example, some states buyback extra energy you produce, giving you additional savings! We included the state incentives you\'re potentially eligible for at the end of the pdf report. Look it over to possibly improve your payback period!',
                   align='L')

    # Dig Deeper into the Analysis
    pdf.add_page()
    pdf.set_font('Arial', size=15, style='') 
    pdf.cell(0, 15, txt='Listed below are several factors that might help you decide.', ln=1, align='L')
    pdf.cell(0, 20, txt='1. Daily Solar Energy Available for your house', ln=1, align='L')

    # Plot the solar radiation data
    plot_solar_radiation(result[1], pdf)

    # Get the payback period
    pdf.add_page()
    pdf.set_font('Arial', size=15, style='')
    pdf.cell(0, 0, txt='2. Payback Period', ln=1, align='L')
    pdf.cell(0, 30, txt='You can start making money after {:.2f} years'.format(payback_period), ln=1, align='L')
    pdf.image(image_name, x=10, y=40, w=150, h=120)


    # Get manufacturer output data
    manufacturer_output_df = manufacturer_output.get_manufacturer_data()
    # print(manufacturer_output_df)

    # Add manufacturer data to the pdf
    pdf.add_page()
    pdf.set_font('Arial', size=15, style='')
    pdf.cell(0, 30, txt='3. Manufacturer Data', ln=1, align='L')
    fig = plt.figure()

    cell_text = []
    for row in range(len(manufacturer_output_df)):
        cell_text.append(manufacturer_output_df.iloc[row])

    plt.table(cellText=cell_text, colLabels=manufacturer_output_df.columns, loc='center')
    plt.axis('off')
    fig.savefig('table.png', dpi=fig.dpi, bbox_inches='tight', transparent="True", pad_inches=0)

    pdf.cell(0, 30, txt= 'Here are a few manufacturers of solar panels and the energy they generate :', ln=1, align='L')
    pdf.image('table.png', x=10, y=20, w=150, h=120)

    pdf.add_page()
    pdf.set_font('Arial', size=15, style='')
    pdf.cell(10, 10, txt='4. State Incentives', align='L')

    page_width = pdf.w - (2 * pdf.l_margin)
    key_space = 65
    val_space = 130

    pat = r'^(<a href=")(.*)(" class).*$'

    for i, policy in enumerate(policies):
        # pdf.set_font('Arial', size=15, style='')
        pdf.cell(0, 30, txt='Incentive Policy {:d}'.format(i + 1), align='C', ln=1)
        # pdf.set_font('Arial', size=15, style='')
        pdf.ln(0.5)

        for key, val in policy.items():
            pdf.set_font('Arial', size=10, style='')
            val = val.replace('<br>', '')

            # Max chars check for a cell
            if len(key) < 30 and len(val) < 75:
                pdf.cell(key_space, 10, key, border=0)

                m = re.search(pat, val)
                if m:
                    val = m.group(2)

                pdf.cell(val_space, 10, val, border=0)
                pdf.ln(8)
            else:
                while len(key) > 0:
                    if "/" in key:
                        key = key.split('/')[0] + ":"
                    pdf.cell(key_space, 10, key[:50], border=0)
                    key = key[55:]

                j = 10
                while len(val) > 0:
                    m = re.search(pat, val)
                    if m:
                        val = m.group(2)

                    if j > 10:
                        pdf.cell(key_space, 10, '', border=0)

                    pdf.cell(val_space, 10, val[:75], border=0)
                    pdf.ln(8)
                    j += 10
                    val = val[75:]

        if i + 1 < len(policies):
            pdf.add_page()
        pdf.set_font('Arial', size=15, style='')

    pdf.output('Analysis.pdf', dest='F')
print("Generated report in Analysis.pdf")
webbrowser.open_new('Analysis.pdf')
