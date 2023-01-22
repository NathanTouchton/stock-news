# from pprint import pprint
from os import environ
from datetime import date, timedelta
from requests import get
from newsapi import NewsApiClient
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": "TSLA",
    "apikey": environ["STOCK_KEY"],
}

STOCK_ENDPOINT = get("https://www.alphavantage.co/query", params=STOCK_PARAMS)
STOCK_ENDPOINT.raise_for_status()

account_sid = environ["TWILIO_SID"]
auth_token = environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

NEWS_ENDPOINT = NewsApiClient(api_key=environ["NEWS_KEY"])

all_articles = NEWS_ENDPOINT.get_everything(
    q='tesla',
    sources='reuters,ars-technica,bloomberg',
    domains='reuters.com,arstechnica.com,bloomberg.com',
    from_param='2023-01-12',
    to='2023-01-18',
    language='en',
    sort_by='relevancy',
    page=1,
)

# pprint(all_articles["articles"][0:3])
# pprint(STOCK_ENDPOINT.json()["Time Series (Daily)"])

NUMBER_OF_DAYS_YESTERDAY = 0
NUMBER_OF_DAYS_TODAY = 0

CHECKING_FOR_DATA_YESTERDAY = True
CHECKING_FOR_DATA_TODAY = True

while CHECKING_FOR_DATA_YESTERDAY is True:
    try:
        NUMBER_OF_DAYS_YESTERDAY += 1
        YESTERDAY = date.today() - timedelta(days=NUMBER_OF_DAYS_YESTERDAY)
        YESTERDAY_PRICE = float(STOCK_ENDPOINT.json()["Time Series (Daily)"][f"{YESTERDAY}"]["4. close"])

    except KeyError:
        continue
    else:
        CHECKING_FOR_DATA_YESTERDAY = False
    break

while CHECKING_FOR_DATA_TODAY is True:
    try:
        NUMBER_OF_DAYS_TODAY += 1
        TODAY = date.today() - timedelta(days=NUMBER_OF_DAYS_TODAY)
        TODAY_PRICE = float(STOCK_ENDPOINT.json()["Time Series (Daily)"][f"{TODAY}"]["1. open"])

    except KeyError:
        continue
    else:
        CHECKING_FOR_DATA_TODAY = False
    break



CHANGE_PERCENT = YESTERDAY_PRICE/TODAY_PRICE*100
# CHANGE_PERCENT = 90

if CHANGE_PERCENT <= 95 or CHANGE_PERCENT >= 105:
    ARTICLES = all_articles["articles"][0:3]
    ARTICLE_ONE_TITLE = all_articles["articles"][0]["title"]
    ARTICLE_ONE_DESCRIPTION = all_articles["articles"][0]["description"]
    ARTICLE_TWO_TITLE = all_articles["articles"][1]["title"]
    ARTICLE_TWO_DESCRIPTION = all_articles["articles"][1]["description"]
    ARTICLE_THREE_TITLE = all_articles["articles"][2]["title"]
    ARTICLE_THREE_DESCRIPTION = all_articles["articles"][2]["description"]

    message = client.messages.create(
    body=f"{ARTICLE_ONE_TITLE}\n{ARTICLE_ONE_DESCRIPTION}",
    from_="+19894742866",
    to="+12244062483"
    )
    message = client.messages.create(
    body=f"{ARTICLE_TWO_TITLE}\n{ARTICLE_TWO_DESCRIPTION}",
    from_="+19894742866",
    to="+12244062483"
    )
    message = client.messages.create(
    body=f"{ARTICLE_THREE_TITLE}\n{ARTICLE_THREE_DESCRIPTION}",
    from_="+19894742866",
    to="+12244062483"
    )

# pprint(YESTERDAY_PRICE)
# pprint(TODAY_PRICE)
