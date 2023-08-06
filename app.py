from flask import Flask, request, redirect, url_for, render_template
app = Flask(__name__)
from db import *
import datetime

@app.route('/')
def home(items=[]):
    if len(items)<1:
        items=todict()
    return render_template('home.html', tasks = sorted(items, key = lambda i:i['date']))

@app.route('/search')
def search():
    category = request.args['category']
    description = request.args['description']
    date = request.args['date']
    results = todict(f'SELECT * FROM tasks WHERE category LIKE "%{category}%" AND description LIKE "%{description}%" AND date LIKE "%{date}%"')
    return home(items = results)

@app.route('/postAdd')
def postAdd():
    category = request.args['category']
    description = request.args['description']
    day = request.args['day']
    month = request.args['month']
    year = request.args['year']
    date = f"{day}/{month}/{year}"
    query(f"INSERT INTO tasks (category, description, date) VALUES ('{category}','{description}','{date}')")
    return redirect(url_for('home'))

@app.route('/add')
def add():        
    return render_template('add.html')

@app.route('/update')
def update():
    tid=request.args["tid"]
    task=todict(f"SELECT * from tasks where tid={tid}")
    return render_template("update.html", task=task[0])
    
@app.route('/post_update')
def post_update():
    tid=request.args["tid"]
    category=request.args["category"]
    description=request.args["description"]
    day=request.args["day"]
    month = request.args["month"]
    year = request.args["year"]
    date = f"{day}/{month}/{year}"
    query(f"UPDATE tasks SET category='{category}', description='{description}', date='{date}' WHERE tid='{tid}'")
    return redirect(url_for('home'))

@app.route('/delete')
def delete():
    tid = request.args['tid']
    query(f'DELETE FROM tasks WHERE tid={tid}')
    return redirect(url_for('home'))


