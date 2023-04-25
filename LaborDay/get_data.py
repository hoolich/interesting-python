import requests
import pandas as pd
import simplejson
from pymongo import MongoClient
import urllib.request

class DataCrawler(object):
    def __init__(self):
        self.cities = list(pd.read_csv('city_data.csv')['city'])
        client = MongoClient(host='localhost', port=12777)
        db = client.Laborday
        self.col = db.ticket

    def get_city_trip(self):
        url = 'https://travelsearch.fliggy.com/index.htm?spm=181.61408.a1z7d.4.7e8b5e9ezgTbCg&searchType=product&keyword={}&category=SCENIC&ttid=seo.000000576'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36'}
        for city in self.cities:
            print('正在爬取城市:{}的数据!'.format(city))
            try:
                res = requests.get(url.format(city))
                # print(res.text)
                data = res.json()
                print(data)
            except simplejson.errors.JSONDecodeError:
                print('无法 decode response:')
                # print(res.text)

        # itemPagenum = data['data']['data'].get('itemPagenum')
            # if itemPagenum is not None:
            #     page_count = itemPagenum['data']['count']
            #
            #     data_list = data['data']['data']['itemProducts']['data']['list'][0]['auctions']
            #     for ticket in data_list:
            #         ticket['city'] = city
            #         self.col.insert_one(ticket)
            #     print('成功爬取城市:{}的第{}页数据!'.format(city, 1))
            #
            #     if page_count > 1:
            #         for page in range(2, page_count+1):
            #             res = requests.get('https://travelsearch.fliggy.com/async/queryItemResult.do?searchType='
            #                                'product&keyword={}&category=SCENIC&pagenum={}'.format(city, page))
            #             data = res.json()
            #             data_list = data['data']['data']['itemProducts']['data']['list'][0]['auctions']
            #             for ticket in data_list:
            #                 ticket['city'] = city
            #                 self.col.insert_one(ticket)
            #             print('成功爬取城市:{}的第{}页数据!'.format(city, page))


if __name__ == '__main__':
    data_crawler = DataCrawler()
    data_crawler.get_city_trip()
