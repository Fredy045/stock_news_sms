import requests
from twilio.rest import Client
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
API_KEY_STOCK = os.environ.get("API_KEY_STOCK_")
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_KEY_NEWS = os.environ.get("API_KEY_NEWS_")

ACCOUNT_SID = os.environ.get("ACCOUNT_SID_")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN_")

# TODO 1. - Getting yesterday's closing stock price.

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": API_KEY_STOCK,
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_data = yesterday_data["4. close"]
print(yesterday_closing_data)

# TODO 2. - Getting the day before yesterday's closing stock price

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_data = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_data)

# TODO 3. - Finding the positive difference between 1 and 2.

difference = float(yesterday_closing_data) - float(day_before_yesterday_closing_data)
up_down = None
if difference < 0:
    up_down = "📉"
else:
    up_down = "📈"
print(difference)

# TODO 4. - Working out the percentage difference in price between closing price yesterday and closing price the day
#  before yesterday.

percentage = round((difference / float(yesterday_closing_data)) * 100)
print(percentage)

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

if percentage > 5.0:
    print("Get news")

# TODO 6. - Using the News API to get articles related to the COMPANY_NAME.

if abs(percentage) > 0:
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        # "from": "2021-11-08",
        "apiKey": API_KEY_NEWS,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]

    # TODO 7. - Using Python slice operator to create a list that contains the first 3 articles.

    three_articles = news_data[:3]

    # TODO 8. - Creating a new list of the first 3 article's headline and description using list comprehension.

    formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage}% \nHeadline: {article['title']}. "
                          f"\nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)

    # TODO 9. - Sending each article as a separate message via Twilio.

    for article in formatted_articles:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages \
            .create(
            body=article,
            from_='+13185318266',
            to='+527711940301'
        )

        print(message.status)
