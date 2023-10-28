import requests
import pygal
from datetime import datetime

# Get user input
# Stock symbol
stock_symbol = input("Enter the stock symbol: ")

# Chart type (Bar or Line)
while True:
    print("\nChart Types\n----------------\n1) Bar\n2) Line\n")
    chart_type = input("Enter 1 for Bar chart, 2 for Line chart: ")
    if chart_type in ["1", "2"]:
        break
    else:
        print("\nInvalid input\n")

# Time series function (Intraday, Daily, Weekly, Monthly)
while True:
    print("\nTime Series\n--------------------------------\n1) Intraday\n2) Daily\n3) Weekly\n4) Monthly\n")
    time_series = input("Enter time series (1, 2, 3, 4): ")
    if time_series in ["1", "2", "3", "4"]:
        break
    else:
        print("\nInvalid input\n")

# Start date
while True:
    start_date = input("\nEnter the start date (YYYY-MM-DD): ")
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        break
    except ValueError:
        print("\nInvalid date format. Please use YYYY-MM-DD format.")

# End date
while True:
    end_date = input("\nEnter the end date in YYYY-MM-DD format: ")
    try:
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        if end_date_obj >= datetime.strptime(start_date, '%Y-%m-%d'):
            break
        else:
            print("The end date should not be before the begin date.")
    except ValueError:
        print("\nInvalid date format. Please use YYYY-MM-DD format.")

# Send the user input to the Alpha Vantage API
base_url = "https://www.alphavantage.co/query"
api_key = 'CRF5E6TEAFQOQWZY'  # Replace with your actual Alpha Vantage API key

params = {
    'function': ['TIME_SERIES_INTRADAY', 'TIME_SERIES_DAILY', 'TIME_SERIES_WEEKLY', 'TIME_SERIES_MONTHLY'][int(time_series) - 1],
    'symbol': stock_symbol,
    'apikey': api_key,
}

response = requests.get(base_url, params=params)
data = response.json()

# Map time series options to their keys in the JSON response
time_series_options = {
    '1': 'Time Series (15min)',  # Intraday
    '2': 'Time Series (Daily)',
    '3': 'Weekly Time Series',
    '4': 'Monthly Time Series'
}

selected_time_series = time_series_options[time_series]

if selected_time_series in data:
    time_series_data = data[selected_time_series]
    time_series_label = ['Intraday', 'Daily', 'Weekly', 'Monthly'][int(time_series) - 1]
else:
    print("Selected time series data not found in response.")
    exit()

# Prepare data for the chart
dates = []
prices = []

for date, info in time_series_data.items():
    if start_date <= date <= end_date:
        dates.append(date)
        prices.append(float(info['4. close']))

dates.reverse()
prices.reverse()

# Generate the chart
chart = pygal.Line(x_label_rotation=20)
chart.title = f'{stock_symbol} Stock Prices ({time_series_label})'

if time_series_label == 'Intraday':
    chart.y_title = 'Price (USD)'
else:
    chart.y_title = 'Close Price (USD)'

chart.x_labels = dates
chart.add('Close Price', prices)

# Function to generate HTML content for the chart
def generate_html_content(chart):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
    {}
    </body>
    </html>
    """.format(chart.render())
    return html_content

# Open the chart in the default web browser
with open("stock_chart.html", "w") as html_file:
    html_content = generate_html_content(chart)
    html_file.write(html_content)

# Optionally, open the HTML chart in the default web browser
import webbrowser
webbrowser.open('stock_chart.html')
   
