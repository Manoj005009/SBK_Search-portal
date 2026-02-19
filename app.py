import os
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# ✅ Database Connection using Environment Variables
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME")
)

cursor = db.cursor(dictionary=True)

# 🔥 TOKEN → CONTENT Mapping
token_content = {
    1: "CYBERCRIME AND DIGITAL INVESTIGATION",
    2: "BANKING AND FINANCE",
    3: "POWER SAVING TECHNIQUES IN COMPUTERS",
    4: "CYBERCRIME AND DIGITAL INVESTIGATION",
    5: "BANKING AND FINANCE",
    6: "POWER SAVING TECHNIQUES IN COMPUTERS",
    7: "CYBERCRIME AND DIGITAL INVESTIGATION",
    8: "BANKING AND FINANCE",
    9: "POWER SAVING TECHNIQUES IN COMPUTERS",
    10: "CYBERCRIME AND DIGITAL INVESTIGATION",
    11: "BANKING AND FINANCE",
    12: "POWER SAVING TECHNIQUES IN COMPUTERS",
    13: "CYBERCRIME AND DIGITAL INVESTIGATION",
    14: "BANKING AND FINANCE",
    15: "POWER SAVING TECHNIQUES IN COMPUTERS",
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    user_id = request.args.get("query")

    if not user_id:
        return render_template("result.html", user=None)

    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        token = user.get("token")
        user["content"] = token_content.get(token, "No Content Assigned")

    return render_template("result.html", user=user)


# ❌ No app.run() needed (Gunicorn will handle it)
