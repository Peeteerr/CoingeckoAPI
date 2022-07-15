from CoingeckoAPIClass import *
import pandas as pd
from pandas import ExcelWriter
import json
from tabulate import tabulate
import time
import openpyxl
from openpyxl.workbook import Workbook

cg = CoinGeckoAPI()
end_date = '06/29/2022' #insert your request end date in month/day/year format.

#put your project slugs here. Ex:
slugs = ['axie-infinity','decentraland','stepn','enjincoin','gala','immutable-x',
              'illuvium','the-sandbox','yield-guild-games','alien-worlds','genopets','league-of-kingdoms','plant-vs-undead-token'

]

#get all daily timeseries data for a project from its inception to stated end date, return as pandas dataframe
### (price, market cap, total volume)
### this is where you can get daily data
def get_market_data2(slug):
    df = cg.get_coin_market_chart_by_id(id=slug,vs_currency='usd',days='max',interval='daily')
    df = pd.DataFrame.from_dict(df)
    return df

#get all daily timeseries data for a given project at a given date, return as pandas dataframe
### (price, market cap, total volume, twitter followers, reddit subs, active reddit users (48hrs), alexa rank)
def get_market_data_by_date2(slug, date):
    df = cg.get_coin_history_by_id(id=slug,vs_currency='usd',date=date,localization='false')
    df = pd.DataFrame.from_dict(df)

    #edit dataframe to just show usd value of metrics
    df.iloc[2,4] = df.iloc[2,4]["usd"]
    df.iloc[3,4] = df.iloc[3,4]["usd"]
    df.iloc[4,4] = df.iloc[4,4]["usd"]

    df.fillna(value=0) #replace N/A data with empty cells to make the final dataset output easier to use
    
    #convert all outputs to strings for further data manipulation
    df['market_data'] = df['market_data'].astype(str)
    df['community_data'] = df['community_data'].astype(str)
    df['developer_data'] = df['developer_data'].astype(str)
    df['public_interest_stats'] = df['public_interest_stats'].astype(str)

    #reconfigure dataframe to get rid of unnecessary column/row data 
    ###(ex.- market cap only has a value in 'market_data' column; missing values elswhere)
    dft = df[['market_data', 'community_data', 'developer_data', 'public_interest_stats']]
    df['data'] = dft.values.tolist()
    df['data'] = df['data'].apply(lambda row: [val for val in row if val != 'nan'])
    df['data'] = df['data'].apply(lambda row: [val for val in row if val != 'None'])
    df = df[['data']]
    df['data'] = df.iloc[:, 0].str[0]
    df = df.rename(columns = {'data': date})
    df = df.transpose() #flip rows and columns for intuitive output
    df.insert(0, 'id', slug, True) #insert an id tag showing project to which data belongs
    
    #rename columns with proper metric identifiers, return full pandas dataframe
    df = df[['id','current_price','market_cap','total_volume','twitter_followers',
             'reddit_subscribers','reddit_accounts_active_48h','alexa_rank']]
    return df

#take all the days with data for a given project and return weekly dates from within that series from most recent to oldest
def get_dates(slug):
    df = get_market_data2(slug)
    periods = (len(df.index)/7)-1
    dates = pd.date_range(end=end_date, periods=periods, freq='W-WED')[::-1]
    dates = dates.strftime('%d-%m-%Y')
    return dates

#get all weekly timeseries data for a given project from inception to stated end date, return as pandas dataframe
### (price, market cap, total volume, twitter followers, reddit subs, active reddit users (48hrs), alexa rank)
def get_all_data_for_co(slug):
    appended_data = []
    dates = get_dates(slug)
    
    #loop through dates in weekly series return data and append to dataframe list
    for date in dates:
        # df = combine_dat_for_slug(slug, date)
        df = get_market_data_by_date2(slug, date)
        appended_data.append(df)
        time.sleep(2)

    #combinee all dataframes in dataframe list, return as pandas dataframe
    df_excel = pd.concat(appended_data)
    return df_excel


##########
# Fetch data for projects and print to different excel sheets >> use this format for whatever projects you want to look at. Ex:
##########

# axie_infinity = get_all_data_for_co(slugs[0])
# axie_infinity.to_excel(('cg-data1.xlsx'), sheet_name=('Axie Infinity'))

# decentraland = get_all_data_for_co(slugs[1])
# decentraland.to_excel(('cg-data2.xlsx'), sheet_name=('decentraland'))
#
# stepn = get_all_data_for_co(slugs[2])
# stepn.to_excel(('cg-data3.xlsx'), sheet_name=('stepn'))
#
# enjin = get_all_data_for_co(slugs[3])
# enjin.to_excel(('cg-data4.xlsx'), sheet_name=('enjin-coin'))

# pvu = get_all_data_for_co(slugs[12])
# pvu.to_excel(('cg-data13.xlsx'), sheet_name=('plant-vs-undead'))

