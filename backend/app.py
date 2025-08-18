from flask import Flask, render_template, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy
from backend.services.stock_service import get_stock_data, get_stock_stats, get_technical_indicators

# 1️⃣ Create Flask app instance
app = Flask(__name__, static_folder="static", template_folder="static")



# Database setup (MySQL)
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:PASSWORD@localhost:3306/company_db"
db_url = os.environ.get("DATABASE_URL", "mysql+pymysql://root:QwcpSRyVvqGRFFSgUudHBEVeSfipjyds@mysql.railway.internal:3306/railway")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# 2️⃣ Company Model
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    high_52week = db.Column(db.Float)
    low_52week = db.Column(db.Float)
    avg_volume = db.Column(db.Float)

# 3️⃣ Seed initial companies into DB
def seed_companies():
    initial_companies = [
        {"ticker": "AAPL", "name": "Apple Inc."},
        {"ticker": "INFY.NS", "name": "Infosys Limited"},
        {"ticker": "GOOGL", "name": "Alphabet Inc."},
        {"ticker": "TSLA", "name": "Tesla Inc."},
        {"ticker": "AMZN", "name": "Amazon.com Inc."},
        {"ticker": "META", "name": "Meta Platforms"},
        {"ticker": "NFLX", "name": "Netflix Inc."},
        {"ticker": "NVDA", "name": "NVIDIA Corp."},
        {"ticker": "JPM", "name": "JPMorgan Chase & Co."},
        {"ticker": "V", "name": "Visa Inc."}
    ]

    for comp in initial_companies:
        exists = Company.query.filter_by(ticker=comp["ticker"]).first()
        if not exists:
            db.session.add(Company(ticker=comp["ticker"], name=comp["name"]))
    db.session.commit()

# 4️⃣ Initialize DB + Seed
with app.app_context():
    db.create_all()
    seed_companies()

# 5️⃣ Home route
@app.route("/")
def home():
    return render_template("index.html")

# 6️⃣ Companies route → fetch from DB
@app.route("/companies")
def get_companies():
    companies = Company.query.all()
    return jsonify([{"ticker": c.ticker, "name": c.name} for c in companies])

# 7️⃣ Prices route
@app.route("/prices")
def get_prices():
    ticker = request.args.get("ticker")
    period = request.args.get("period", "1mo")   # default: 1 month
    interval = request.args.get("interval", "1d")  # default: 1 day

    if not ticker:
        return jsonify({"error": "Missing 'ticker' parameter"}), 400

    data = get_stock_data(ticker, period=period, interval=interval)
    return jsonify(data)

# 8️⃣ Stats route
@app.route("/stats")
def get_stats():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "Missing 'ticker' parameter"}), 400

    stats = get_stock_stats(ticker)

    # Save/update stats in DB
    company = Company.query.filter_by(ticker=ticker).first()
    if company:
        company.high_52week = stats["high_52week"]
        company.low_52week = stats["low_52week"]
        company.avg_volume = stats["avg_volume"]
    else:
        company = Company(
            ticker=ticker,
            name=ticker,  # fallback if no name
            high_52week=stats["high_52week"],
            low_52week=stats["low_52week"],
            avg_volume=stats["avg_volume"]
        )
        db.session.add(company)

    db.session.commit()
    return jsonify(stats)

# 9️⃣ Indicators route
@app.route("/indicators")
def indicators():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "Missing 'ticker' parameter"}), 400
    try:
        data = get_technical_indicators(ticker)
        return jsonify(data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# 🔟 Run the app
#if __name__ == "__main__":
   # app.run(debug=True)
