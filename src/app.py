import pyupbit

df = pyupbit.get_ohlcv("KRW-BTC", interval='day1', count=365)
print(df)
