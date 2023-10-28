import requests
import pygal
import html
from datetime import datetime
from xml.sax.saxutils import unescape

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
api_key = 'YOUR_API_KEY'  # Replace with your actual Alpha Vantage API key

params = {
    'function': 'TIME_SERIES_' + ['INTRADAY', 'DAILY', 'WEEKLY', 'MONTHLY'][int(time_series) - 1],
    'symbol': stock_symbol,
    'apikey': api_key,
}

response = requests.get(base_url, params=params)
data = response.json()

# Extract data for the chart
if 'Time Series (Daily)' in data:
    time_series_data = data['Time Series (Daily)']
    time_series_label = 'Daily'

elif 'Time Series (15min)' in data:
    time_series_data = data['Time Series (15min)']
    time_series_label = '15-Min'

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





