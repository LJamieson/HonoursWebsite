import sqlite3
from functools import wraps
from flask import Flask, redirect, render_template, request, session, url_for, g

app = Flask(__name__)
app.secret_key = 'X9YEm3bxpoV73jQnhxvplmMNk6rGqO4d'

@app.route('/')
def home():
    return render_template('homepage.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)