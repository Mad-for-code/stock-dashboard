import yfinance as yf
import pandas as pd

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

def get_stock_stats(ticker):
    """
    Returns 52-week high, 52-week low, avg volume for a stock
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")  # 1 year data

    if hist.empty:
        return {}

    high_52 = hist["Close"].max()
    low_52 = hist["Close"].min()
    avg_volume = hist["Volume"].mean()

    return {
        "ticker": ticker,
        "high_52week": round(high_52, 2),
        "low_52week": round(low_52, 2),
        "avg_volume": round(avg_volume, 2)
    }

def get_technical_indicators(ticker, period="3mo", interval="1d"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)

    if hist.empty:
        return []

    # SMA 20-day
    hist["SMA_20"] = hist["Close"].rolling(window=20).mean()

    # EMA 20-day
    hist["EMA_20"] = hist["Close"].ewm(span=20, adjust=False).mean()

    # RSI 14-day
    delta = hist["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    # Prevent division by zero
    rs = avg_gain / avg_loss.replace(0, 1)
    hist["RSI"] = 100 - (100 / (1 + rs))

    hist.reset_index(inplace=True)

    indicators = []
    for _, row in hist.iterrows():
        indicators.append({
            "date": row["Date"].strftime("%Y-%m-%d"),
            "SMA_20": float(row["SMA_20"]) if pd.notna(row["SMA_20"]) else None,
            "EMA_20": float(row["EMA_20"]) if pd.notna(row["EMA_20"]) else None,
            "RSI": float(row["RSI"]) if pd.notna(row["RSI"]) else None
        })


    return indicators



if __name__ == "__main__":
    print(get_stock_data('TSLA'))
