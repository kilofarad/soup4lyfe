import requests, datetime
import pandas as pd

def get_currencies_list():
    '''Returns a list of supported currencies for our analysis'''
    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    response = requests.get(url)

    if response.status_code ==  200:
        response = response.json()
        coins = response['Data']
        coins = set(coins.keys())

    url = 'https://min-api.cryptocompare.com/data/news/categories'
    response = requests.get(url)

    if response.status_code == 200:
        response = response.json()
        cats = set([v['categoryName'] for v in response])

    return list( coins & cats )

def fetchNewsPerCoin(sym, begin = 1517443200, end = None, hard_start = False):
    '''Fetches a dataframe containing news for the given coin between the specified timestamps.
        Note that from and to must be epoch timestamps.
        Default behavior is to fetch from 2/1/2018 to the present day. 
        If hard_start is True, it will trim off times prior to the begin timestamp'''
    #TODO: implement hard_start
    try:
        if end:
            int(end)
        int(begin)
    except:
        raise ValueError('fetchNewsPerCoin begin and end parameters should be castable to int')

    cols = ['published_on', 'title', 'source', 'body', 'tags']
    lts = end 
    df = pd.DataFrame(columns = cols)
 
    while(lts is None or lts > begin):
        ltsString = '&lTs={}'.format(lts) if lts else ''
        url = 'https://min-api.cryptocompare.com/data/v2/news/?lang=EN&categories={}&sortOrder=latest'.format(sym) + ltsString
        response = requests.get(url)
        if response.status_code ==  200 :
            dic = response.json()
            try:
                lts = dic['Data'][-1]['published_on']
            except IndexError:
                if dic['hasWarning']:
                    print(response.content)
                    raise Exception('Empty API Response')
                else:
                    break

            print('\t', datetime.datetime.utcfromtimestamp(lts).isoformat())

            #remove unwanted data from dict prior to df conversion
            for data_dic in dic['Data']:
                ks = list(data_dic.keys())
                for key in ks:
                    if key not in cols:
                        del data_dic[key]
            data = pd.DataFrame.from_dict(dic['Data'], orient = 'columns')

            #convert the timestamp into ISO format
            data['published_on'] = pd.to_datetime(data.published_on, unit='s')
            df = df.append(data, sort=True)
        else: 
            raise Exception('Bad API Response Code')

    return df
