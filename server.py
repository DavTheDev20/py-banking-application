from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

current_date = datetime.now().strftime("%Y")


@app.route('/')
def home():
    return render_template('index.html', name="Davin", curr_date=current_date, title="Home")


@app.route('/register')
def register():
    return render_template('register.html', curr_date=current_date, title="Register")


if __name__ == '__main__':
    app.run(debug=True)
