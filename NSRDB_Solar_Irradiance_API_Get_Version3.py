# NSRDB_Solar_Irradiance_API_Get_Version3.py
# Authors - Jonika Rathi, Shubhang Seth
# This is the program utility used to integrate with NSRDB APIs and get solar irradiance data.
# March 7 2021

# Libraries import
import pandas as pd


def get_solar_radiation_data(lattitude, longitude):
    # API parameters
    lat = lattitude  # default =    14.62    ;   pittsburgh: 40.44
    lon = longitude  # default =    -24.27   ;   pittsburgh: -79.99
    year = '2017'
    api_key = 'QlBIVyL7kT9hsldmMzUU6noUrYYLBIAN8jkmH0IT'
    leap_year = 'false'
    interval = '60'
    utc = 'true'
    name = 'Jonika+Rathi'
    reason_for_use = 'Academic'
    affiliation = 'Carnegie+Mellon'
    email = 'jrathi@andrew.cmu.edu'
    mailing_list = 'false'
    attributes = 'dni'

    # Production URL
    url = 'https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(
        year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=name, email=email,
        mailing_list=mailing_list, affiliation=affiliation, reason=reason_for_use, api=api_key, attr=attributes)
    rawdata = pd.read_csv(url, skiprows=2)
    df = pd.DataFrame(rawdata)

    # Change datatype for uniformity
    df['Year'] = df['Year'].astype(int)
    df['Month'] = df['Month'].astype(int)
    df['Day'] = df['Day'].astype(int)
    df['Minute'] = df['Minute'].astype(int)
    df['DNI'] = df['DNI'].astype(float)

    # Final calculations for solar irradiance
    total_DNI = df['DNI'].sum()  # total of DNI column
    average_DNI = total_DNI / len(df)  # convert table to average
    average_DNI /= 1000  # convert watts to kilowatts
    average_DNI *= 24  # convert annual hours to daily

    return average_DNI, df


# This is for testing purpose only
if __name__ == "__main__":
    result = get_solar_radiation_data(14.62, -24.27)
    print('The average annual solar radiation value for your given location is: ', round(result[0], 2), 'kWh/m2/day')
    df = result[1]
    # Graph of averages per month
    import matplotlib.pyplot as plt

    plt.rcdefaults()
    import matplotlib.pyplot as plt

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
    print(graph_df)
    graph_df.plot.bar(rot=70, title="Yearly Solar Radiation (kWH/m2/day)")
    plt.show(block=True)
