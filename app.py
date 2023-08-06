from flask import Flask, request, redirect, url_for, render_template
app = Flask(__name__)
from db import *
import datetime

@app.route('/')
def home(items=[]):
    if len(items)<1:
        items=todict()
    return render_template('home.html', tasks = sorted(items, key = lambda i:i['date']))

@app.route('/sa')
def sa():
    action = request.args.get('action')
    print(action)
    if action == 'search':
        category = request.args['category']
        description = request.args['description']
        date = request.args['date']
        results = todict(f'SELECT * FROM tasks WHERE category LIKE "%{category}%" AND description LIKE "%{description}%" AND date LIKE "%{date}%"')
        return home(items = results)
            
    else:
        category = request.args['category']
        description = request.args['description']
        date = request.args['date']
        query(f"INSERT INTO tasks (category, description, date) VALUES ('{request.args['category']}','{request.args['description']}','{request.args['date']}')")
        return redirect((url_for('home')))

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
    date=request.args["date"]
    query(f"UPDATE tasks SET category='{category}', description='{description}', date='{date}' WHERE tid='{tid}'")
    return redirect(url_for('home'))

@app.route('/delete')
def delete():
    tid = request.args['tid']
    query(f'DELETE FROM tasks WHERE tid={tid}')
    return redirect(url_for('home'))


