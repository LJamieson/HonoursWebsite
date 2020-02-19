import sqlite3
from functools import wraps
from flask import Flask, g,redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'X9YEm3bxpoV73jQnhxvplmMNk6rGqO4d'
db_location = './var/database.db'

def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = sqlite3.connect(db_location)
    return db

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/entry/')
def entry():
    db = get_db()
    db.cursor().execute('insert into animals(entry, family, lifeSpan, typeOf) values ("Labrador", "Canine", "10-14 Years", "Dog")')
    db.commit()
    data = db.cursor().execute('SELECT * FROM animals WHERE entry = "Labrador"')
    dElems = data.fetchall()
    return render_template('entrypage.html', vElems=dElems)

@app.route('/species/<vEntry>')
def vEntry_page(vEntry):
    db = get_db()
    data = db.cursor().execute('SELECT * FROM animals WHERE entry = "'+(vEntry).lower().title()+'"')
    dElems = data.fetchall()
    return render_template('entrypage.html', vElems=dElems)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errorpage.html'), 404



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
