from CoingeckoAPIClass import *
import pandas as pd
from pandas import ExcelWriter
import json
from tabulate import tabulate
import time
import openpyxl
from openpyxl.workbook import Workbook

cg = CoinGeckoAPI()

#put your project slugs here
game_slugs = ['axie-infinity','decentraland','stepn','enjincoin','gala','immutable-x',
              'illuvium','the-sandbox','yield-guild-games','alien-worlds','genopets','league-of-kingdoms','plant-vs-undead-token'

]

#get daily timeseries data (price, market cap, total volume) for a project since its inception
def get_market_data2(slug):
    df = cg.get_coin_market_chart_by_id(id=slug,vs_currency='usd',days='max',interval='daily')
    df = pd.DataFrame.from_dict(df)

    return df

#get all the daily timeseries data for a given project
### (price, market cap, total volume, twitter followers, reddit subs, active reddit users (48hrs), alexa rank)
def get_market_data_by_date2(slug, date):
    df = cg.get_coin_history_by_id(id=slug,vs_currency='usd',date=date,localization='false')
    df = pd.DataFrame.from_dict(df)

    #just show usd
    df.iloc[2,4] = df.iloc[2,4]["usd"]
    df.iloc[3,4] = df.iloc[3,4]["usd"]
    df.iloc[4,4] = df.iloc[4,4]["usd"]

    df.fillna(value=0)

    df['market_data'] = df['market_data'].astype(str)
    df['community_data'] = df['community_data'].astype(str)
    df['developer_data'] = df['developer_data'].astype(str)
    df['public_interest_stats'] = df['public_interest_stats'].astype(str)

    dft = df[['market_data', 'community_data', 'developer_data', 'public_interest_stats']]
    df['data'] = dft.values.tolist()

    df['data'] = df['data'].apply(
        lambda row: [val for val in row if val != 'nan']
    )
    df['data'] = df['data'].apply(
        lambda row: [val for val in row if val != 'None']
    )

    df = df[['data']]
    df['data'] = df.iloc[:, 0].str[0]
    df = df.rename(columns = {'data': date})
    df = df.transpose()
    df.insert(0, 'id', slug, True)
    df = df[['id','current_price','market_cap','total_volume','twitter_followers',
             'reddit_subscribers','reddit_accounts_active_48h','alexa_rank']]

    return df

#take the daily data and convert it to weeks
def get_dates(slug):
    df = get_market_data2(slug)
    periods = (len(df.index)/7)-1
    dates = pd.date_range(end='06/29/2022', periods=periods, freq='W-WED')[::-1]
    dates = dates.strftime('%d-%m-%Y')

    return dates

#get all the weekly timeseries data for a given project
### (price, market cap, total volume, twitter followers, reddit subs, active reddit users (48hrs), alexa rank)
def get_all_data_for_co(slug):
    appended_data = []

    dates = get_dates(slug)
    for date in dates:
        # df = combine_dat_for_slug(slug, date)
        df = get_market_data_by_date2(slug, date)

        appended_data.append(df)
        time.sleep(2)

    df_excel = pd.concat(appended_data)
    return df_excel


##########
# Fetch data for projects and print to different excel sheets >> use this format for whatever projects you want to look at
##########

# axie_infinity = get_all_data_for_co(game_slugs[0])
# axie_infinity.to_excel(('cg-data1.xlsx'), sheet_name=('Axie Infinity'))

# decentraland = get_all_data_for_co(game_slugs[1])
# decentraland.to_excel(('cg-data2.xlsx'), sheet_name=('decentraland'))
#
# stepn = get_all_data_for_co(game_slugs[2])
# stepn.to_excel(('cg-data3.xlsx'), sheet_name=('stepn'))
#
# enjin = get_all_data_for_co(game_slugs[3])
# enjin.to_excel(('cg-data4.xlsx'), sheet_name=('enjin-coin'))
#
# gala = get_all_data_for_co(game_slugs[4])
# gala.to_excel(('cg-data5.xlsx'), sheet_name=('gala'))
#
# immutable = get_all_data_for_co(game_slugs[5])
# immutable.to_excel(('cg-data6.xlsx'), sheet_name=('immutable-x'))
#
# illuvium = get_all_data_for_co(game_slugs[6])
# illuvium.to_excel(('cg-data7.xlsx'), sheet_name=('illuvium'))
#
# sandbox = get_all_data_for_co(game_slugs[7])
# sandbox.to_excel(('cg-data8.xlsx'), sheet_name=('the-sandbox'))

# ygg = get_all_data_for_co(game_slugs[8])
# ygg.to_excel(('cg-data9.xlsx'), sheet_name=('ygg'))
#
# alien_worlds = get_all_data_for_co(game_slugs[9])
# alien_worlds.to_excel(('cg-data10.xlsx'), sheet_name=('alien-worlds'))

# genopets = get_all_data_for_co(game_slugs[10])
# genopets.to_excel(('cg-data11.xlsx'), sheet_name=('genopets'))
#
# lok = get_all_data_for_co(game_slugs[11])
# lok.to_excel(('cg-data12.xlsx'), sheet_name=('league-of-kingdoms'))

# pvu = get_all_data_for_co(game_slugs[12])
# pvu.to_excel(('cg-data13.xlsx'), sheet_name=('plant-vs-undead'))

