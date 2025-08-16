import yfinance as yf
import pandas as pad

def get_stock_data(ticker,period = "1mo",interval = "1d"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period = period , interval = interval)
    hist.reset_index(inplace=True)
    data =[]
    for _, row in hist.iterrows():
        data.append({
            "date":row["Date"].strftime("%Y-%m-%d"),
            "close":round(row["Close"],2) #gives the closing price


        })
    return data

if __name__ == "__main__":
    print(get_stock_data('TSLA'))

