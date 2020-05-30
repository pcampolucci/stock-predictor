import yfinance as yf

import datetime

currentDT = datetime.datetime.now()
pastDT = currentDT - datetime.timedelta(days=7)

currentDT = str(currentDT)[:10]
pastDT = str(pastDT)[:10]

msft = yf.Ticker("MSFT")

data = yf.download("msft", start=pastDT, end=currentDT, interval="1m")

print(data)

