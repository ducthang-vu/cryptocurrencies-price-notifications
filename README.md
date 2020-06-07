# cryptocurrencies-price-notifications
cryptocurrencies-price-notifications is a simple python script which retrieve the bitcoin price in USD every 5 minutes 
and send notifications on Telegram (https://web.telegram.org/) and also, optionally, on phone.

Future version of the script will track other cryptocurrencies.

## FEATURES
Cryptocurrencies quotes are retrieve from the [CoinMarketCap API](https://coinmarketcap.com/api/).
The script will at the start of the script, and then every 5 minutes, get the current bitcoin price in USD dollar.  

Two kind of notifications are then sent by using the automation website [IFTTT](https://ifttt.com/). Both applets use 
the "webhooks" and the "notification" service.

After 5 retrieves, that is to say every 25 minutes, a notification will be sent to a Telegram channel with the last 5 
quotes.

At the beginning of the program, the user is require to activate notification on phone, in case the bitcoin price surges 
or falls to a certain upper and lower limit. If the user activate this notification, he will be require to set these 
upper and lower values. 

The notification will be fire only once. 

In order to end the execution of the program, the user must manually terminate the script. In this case the last values 
retrieves but not already notified on Telegram channel shall be sent to the channel.


## Usage
Download the repository and execute index.py.

The [Requests](https://requests.readthedocs.io/en/master/) library must be installed. 


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.