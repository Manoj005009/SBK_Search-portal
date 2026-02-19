import os
import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

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

# ✅ Use DATABASE_URL (Render Best Practice)
def get_db_connection():
    database_url = os.environ.get("DATABASE_URL")  # ✅ correct key name

    if not database_url:
        raise Exception("DATABASE_URL is missing in Render Environment!")

    return psycopg2.connect(database_url)
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    user_id = request.args.get("query")

    if not user_id:
        return render_template("result.html", user=None)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()

        user = None
        if row:
            columns = [desc[0] for desc in cursor.description]
            user = dict(zip(columns, row))

            token = user.get("token")
            user["content"] = token_content.get(token, "No Content Assigned")

        cursor.close()
        conn.close()

        return render_template("result.html", user=user)

    except Exception as e:
        return f"Database Error: {e}"

