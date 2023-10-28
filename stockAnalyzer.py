from datetime import datetime
import requests
from lxml import html
import pygal
import webbrowser

#Get user input-------------------

#get stock symbol
stock_symbol = input("Enter the stock symbol: ")

#get chart type, line or bar
while True:
    print("\nChart Types\n ----------------\n 1) Bar \n 2) Line\n")
    chart_type = input("Enter 1 for Bar chart, 2 for Line chart: ")
    if chart_type in ["1", "2"]:
        break
    else:
        print("\nInvalid input\n")

#get time series function, intraday, daily, weekly, or monthly
while True:
    print("\nTime Series \n--------------------------------\n 1) Intraday\n 2) Daily\n 3) Weekly\n 4) Monthly\n")
    u_time_series = input("Enter time series (1,2,3,4): ")
    if u_time_series in ["1","2","3","4"]:
        break
    else: print("\nInvalid Input")


if u_time_series == "1":
    time_series = "TIME_SERIES_INTRADAY"
if u_time_series == "2":
    time_series = "TIME_SERIES_DAILY"
if u_time_series == "3":
    time_series = "TIME_SERIES_WEEKLY"
if u_time_series == "2":
    time_series = "TIME_SERIES_MONTHLY"


#get start date
while True:
    start_date = input("\nEnter the start date (YYYY-MM-DD): ")
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        break
    except ValueError:
        print("\nInvalid date format. Please use YYYY-MM-DD format.")


#get end date
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


#----user input is gathered, to be sent to API ------------
print(stock_symbol, chart_type, time_series, start_date, end_date)



api_key = 'K1Q8KTQTHI47M38M'

url = f'https://www.alphavantage.co/query?function={time_series}&symbol={stock_symbol}&apikey={api_key}'

response = requests.get(url)
data = response.json()
print(data)

# Parse the API response
tree = html.fromstring(response.text)

closing_prices = []

#-----------------------------------------------------------------------------------------------------------------------------------------
# Below needs updated to work dynamically with intra day, daily, weekly, and monthly. I think we just need to change data['Time Series (Daily)'] 
# to a variable that is the correct string based what user input was
#-----------------------------------------------------------------------------------------------------------------------------------------

for date, values in data['Time Series (Daily)'].items():
    closing_prices.append(float(values['4. close']))

print(closing_prices)


#-----------------------------------------------------------------------------------------------------------------------------------------
#Needs to check variable chart_type to see if bar chart or line chart should be rendered, the code below makes a line chart successfully
#-----------------------------------------------------------------------------------------------------------------------------------------


# Create a line chart
chart = pygal.Line()
chart.title = f'{stock_symbol} Stock Prices'
chart.x_labels = reversed([str(i) for i in range(1, len(closing_prices) + 1)])
chart.add('Closing Price', [float(price) for price in closing_prices])



#-----------------------------------------------------------------------------------------------------------------------------------------
# Render the chart to an SVG file
chart.render_to_file('stock_chart.svg')


webbrowser.open('stock_chart.svg')
