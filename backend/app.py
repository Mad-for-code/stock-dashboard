from flask import Flask, render_template

# 1️⃣ Create Flask app instance
app = Flask(__name__, static_folder="static", template_folder="static")

# 2️⃣ Home route
@app.route("/")
def home():
    return render_template("index.html")

# 3️⃣ Run the app
if __name__ == "__main__":
    app.run(debug=True)
