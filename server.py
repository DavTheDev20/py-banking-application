from http import server
from pprint import pprint
import smtpd
from flask import Flask, render_template, jsonify, request, g
import sqlite3
from datetime import datetime
import traceback
import jwt
import bcrypt
from dotenv import load_dotenv
import os
from flask_cors import CORS
from smtplib import SMTP, SMTP_SSL

load_dotenv()

app = Flask(__name__)
CORS(app)

SQL_DATABASE = "./db/main.db"
JWT_SECRET = os.environ["JWT_SECRET"]
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_PASSWORD = os.environ["GMAIL_PASSWORD"]

current_date = datetime.now().strftime("%Y")

con = sqlite3.connect(SQL_DATABASE, check_same_thread=False)
cur = con.cursor()


def create_users_table():
    """Creates SQL database table to store users"""
    sql = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, email TEXT UNIQUE, password TEXT)"
    cur.execute(sql)


create_users_table()


@app.route('/')
def home():
    return render_template('index.html', name="Davin", curr_date=current_date, title="Home")


@app.route('/register')
def register():
    return render_template('register.html', curr_date=current_date, title="Register")


@app.route('/api/register', methods=["POST"])
def register_user():
    data = request.json
    try:
        if data["username"] and data["email"] and data["password"]:
            hashed_password = str(bcrypt.hashpw(
                data["password"].encode("utf-8"), bcrypt.gensalt()), "utf-8")
            sql = f"INSERT INTO users (username, email, password) VALUES ('{data['username']}', '{data['email']}', '{hashed_password}')"
            try:
                cur.execute(sql)
                con.commit()
                try:
                    server = SMTP_SSL('smtp.gmail.com', 465)
                    server.ehlo()
                    server.login(GMAIL_USER, GMAIL_PASSWORD)
                    server.sendmail(
                        GMAIL_USER, data["email"], f"Subject: Welcome to the Bank {data['username']}!\nThis is a test.")
                except:
                    traceback.print_exc()
                    print("Error sending email")
                token = jwt.encode(
                    {"username": data["username"], "email": data["email"]}, JWT_SECRET, "HS256")
                return {"success": True, "token": token}, 200
            except:
                pprint(traceback.format_exc())
                return {"success": False, "error": traceback.format_exc()}, 500
    except KeyError:
        return {"success": False, "error": "Please include username, email, and password in request json body."}, 400


@app.route('/user/<user_id>')
def user_page(user_id):
    # Route used to show user their banking information.
    pass


if __name__ == '__main__':
    app.run(debug=True, port=3000)
