import requests 
import pandas as pd
from datetime import timezone
from datetime import datetime 
from datetime import date 
from datetime import timedelta
import time
from django.conf import settings


lunarcrush_key = 'loemw18b9kle5e8v3h93ss'

def top_coins():
    lc_market = requests.get(
        url = 'https://api.lunarcrush.com/v2?data=market&',
        params = {
            'key': lunarcrush_key,      
        }
    )
    all_coins = []
    for entry in lc_market.json().get('data'):
        coin = []
        coin.append(entry.get('s'))
        coin.append(entry.get('mc'))
        all_coins.append(coin)
    all_coins.sort(key = lambda x : x[1], reverse = True)
    top_ten_coins = all_coins[:10]
    return(top_ten_coins)

top_coins_lst = top_coins()
top_coin_names_lst = [x[0] for x in top_coins_lst]

def get_coin_data(key, coin, date_diff, start_date, end_date):
    lc = requests.get(
        url = 'https://api.lunarcrush.com/v2?data=assets&',
        params = {
            'key': lunarcrush_key,
            'symbol': coin,
            'interval': 'day',
            'data_points': date_diff,
            'start': int(start_date.replace(tzinfo=timezone.utc).timestamp()),
            'end': int(end_date.replace(tzinfo=timezone.utc).timestamp())       
        }
    )
    metric_names = []
    for entry in lc.json().get('data')[0].get('timeSeries'):
        for key in entry:
            metric_names.append(key) if key not in metric_names else metric_names
    metrics_list = []
    for entry in lc.json().get('data')[0].get('timeSeries'):
        row_list = []
        for key in entry:
            row_list.append(entry.get(key))
        metrics_list.append(row_list)
    metrics_df = pd.DataFrame(metrics_list, columns = metric_names)
    metrics_df['time'] = metrics_df['time'].apply(lambda x : datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    metrics_df['coin'] = coin
    cols = list(metrics_df)
    cols.insert(0, cols.pop(cols.index('coin')))
    metrics_df = metrics_df.loc[:, cols]
    return(metrics_df)

def get_all_coins_data(coins_list):
    appended_data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days = 700)
    date_diff = (end_date - start_date).days
    for coin in coins_list:
        appended_data.append(get_coin_data(lunarcrush_key, coin, date_diff, start_date, end_date))
        time.sleep(.1)
    output = pd.concat(appended_data)
    return(output)

df = get_all_coins_data(top_coin_names_lst)

focused_df = df[['coin', 'asset_id', 'time', 'close', 'volume', 'market_cap', 'reddit_posts', 'reddit_comments', 'tweets', 'tweet_favorites', 'social_volume']]

user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
database_name = settings.DATABASES['default']['NAME']

database_url = 'sqlite3://{user}:{password}@localhost:5432/{database_name}'.format(
    user=user,
    password=password,
    database_name=database_name,
)

engine = create_engine(database_url, echo=False)
focused_df.to_sql(cryptoData, con=engine)


print(focused_df)