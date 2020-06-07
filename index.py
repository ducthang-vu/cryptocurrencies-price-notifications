import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime
import time


class Notification:
    def __init__(self):
        self.coinMarket_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        with open('assets/coinMarket_api_key.txt', 'r') as filename:
            self.coinMarket_api_key = filename.read()
        self.upper_limit = 9400.00
        with open('assets/ifttt_webhook_url.txt', 'r') as filename:
            self.iftt_url = filename.read()

    def get_quote(self):
        parameters = {
            'id': '1',
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.coinMarket_api_key,
        }
        session = requests.Session()
        session.headers.update(headers)
        try:
            response = session.get(self.coinMarket_url, params=parameters)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        return data['data']['1']['quote']['USD']['price']

    def post(self, event, value):
        data = {'value1': value}
        date = datetime.now()
        requests.post(self.iftt_url.format(event), json=data)

    def format_bitcoin_history(self, bitcoin_history):
        rows = []
        for bitcoin_price in bitcoin_history:
            date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
            price = bitcoin_price['price']
            row = '{}: $<b>{}</b>'.format(date, price)
            rows.append(row)
        return '<br>'.join(rows)

    def main(self):
        bitcoin_history = []
        while True:
            price = self.get_quote()
            date = datetime.now()
            bitcoin_history.append({'date': date, 'price': price})
            print(price)
            if price > self.upper_limit:
                self.post('bitcoin_price_emergency', price)
            if len(bitcoin_history) == 5:
                print(self.format_bitcoin_history(bitcoin_history))
                self.post('bitcoin_price_update', self.format_bitcoin_history(bitcoin_history))
                bitcoin_history = []
            time.sleep(300)


notification = Notification()
notification.main()
