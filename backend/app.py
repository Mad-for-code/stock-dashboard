from flask import Flask, render_template, jsonify , request
from .services.stock_service import get_stock_data

# 1️⃣ Create Flask app instance
app = Flask(__name__, static_folder="static", template_folder="static")

# 2️⃣ Home route
@app.route("/")
def home():
    return render_template("index.html")

# companies route
@app.route("/companies")
def get_companies():
    companies = [
        {"ticker": "AAPL", "name": "Apple Inc."},
        {"ticker": "MSFT", "name": "Microsoft Corp."},
        {"ticker": "GOOGL", "name": "Alphabet Inc."},
        {"ticker": "TSLA", "name": "Tesla Inc."},
        {"ticker": "AMZN", "name": "Amazon.com Inc."},
        {"ticker": "META", "name": "Meta Platforms"},
        {"ticker": "NFLX", "name": "Netflix Inc."},
        {"ticker": "NVDA", "name": "NVIDIA Corp."},
        {"ticker": "JPM", "name": "JPMorgan Chase & Co."},
        {"ticker": "V", "name": "Visa Inc."}
    ]
    return jsonify(companies)

# 3️⃣ Prices route
@app.route("/prices")
def get_prices():
    """
    Returns historical stock data for a given ticker.
    Example: /prices?ticker=AAPL&period=1mo
    """
    ticker = request.args.get("ticker")
    period = request.args.get("period", "1mo")   # default: 1 month
    interval = request.args.get("interval", "1d")  # default: 1 day

    if not ticker:
        return jsonify({"error": "Missing 'ticker' parameter"}), 400

    data = get_stock_data(ticker, period=period, interval=interval)
    return jsonify(data)


# 3️⃣ Run the app
if __name__ == "__main__":
    app.run(debug=True)
