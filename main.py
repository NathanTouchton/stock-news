# from pprint import pprint
from os import environ
from datetime import date, timedelta
from requests import get

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": "TSLA",
    "apikey": environ["STOCK_KEY"],
}

STOCK_ENDPOINT = get("https://www.alphavantage.co/query", params=STOCK_PARAMS)
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_ENDPOINT.raise_for_status()

NUMBER_OF_DAYS = 0

CHECKING_FOR_DATA = True

while CHECKING_FOR_DATA is True:
    try:
        NUMBER_OF_DAYS += 1
        YESTERDAY = date.today() - timedelta(days=NUMBER_OF_DAYS)
        YESTERDAY_PRICE = float(STOCK_ENDPOINT.json()["Time Series (Daily)"][f"{YESTERDAY}"]["4. close"])

    except KeyError:
        continue
    else:
        CHECKING_FOR_DATA = False
    break

TODAY_PRICE = float(STOCK_ENDPOINT.json()["Time Series (Daily)"][f"{date.today()}"]["1. open"])

CHANGE_PERCENT = YESTERDAY_PRICE/TODAY_PRICE*100

if CHANGE_PERCENT <= 95 or CHANGE_PERCENT >= 105:
    print("Check the news.")

# pprint(YESTERDAY_PRICE)
# pprint(TODAY_PRICE)


## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME.
#HINT 1: Think about using the Python Slice Operator



## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number.
#HINT 1: Consider using a List Comprehension.



#Optional: Format the SMS message like this:
# """
# TSLA: 🔺2%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# or
# "TSLA: 🔻5%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# """
