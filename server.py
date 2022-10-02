from pprint import pprint
from flask import Flask, render_template, jsonify, request, g
import sqlite3
from datetime import datetime
import traceback
import jwt
import bcrypt

app = Flask(__name__)

SQL_DATABASE = "./db/main.db"

current_date = datetime.now().strftime("%Y")

con = sqlite3.connect(SQL_DATABASE, check_same_thread=False)
cur = con.cursor()


def create_users_table():
    """Creates SQL database table to store users"""
    sql = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT)"
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

            print(hashed_password)
            sql = f"INSERT INTO users (username, email, password) VALUES ('{data['username']}', '{data['email']}', '{hashed_password}')"
            try:
                cur.execute(sql)
                con.commit()
                return {"success": True}
            except:
                pprint(traceback.format_exc())
                return {"success": False, "error": traceback.format_exc()}
    except KeyError:
        return {"success": False, "error": "Please include username, email, and password in request json body."}, 400


@app.route('/user/<user_id>')
def user_page(user_id):
    # Route used to show user their banking information.
    pass


if __name__ == '__main__':
    app.run(debug=True)
