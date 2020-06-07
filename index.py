import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime
import time
import pyinputplus as pyip


def set_config(current=None):
    new_upper_limit = pyip.inputNum('Enter new upper limit: > ', greaterThan=current)
    new_lower_limit = pyip.inputNum('Enter new lower limit: > ', lessThan=current)
    with open('config/config.json') as config_file:
        config = json.load(config_file)
    config['upper_limit'] = new_upper_limit
    config['lower_limit'] = new_lower_limit
    with open('config/config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)


class Notification:
    def __init__(self):
        self.coinMarket_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        with open('config/config.json') as config_file:
            config = json.load(config_file)
        self.coinMarket_api_key = config['coinMarket_api_key']
        self.iftt_url = config['iftt_webhook_url']
        self.lower_limit = config['lower_limit']
        self.upper_limit = config['upper_limit']
        self.is_active_limit_notification = False
        self.bitcoin_history = []

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
        data = None
        try:
            response = session.get(self.coinMarket_url, params=parameters)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        return data['data']['1']['quote']['USD']['price']

    def post(self, event, value):
        data = {'value1': value}
        requests.post(self.iftt_url.format(event), json=data)

    def format_bitcoin_history(self):
        rows = []
        for bitcoin_price in self.bitcoin_history:
            date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
            price = bitcoin_price['price']
            row = '{}: $<b>{}</b>'.format(date, price)
            rows.append(row)
        return '<br>'.join(rows)

    def notify(self):
        while True:
            price = self.get_quote()
            date = datetime.now()
            self.bitcoin_history.append({'date': date, 'price': price})
            print(price)
            if self.is_active_limit_notification:
                if price >= self.upper_limit or price <= self.lower_limit:
                    self.post('bitcoin_price_emergency', price)
            if len(self.bitcoin_history) == 5:
                self.post('bitcoin_price_update', self.format_bitcoin_history())
                self.bitcoin_history = []
            time.sleep(300)

    def start(self):
        current_quote = self.get_quote()
        print('''Welcome to CryptoCurrencies App
        Current bitcoin quote is: $ {}\n
        '''.format(current_quote))
        user_choice_notif = pyip.inputYesNo('Do you want to activate notifications on Telegram when bitcoin surges or '
                                            'falls to a upper and lower limit? (Y/N) > ')
        if user_choice_notif == 'yes':
            print('The current limits are:\n\tupper limit: $ {}\n\tlower limit: $ {}'.format(self.upper_limit,
                                                                                             self.lower_limit))
            user_choice_conf = pyip.inputYesNo('Do you want to modify any of these parameters? (Y/N) > ')
            if user_choice_conf == 'yes':
                set_config(current_quote)
            self.is_active_limit_notification = True
        try:
            self.notify()
        except KeyboardInterrupt:
            self.post('bitcoin_price_update', self.format_bitcoin_history())
            print('Script interrupted')


if __name__ == '__main__':
    notification = Notification()
    notification.start()
