from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

# --------------------
# Basic routes
# --------------------
@app.route('/')
def home():
    return render_template('index.html')


# --------------------
# Database connection with render postgred: this is step 3!!!
# step 1 is to create the postgred in render.com and get the URL of your database. 
# Step 2 is to use another python code to pull your local csv data into the render.com postgred using again DATABASE_URL. 
# --------------------
def get_db_connection():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(
        DATABASE_URL,
        sslmode="require"
    )
    return conn


# --------------------
# Data description page: you can customize the select texts of database based on the column you have
# --------------------
@app.route('/data_description')
def show_data():
    conn = get_db_connection()
    cur = conn.cursor()

    # Get the first row only (for demo)
    cur.execute("SELECT title, animal, book_cover_image FROM animal LIMIT 1;")
    row = cur.fetchone()

    cur.close()
    conn.close()

    # Convert row to dict for template
    data = {
        "title": row[0],
        "animal": row[1],
        "book_cover_image": row[2]
    }

    return render_template("data_description.html", data=data)


# --------------------
# Run app
# --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
