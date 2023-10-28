import pandas as pd
from alpha_vantage.timeseries import TimeSeries

api_key = 'NXIYN25QRQTO36XP' 

# Hardcode inputs for testing
stock_symbol = 'GOOGL'
start_date = '2023-02-01' 
end_date = '2023-02-28'

# API call
ts = TimeSeries(key=api_key)
data, meta_data = ts.get_daily(symbol=stock_symbol,outputsize='full')

# Format data
df = pd.DataFrame(data)
df = df.loc[start_date:end_date]
df.index = pd.to_datetime(df.index)

# Check data
print(df.head())
print(df.dtypes) 

# Plot
df['4. close'].plot()