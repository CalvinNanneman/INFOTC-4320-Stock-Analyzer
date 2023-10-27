import requests
from datetime import datetime
import pygal
from lxml import etree

# Get user input

# Get stock symbol
stock_symbol = input("Enter the stock symbol: ")

# Get chart type, line or bar
while True:
    print("\nChart Types\n ----------------\n 1) Bar \n 2) Line\n")
    chart_type = input("Enter 1 for Bar chart, 2 for Line chart: ")
    if chart_type in ["1", "2"]:
        break
    else:
        print("\nInvalid input\n")

# Get time series function, intraday, daily, weekly, or monthly
while True:
    print("\nTime Series \n--------------------------------\n 1) Intraday\n 2) Daily\n 3) Weekly\n 4) Monthly\n")
    time_series = input("Enter time series (1,2,3,4): ")
    if time_series in ["1", "2", "3", "4"]:
        break
    else:
        print("\nInvalid Input\n")

# Get start date
while True:
    start_date = input("\nEnter the start date (YYYY-MM-DD): ")
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        break
    except ValueError:
        print("\nInvalid date format. Please use YYYY-MM-DD format.")

# Get end date
while True:
    end_date = input("\nEnter the end date in YYYY-MM-DD format: ")
    try:
        datetime.strptime(end_date, '%Y-%m-%d')
        if end_date >= start_date:
            break
        else:
            print("The end date should not be before the begin date.")
    except ValueError:
        print("\nInvalid date format. Please use YYYY-MM-DD format.")

# Generate a graph and open in the user's default browser
api_key = "NXIYN25QRQTO36XP"  # Replace with your Alpha Vantage API key

# Create the API request URL
function = ""
if time_series == "1":
    function = "TIME_SERIES_INTRADAY"
    interval = input("Enter time interval (1min, 5min, 15min, 30min, 60min): ")
else:
    if time_series == "2":
        function = "TIME_SERIES_DAILY"
    elif time_series == "3":
        function = "TIME_SERIES_WEEKLY"
    elif time_series == "4":
        function = "TIME_SERIES_MONTHLY"

url = f'https://www.alphavantage.co/query?function={function}&symbol={stock_symbol}&apikey={api_key}'

if time_series == "1":
    url += f'&interval={interval}'

# Make the API request
response = requests.get(url)
data = response.json()

# Parse the data and create a chart
dates = []
values = []

if time_series == "1":
    for timestamp, values in data["Time Series"][interval].items():
        dates.append(timestamp)
        values.append(float(values["1. open"]))

    chart = pygal.Line(x_label_rotation=20, x_labels_major_every=10)
else:
    for date, values in data["Time Series"].items():
        dates.append(date)
        values.append(float(values["4. close"]))

    if chart_type == "1":
        chart = pygal.Bar(x_label_rotation=20, x_labels_major_every=10)
    else:
        chart = pygal.Line(x_label_rotation=20, x_labels_major_every=10)

chart.title = f"{stock_symbol} Stock Price"
chart.x_labels = dates
chart.add("Price", values)

# Save the chart to an SVG file
chart.render_to_file(f"{stock_symbol}_chart.svg")

# Open the chart in the default web browser
chart.render_in_browser()


