from flask import Flask, render_template, redirect, url_for, request, flash
import db 
from db import get_db
import sqlite3


app = Flask(__name__) #Application factory 
app.config ['DATABASE'] = 'mydatabase.db'

db.init_app(app)

@app.route('/')
def home():
    return render_template('/add_task.html')

#route for handling login page logic
@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('add_task'))
    return render_template('/login.html', error=error)

@app.route("/add_task", methods=['GET', 'POST'])
def add_task():
    db = get_db()

    if request.method == 'POST':
        task = request.form['task']
        time_minutes = request.form['time_minutes']

        db.execute(
            'INSERT INTO tasks (task, time_minutes) VALUES (?, ?)',
            (task, time_minutes)
        )
        db.commit()

    tasks = db.execute('SELECT id, task, time_minutes FROM tasks').fetchall()


    #Calculate sum of time_minutes 
    time_sum = sum(task['time_minutes'] for task in tasks)



    return render_template('add_task.html', tasks=tasks, time_sum=time_sum)

    # return render_template('add_task.html')


@app.route("/delete_task/<int:task_id>", methods=['POST'])
def delete_task(task_id):
    print(f"Attempting to delete task with ID: {task_id}")
    db = get_db()
    try:
        db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        db.commit()
        print(f"Task ID {task_id} deleted successfully")
    except Exception as e:
        print(f"Error deleting task {e}")
        db.rollback()
    return redirect(url_for('add_task'))



if __name__ == '__main__':
    app.run(debug=True) 
