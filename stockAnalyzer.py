from datetime import datetime

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
    time_series = input("Enter time series (1,2,3,4): ")
    if time_series in ["1","2","3","4"]:
        break
    else: print("\nInvalid Input")

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
