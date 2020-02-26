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


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search = request.form['vElemSearch']
        return search_results(search)
    return render_template('homepage.html')

@app.route('/results/<vElemSearch>', methods=['GET', 'POST'])
def search_results(vElemSearch):
    db = get_db()
    data = db.cursor().execute('SELECT entry FROM animals WHERE entry LIKE "'+vElemSearch+'"')
    dElems = data.fetchall()
    if request.method == 'POST':
        search = request.form['vElemSearch']
        return search_results(search)
    return render_template('results.html', vElems=dElems)

@app.route('/entry/')
def entry():
    db = get_db()
    records = [(1,"Labrador", "Canine", "10-14 Years", "Dog"), (2, "Pomeranian", "Canine", "12-16 Years", "Dog"),(3, "Highland-Cattle", "Bovidae", "20 Years", "Cattle")]
    db.cursor().executemany('insert into animals values (?,?,?,?,?);',records);
    db.commit()
    #data = db.cursor().execute('SELECT * FROM animals WHERE entry = "Labrador"')
    #dElems = data.fetchall()
    return render_template('homepage.html')#, vElems=dElems)

@app.route('/species', methods=['GET', 'POST'])
def species():
    db = get_db()
    data = db.cursor().execute('SELECT entry FROM animals')
    dElems = data.fetchall()
    if request.method == 'POST':
        search = request.form['vElemSearch']
        return search_results(search)
    return render_template('speciespage.html', vElems=dElems)

@app.route('/species/<vEntry>', methods=['GET', 'POST'])
def vEntry_page(vEntry):
    db = get_db()
    data = db.cursor().execute('SELECT * FROM animals WHERE entry = "'+(vEntry).lower().title()+'"')
    dElems = data.fetchall()
    if request.method == 'POST':
        search = request.form['vElemSearch']
        return search_results(search)
    return render_template('entrypage.html', vElems=dElems)

@app.errorhandler(404, methods=['GET', 'POST'])
def page_not_found(error):
    if request.method == 'POST':
        search = request.form['vElemSearch']
        return search_results(search)
    return render_template('errorpage.html'), 404



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
