import pygal
import requests
from lxml import html

# Function to get stock data from Alpha Vantage API
def get_stock_data(symbol, chart_type, time_series, start_date, end_date):
    api_key = 'CRF5E6TEAFQOQWZY'  # Replace with your Alpha Vantage API key
    base_url = f'https://www.alphavantage.co/query?'
    function = 'TIME_SERIES_INTRADAY' if time_series == 'intraday' else 'TIME_SERIES_DAILY'

    params = {
        'function': function,
        'symbol': symbol,
        'interval': '1d',
        'apikey': api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'Time Series (Daily)' in data:
        time_series_data = data['Time Series (Daily)']
    else:
        print("No data available for this stock symbol or time series.")
        return [], []  # Return empty lists for dates and prices when there's no data

    # Extract dates and closing prices
    dates = []
    prices = []

    for date, info in time_series_data.items():
        if start_date <= date <= end_date:
            dates.append(date)
            prices.append(float(info['4. close']))

    return dates, prices


# Function to generate and display a chart
def generate_chart(symbol, chart_type, time_series, start_date, end_date):
    dates, prices = get_stock_data(symbol, chart_type, time_series, start_date, end_date)

    if dates and prices:
        chart = pygal.Line()
        chart.title = f'{symbol} Stock Price Chart'
        chart.x_labels = dates
        chart.add('Closing Price', prices)
        chart.render_to_file('chart.svg')

def main():
    symbol = input("Enter the stock symbol for the company: ")
    chart_type = input("Enter the chart type (e.g., line, bar, etc.): ")
    time_series = input("Enter the time series function (intraday or daily): ")
    start_date = input("Enter the beginning date in YYYY-MM-DD format: ")
    end_date = input("Enter the end date in YYYY-MM-DD format: ")

    if start_date > end_date:
        print("The end date cannot be before the begin date.")
        return

    generate_chart(symbol, chart_type, time_series, start_date, end_date)

if __name__ == '__main__':
    main()
