from pprint import pprint
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import traceback
import jwt
import bcrypt
from dotenv import load_dotenv
import os
from flask_cors import CORS
from smtplib import SMTP_SSL

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


def secured_route(route_func):
    def check_token():
        token = request.cookies.get('token')
        if token == None:
            return redirect(url_for('login'), code=401)
        return route_func(token)
    return check_token


@app.route('/')
def home():
    return render_template('index.html', name="Davin", curr_date=current_date, title="Home")


@app.route('/register')
def register():
    return render_template('register.html', curr_date=current_date, title="Register")


@app.route('/login')
def login():
    return render_template('login.html', curr_date=current_date, title="Login")


@app.route('/main')
@secured_route
def main(token):
    token_data = jwt.decode(token, JWT_SECRET, "HS256")
    user_data = {
        "username": token_data["username"], "email": token_data["email"]}
    return render_template('main.html', curr_date=current_date, title=f"Welcome {user_data['email'].upper()}", user_data=user_data)


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
                    # This code sends an email to user upon registration using email provided
                    server = SMTP_SSL('smtp.gmail.com', 465)
                    server.ehlo()
                    server.login(GMAIL_USER, GMAIL_PASSWORD)
                    server.sendmail(
                        GMAIL_USER, data["email"], f"Subject: Welcome to the Bank {data['username']}!\nThis is a test.")
                except:
                    traceback.print_exc()
                    print("Error sending email")
                # Creates JSON web token to be used to identify user on client side
                token = jwt.encode(
                    {"username": data["username"], "email": data["email"]}, JWT_SECRET, "HS256")
                return {"success": True, "token": token}, 200
            except:
                pprint(traceback.format_exc())
                return {"success": False, "error": traceback.format_exc()}, 500
    except KeyError:
        return {"success": False, "error": "Please include username, email, and password in request json body."}, 400


@app.route('/api/login', methods=["POST"])
def login_user():
    data = request.json
    sql = f"SELECT * from users WHERE username = '{data['username']}'"
    res = cur.execute(sql)
    user_data = res.fetchall()
    if user_data == []:
        return {"success": False, "error": "No user found with that username"}, 400
    user = {"username": user_data[0][1],
            "email": user_data[0][2], "password": user_data[0][3]}
    if bcrypt.checkpw(data['password'].encode('utf-8'), user["password"].encode('utf-8')):
        token = jwt.encode(
            {"username": user["username"], "email": user["email"]}, JWT_SECRET, "HS256")
        return {"success": True, "token": token}
    else:
        return {"success": False, "error": "Incorrect password, please try again"}, 400


if __name__ == '__main__':
    app.run(debug=True, port=3000)
