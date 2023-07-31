from dotenv import load_dotenv
import os
import requests
from sms_ir import SmsIr

load_dotenv()
stock_name = os.getenv('STOCK_NAME')
company_name = os.getenv('COMPANY_NAME')
stock_endpoint = os.getenv('STOCK_ENDPOINT')
news_endpoint = os.getenv('NEWS_ENDPOINT')
alpha_vantage_api_key = os.getenv('ALPHAVANTAGE_API_KEY')
news_api_key = os.getenv('NEWS_API_KEY')
sms_api_key = os.getenv('SMS_API_KEY')
sms_line_number = os.getenv('SMS_LINE_NUMBER')
sms_to_number = os.getenv('SMS_TO_NUMBER')

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": stock_name,
    "apikey": alpha_vantage_api_key
}


def get_news():
    parameters = {
        "q": stock_name,
        "from": stock_name,
        "sortBy": "popularity",
        "apiKey": news_api_key
    }
    response = requests.get(news_endpoint, params=parameters)
    response.raise_for_status()
    news_data = response.json()["articles"]
    first_three_news = news_data[:3]
    return (first_three_news)


response = requests.get(stock_endpoint, params=parameters)
response.raise_for_status()
stock_data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in stock_data.items()]
yesterday_data = data_list[0]['4. close']
day_before_yesterday_data = data_list[1]['4. close']

difference = abs(float(yesterday_data) - float(day_before_yesterday_data))
difference_percentage = (difference / float(yesterday_data)) * 100
if difference_percentage > 4:
    up_down = None
    news = get_news()
    if difference_percentage >= 0:
        up_down = "🔺"
    else:
        up_down = "🔻"

    formatted_news = [
        f"{stock_name} {up_down}:{int(difference_percentage)}%. \nHeadline: {item['title']}\nBrief: {item['description']}"
        for item in news]

    for item in formatted_news:
        sms_ir = SmsIr(
            sms_api_key,
            sms_line_number,
        )
        sms_ir.send_sms(
            sms_to_number,
            item,
            sms_line_number,
        )
